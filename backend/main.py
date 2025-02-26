from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from models import TokenResponse, UserInfo, ToDoItem, Todo
from controller import AuthController
from database import SessionLocal

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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def get_todos(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    todos = db.query(Todo).filter(Todo.user_id == user.preferred_username).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No ToDo items found")
    
    return todos

# Add a new ToDo item
class TodoRequest(BaseModel):
    task: str

@app.post("/todos", response_model=ToDoItem)
async def add_todo(request: TodoRequest, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")

    new_todo = Todo(title=request.task, user_id=user.preferred_username)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

# Delete a ToDo item
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user = AuthController.protected_endpoint(credentials)  # Verify user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.preferred_username).first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    
    db.delete(todo)
    db.commit()
    
    return {"message": "ToDo item deleted successfully"}
