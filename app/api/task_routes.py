from fastapi import APIRouter, HTTPException
from typing import List

from app.models.task import Task
from app.services.task_service import TaskManager

router = APIRouter()
task_manager = TaskManager()


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
@router.get("/tasks")
async def get_tasks():
    return task_manager.get_all_tasks()

# ===== SHOW DELETED TASKS =====
#Show all deleted tasks
@router.get("/tasks/deleted", response_model=List[Task])
def get_deleted_tasks():
    return task_manager.get_all_deleted_tasks()

# ===== TASK CREATION STATION =====
# When someone visits /tasks with POST request (delivering new task)
@router.post("/tasks")
def create_task(task:Task):
    return task_manager.add_task(task.title)

# ===== TOGGLE TASK COMPLETE STATUS  =====
@router.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    return task_manager.toggle_complete_task(task_id)

# ===== TASK RETRIEVAL BY ID =====
@router.get("/tasks/{task_id}")
def retrieve_task(task_id: int):
    return task_manager.get_task(task_id)
    

# ===== TASK UPDATE STATION =====
@router.put("/tasks/{task_id}")
def update_task_request(task_id: int, update: TaskManager.UpdateTaskReq):
	return task_manager.update_task(task_id, update.title)

# ===== TASK DELETION STATION =====
@router.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int):
	task = task_manager.delete_task(task_id)
	return {
		"message": f"task '{task.id}' has been deleted",
		"task" : task
	}

# ===== SHOW DELETED TASK BY ID =====
@router.get("/tasks/deleted/{task_id}")
def get_deleted_task(task_id:int):
	return task_manager.get_deleted_task(task_id)

# ===== TASK RESTORE =====
@router.put("/tasks/{task_id}/restore")
def task_restore(task_id:int):
	task = task_manager.restore_task(task_id)
	return {
		"message": f"task '{task.title}' successfully restored",
		"task" : task
	}