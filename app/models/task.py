from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ====== THE TASKS STORAGE ======
class Task(BaseModel):
		id: int
		title: str
		completed: bool = False
		deleted: bool = False
		created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
		updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
		deleted_at: Optional[str] = None