from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Model (Needed for ForeignKey reference in Todo)
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Matches Keycloak `sub`
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    todos = relationship("Todo", back_populates="user")  # Link to ToDo tasks

# ToDo Model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"))  # Link to users table
    user = relationship("User", back_populates="todos")  # Establish relationship

    def __repr__(self):
        return f"<Todo {self.title}>"

# Pydantic Models for API Requests & Responses
class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserInfo(BaseModel):
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

# ✅ Fixed ToDoItem Model (Now Matches Database Schema)
class ToDoItem(BaseModel):
    id: Optional[int] = None  # Auto-incremented in the database
    title: str  # Changed from `task` to match DB column
    description: Optional[str] = None
    completed: bool = False
    user_id: str  # Stores user ID instead of username for consistency

    class Config:
        orm_mode = True  # Ensures compatibility with SQLAlchemy models
