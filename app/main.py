#tomorrow will test recently added features
# also will add more features for the API
# next will adding logging to trace errors and requests
# and will add a database to store tasks instead of in-memory storage
#once done, will create my own pseudocode to use as a reference for future projects
# and will also add a README file to explain how to use the API
#importing necessary tools from fastapi
import logging
import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import List, Optional


# Setting up logging to track errors and requests
chat_logger = logging.getLogger('app_logger')
chat_logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG to capture all messages

# define log message format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('task_app.log')
file_handler.setFormatter(formatter)  # Set the format for the log messages
chat_logger.addHandler(file_handler)  # Add the file handler to the logger

#Stream Handler to log in console
console_handler = logging.FileHandler("task_app.log")
file_handler.setFormatter(formatter)
chat_logger.addHandler(console_handler)

#Prevent duplicate logs in console
chat_logger.propagate = False


# Creating our application - like naming our project
app = FastAPI()

# ====== THE TASKS STORAGE ======
class Task(BaseModel):
		id: int
		title: str
		completed: bool = False
		deleted: bool = False
		created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
		updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
		deleted_at: Optional[str] = None
		
		def display_info(self) -> str:
			return f"[{self.id}] {self.title} | Done: {self.completed} | Deleted: {self.deleted}"

# ======== TASK CONTROLLER, CRUD FUNCTIONS ========		
class TaskManager(BaseModel):
	tasks: List[Task] = Field(default_factory=list)
	next_id: int = 1
	class UpdateTaskReq(BaseModel):
		title: str
		
#====== ADD A NEW TASKS ======		
	def add_task(self, title: str) -> Task:
		if not title or not title.strip():
			raise HTTPException(status_code=400, detail="Title must be included")
		
		task = Task(id=self.next_id, title=title)
		self.tasks.append(task)
		self.next_id += 1
		return task
		
#====== DISPLAY ALL EXISTING TASK ======			
	def get_all_tasks(self):
		return [task for task in self.tasks if not task.deleted]
	

#====== DISPLAY ALL DELETED TASK ======
	def get_all_deleted_tasks(self):
		return [task for task in self.tasks if task.deleted]
		
#======TASK RETRIEVAL BY ID======		
	def get_task(self, task_id):
		for task in self.tasks:
			if task.id == task_id:
				return task
		raise HTTPException(status_code=404, detail="Task not found")
	
#====== GET DELETED TASK BY ID ======	
	def get_deleted_task(self, id: int, deleted: bool = True) -> Optional[Task]:
		deleted_task = self.get_task(id)
		if not deleted_task.deleted:
			raise HTTPException(status_code=404, detail="Task is not Deleted ")
		return deleted_task
	
#======TOGGLE COMPLETED TASK TO NOT COMPLETE ======	
	def toggle_complete_task(self, id: int) -> Optional[Task]:
		task = self.get_task(id)
		task.completed = not task.completed
		task.updated_at = datetime.utcnow().isoformat().replace("+00:00", "Z")
		return task
				
#====== UPDATE EXISTING TASK ======	
	def update_task(self,id: int, new_title: str) -> Optional[Task]:
		task = self.get_task(id)
		if task:
				validated = Task(
					id=task.id, 
					title=new_title, 
					completed=task.completed,
					deleted=task.deleted, 
					created_at=task.created_at
				)
				task.title = validated.title
				task.updated_at = datetime.utcnow().isoformat().replace("+00:00", "Z")

				return task
		
					
#====== DELETE EXISTING TASK ======	
	def delete_task(self, id: int) -> Optional[Task]:
		task = self.get_task(id)  # Find the task by its ID
		task.deleted = True  # Soft-delete the task (mark as deleted)
		task.updated_at = datetime.utcnow().isoformat() + "Z"  # Update the timestamp
		return task  # Return the updated task
		
    
#====== RESTORE DELETED TASK BY ID ======			
	def restore_task(self, id: int) -> Optional[Task]:
		# Try to find the task with the given ID
		task = self.get_task(id)
		if not task.deleted:
			raise HTTPException(status_code=400, detail="Task not deleted yet")
		# If found, restore it by unmarking as deleted
		task.deleted = False
		# Update the timestamp to track when the task was restored
		task.updated_at = datetime.utcnow().isoformat().replace("+00:00", "Z")
		return task  # Return the restored task
	


# Welcome message for visitors
welcome = { "message": "Hello there! welcome to my first API!"}

task_manager = TaskManager()

# ===== SETTING UP OUR ROUTES + LOGGING =====
@app.middleware("http")
async def log_request_info(request: Request, call_next):
    """Log details of every request made to the API"""
    logger = logging.getLogger("uvicorn.access")
    start_time = time.time()

    logger.info(f"Incoming Request: {request.method}, {request.url}")

    body = await request.body()
    try:
        body_text = body.decode("utf-8")
    except UnicodeDecodeError:
        body_text = "<binary data>"

    logger.info(f"Request body: {body_text}")

    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)

    logger.info(f"Response status: {response.status_code}, took {process_time}s")

    return response
        
    

# ===== FRONT DOOR OF OUR HOUSE =====
# When someone visits the root URL (like our home address)
@app.get("/")
def home():
    # Show the welcome message as JSON (like a formatted letter)
    return welcome

# ===== TASK DISPLAY ROOM =====
# When someone visits /tasks with a GET request (looking at tasks)
@app.get("/tasks")
async def get_tasks():
    return task_manager.get_all_tasks()

# ===== SHOW DELETED TASKS =====
#Show all deleted tasks
@app.get("/tasks/deleted", response_model=List[Task])
def get_deleted_tasks():
    return task_manager.get_all_deleted_tasks()

# ===== TASK CREATION STATION =====
# When someone visits /tasks with POST request (delivering new task)
@app.post("/tasks")
def create_task(task:Task):
    return task_manager.add_task(task.title)

# ===== TOGGLE TASK COMPLETE STATUS  =====
@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    return task_manager.toggle_complete_task(task_id)

# ===== TASK RETRIEVAL BY ID =====
@app.get("/tasks/{task_id}")
def retrieve_task(task_id: int):
    return task_manager.get_task(task_id)
    

# ===== TASK UPDATE STATION =====
@app.put("/tasks/{task_id}")
def update_task_request(task_id: int, update: TaskManager.UpdateTaskReq):
	return task_manager.update_task(task_id, update.title)

# ===== TASK DELETION STATION =====
@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int):
	task = task_manager.delete_task(task_id)
	return {
		"message": f"task '{task.id}' has been deleted",
		"task" : task
	}

# ===== SHOW DELETED TASK BY ID =====
@app.get("/tasks/deleted/{task_id}")
def get_deleted_task(task_id:int):
	return task_manager.get_deleted_task(task_id)

# ===== TASK RESTORE =====
@app.put("/tasks/{task_id}/restore")
def task_restore(task_id:int):
	task = task_manager.restore_task(task_id)
	return {
		"message": f"task '{task.title}' successfully restored",
		"task" : task
	}

