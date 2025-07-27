
from typing import List, Optional
from app.models.task import Task
from datetime import datetime, timezone
from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from app.models.task_model import TaskDB
from app.schemas.task_schema import TaskUpdate
from app.config.database import get_db
from sqlalchemy.orm import Session

# ======== TASK CONTROLLER, CRUD FUNCTIONS ========		
class TaskManager:
	def __init__(self, db: Session):
		self.db = db


#================= POST METHOD ===================

#====== ADD A NEW TASKS ======		
	def add_task(self, title: str) -> TaskDB:
		if not title or not title.strip():
			raise HTTPException(status_code=400, detail="Title must be included")
		
		task = TaskDB(title=title)
		self.db.add(task)
		self.db.commit()
		self.db.refresh(task)
		return task
	
#=====================================================

#================= GET METHOD ===================

#====== DISPLAY ALL EXISTING TASK ======			
	def get_all_tasks(self):
		all_tasks = self.db.query(TaskDB).filter_by(deleted=False).all()
		if not all_tasks:
			raise HTTPException(status_code=200, detail="No active tasks found")
		return all_tasks
	

#====== DISPLAY ALL DELETED TASK ======
	def get_all_deleted_tasks(self):
		all_deleted_tasks = self.db.query(TaskDB).filter_by(deleted=True).all()
		if not all_deleted_tasks:
			raise HTTPException(status_code=200, detail="No deleted tasks found")
		return all_deleted_tasks 
		
#======TASK RETRIEVAL BY ID======		
	def get_task(self, task_id):
		task = self.db.query(TaskDB).filter_by(id=task_id).first()
		if not task:
			raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")
		return task
	
#====== GET DELETED TASK BY ID ======	
	def get_deleted_task(self, task_id:int, deleted: bool = True) -> Optional[Task]:
		task = self.db.query(TaskDB).filter_by(id=task_id,deleted=True).first()
		if not task:
			raise HTTPException(status_code=404, detail=f"Task ID {task_id} is not Deleted ")
		return task
	
#=====================================================

#================= PUT METHOD ===================
				
#====== UPDATE EXISTING TASK ======	
	def update_task(self,id: int, update_data: TaskUpdate) -> Optional[Task]:
		task = self.get_task(id)
		if not task:
			raise HTTPException(status_code=404, detail=f"Task ID {id} not found")
		
		if update_data.title is not None:
				task.title = update_data.title
		if update_data.completed is not None:
				task.completed = update_data.completed

		task.updated_at = datetime.utcnow()
		self.db.commit()
		self.db.refresh(task)
		return task

#====== RESTORE DELETED TASK BY ID ======			
	def restore_task(self, id: int) -> Optional[Task]:
		# Try to find the task with the given ID
		task = self.get_task(id)
		if not task.deleted:
			raise HTTPException(status_code=400, detail="Task not deleted yet")
		# If found, restore it by unmarking as deleted
		task.deleted = False
		# Update the timestamp to track when the task was restored
		task.updated_at = datetime.utcnow()
		self.db.commit()
		self.db.refresh(task)
		return task  # Return the restored task		
	
#=====================================================	

#================= DELETE METHOD ===================
				
#====== DELETE EXISTING TASK ======	
	def delete_task(self, id: int) -> Optional[TaskDB]:
		task = self.get_task(id)  # Find the task by its ID
		task.deleted = True  # Soft-delete the task (mark as deleted)
		task.deleted_at = datetime.utcnow()
		task.updated_at = datetime.utcnow()  # Update the timestamp
		if not task:
			raise HTTPException(status_code=404, detail=f"Task ID {id} not found")
		self.db.commit()
		self.db.refresh(task)
		return task  # Return the updated task
		
    
