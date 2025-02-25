import logging
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID  # Requires `pip install python-keycloak`
from pydantic import BaseModel
import jwt

# Import settings
try:
    from config import settings
except ImportError:
    raise ImportError("Ensure `config.py` contains settings like server_url, client_id, realm, etc.")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OAuth2 Configuration for FastAPI Docs
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.authorization_url,
    tokenUrl=settings.token_url,
)

# Keycloak Client Configuration
keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,
    client_id=settings.client_id,
    realm_name=settings.realm,
    client_secret_key=settings.client_secret,
    verify=True
)


# **Pydantic User Model**
class User(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    realm_roles: list
    client_roles: list


async def get_idp_public_key() -> str:
    """
    Fetch Keycloak's public key dynamically to verify tokens.
    """
    try:
        public_key = keycloak_openid.public_key()
        if not public_key:
            raise ValueError("Empty public key received from Keycloak")
        
        logger.info("Successfully fetched Keycloak public key.")
        return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    except Exception as e:
        logger.error(f"Failed to fetch Keycloak public key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch identity provider public key",
        )


async def get_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Validate and decode the Keycloak access token.
    """
    logger.info(f"Received Token: {token}")  # Debugging token

    if not token:
        logger.error("No token received")
        raise HTTPException(status_code=401, detail="Missing authentication token")

    try:
        public_key = await get_idp_public_key()
        
        # Decode JWT token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_exp": True}
        )

        logger.info(f"Token successfully decoded for user: {decoded_token.get('preferred_username')}")
        return decoded_token
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication error")


async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    """
    Extracts user details from the decoded token.
    """
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("resource_access", {}).get(settings.client_id, {}).get("roles", [])
        )
    except Exception as e:
        logger.error(f"Error parsing user information: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error extracting user details from token",
        )
