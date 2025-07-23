
from typing import List, Optional
from models.task import Task
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field

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