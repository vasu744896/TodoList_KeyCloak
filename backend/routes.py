from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Todo
from .schemas import TodoCreate, TodoResponse
from .auth import get_current_user  # Keycloak user authentication

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    new_todo = Todo(**todo.dict(), user_id=user["sub"])  # Assign task to logged-in user
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos/", response_model=list[TodoResponse])
async def get_todos(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Todo).filter(Todo.user_id == user["sub"]).all()
