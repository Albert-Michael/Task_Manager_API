from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.models.task import Task
from app.models.task_model import TaskDB
from app.services.task_service import TaskManager
from app.config.database import get_db 
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdateResponse, TaskUpdate, TaskRestoreResponse, TaskDeleteResponse
from datetime import datetime

router = APIRouter()


# Welcome message for visitors
welcome = { "message": "Hello there! welcome to my first API!"}


# ===== FRONT DOOR OF OUR HOUSE =====
# When someone visits the root URL (like our home address)
@router.get("/")
def home():
    # Show the welcome message as JSON (like a formatted letter)
    return welcome

# ===== TASK DISPLAY ROOM =====
# When someone visits /tasks with a GET request (looking at tasks)
@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(db: Session = Depends(get_db)):
    task_manager = TaskManager(db) 
    return task_manager.get_all_tasks()

# ===== SHOW DELETED TASKS =====
#Show all deleted tasks
@router.get("/tasks/deleted", response_model=List[TaskResponse])
def get_deleted_tasks(db: Session = Depends(get_db)):
    deleted_tasks = TaskManager(db)
    return deleted_tasks.get_all_deleted_tasks()

# ===== TASK CREATION STATION =====
# When someone visits /tasks with POST request (delivering new task)
@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate, db: Session = Depends(get_db)):
    task_manager = TaskManager(db)

    try:
        new_task = task_manager.add_task(task.title)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== TASK RETRIEVAL BY ID =====
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def retrieve_task(task_id: int, db: Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.get_task(task_id)
    

# ===== TASK UPDATE STATION =====
@router.put("/tasks/{task_id}", response_model=TaskUpdateResponse, status_code=status.HTTP_202_ACCEPTED)
def update_task_request(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
   task_manager = TaskManager(db)
   return task_manager.update_task(task_id, update)


# ===== TASK DELETION STATION =====
@router.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
def delete_existing_task(task_id: int, db:Session = Depends(get_db)):
    task_manager= TaskManager(db)
    return task_manager.delete_task(task_id)

# ===== SHOW DELETED TASK BY ID =====
@router.get("/tasks/deleted/{task_id}",response_model=TaskResponse)
def get_deleted_task(task_id:int, db:Session = Depends(get_db)):
    task_manager = TaskManager(db)
    return task_manager.get_deleted_task(task_id)

# ===== TASK RESTORE =====
@router.put("/tasks/{task_id}/restore", response_model=TaskRestoreResponse)
def task_restore(task_id: int, db:Session = Depends(get_db)):
   task_manager = TaskManager(db)
   return task_manager.restore_task(task_id)