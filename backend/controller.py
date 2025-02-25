from fastapi import Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import TokenResponse, UserInfo, ToDoItem
from service import AuthService

# Initialize HTTPBearer security dependency
bearer_scheme = HTTPBearer()


class AuthController:
    """
    Controller for handling authentication logic.
    """

    # In-memory ToDo list storage
    todos = []

    @staticmethod
    def read_root():
        """
        Root endpoint providing basic information and documentation link.

        Returns:
            dict: A welcome message and link to the documentation.
        """
        return {
            "message": (
                "Welcome to the Keycloak authentication system. "
                "Use the /login endpoint to authenticate and /protected to access the protected resource."
            ),
            "documentation": "/docs",
        }

    @staticmethod
    def login(username: str = Form(...), password: str = Form(...)) -> TokenResponse:
        """
        Authenticate user and return access token.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user.

        Raises:
            HTTPException: If the authentication fails (wrong credentials).

        Returns:
            TokenResponse: Contains the access token upon successful authentication.
        """
        # Authenticate the user using the AuthService
        access_token = AuthService.authenticate_user(username, password)

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return TokenResponse(access_token=access_token)

    @staticmethod
    def protected_endpoint(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> UserInfo:
        """
        Access a protected resource that requires valid token authentication.

        Args:
            credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

        Raises:
            HTTPException: If the token is invalid or not provided.

        Returns:
            UserInfo: Information about the authenticated user.
        """
        # Extract the bearer token from the provided credentials
        token = credentials.credentials

        # Verify the token and get user information
        user_info = AuthService.verify_token(token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_info

    @staticmethod
    def add_todo(user: UserInfo, task: str) -> ToDoItem:
        """
        Add a new ToDo item.

        Args:
            user (UserInfo): The authenticated user's information.
            task (str): The task description.

        Returns:
            ToDoItem: The created ToDo item.
        """
        new_todo = ToDoItem(
            id=len(AuthController.todos) + 1,
            task=task,
            completed=False,
            username=user.preferred_username  # Extracting the username string
        )
        AuthController.todos.append(new_todo)
        return new_todo

    @staticmethod
    def get_todos(user: UserInfo):
        """
        Retrieve all ToDo items for the authenticated user.

        Args:
            user (UserInfo): The authenticated user's information.

        Returns:
            list[ToDoItem]: List of ToDo items for the user.
        """
        return [todo for todo in AuthController.todos if todo.username == user.preferred_username]

    @staticmethod
    def delete_todo(user: UserInfo, todo_id: int):
        """
        Delete a ToDo item for the authenticated user.

        Args:
            user (UserInfo): The authenticated user's information.
            todo_id (int): The ID of the ToDo item to delete.

        Raises:
            HTTPException: If the ToDo item is not found.

        Returns:
            dict: Success message.
        """
        for index, todo in enumerate(AuthController.todos):
            if todo.id == todo_id and todo.username == user.preferred_username:
                del AuthController.todos[index]
                return {"message": "ToDo item deleted successfully"}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDo item not found or unauthorized"
        )
