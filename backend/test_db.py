from database import SessionLocal, Task

db = SessionLocal()
tasks = db.query(Task).all()

for task in tasks:
    print(task.id, task.task, task.username)

db.close()
    