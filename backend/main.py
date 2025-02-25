from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from models import TokenResponse, UserInfo, ToDoItem
from controller import AuthController

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update this based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication scheme
bearer_scheme = HTTPBearer()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI ToDo App"}

# Login model
class LoginRequest(BaseModel):
    username: str
    password: str

# Login endpoint (expects JSON instead of form data)
@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    token = AuthController.login(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

# Protected user info endpoint
@app.get("/protected", response_model=UserInfo)
async def protected_endpoint(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = AuthController.protected_endpoint(credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    return user

# Get all ToDo items for the authenticated user
@app.get("/todos", response_model=List[ToDoItem])
async def get_todos(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    todos = AuthController.get_todos(user)
    if todos is None:
        raise HTTPException(status_code=404, detail="No ToDo items found")
    
    return todos

# Add a new ToDo item
class TodoRequest(BaseModel):
    task: str

@app.post("/todos", response_model=ToDoItem)
async def add_todo(request: TodoRequest, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    new_todo = AuthController.add_todo(user, request.task)
    if not new_todo:
        raise HTTPException(status_code=400, detail="Failed to add ToDo item")
    
    return new_todo

# Delete a ToDo item
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    success = AuthController.delete_todo(user, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    
    return {"message": "ToDo item deleted successfully"}
