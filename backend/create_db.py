from database import engine
from models import Base, User, Todo  # Import all models

Base.metadata.create_all(bind=engine)
