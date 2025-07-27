from pydantic import BaseModel
from pydantic.types import constr
from typing import Optional, Literal
from datetime import datetime

#====== DEFINE THE DB SCHEMAS =====
class TaskCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=255) #type: ignore

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    deleted: bool
    created_at:datetime
    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] #type: ignore
    completed: Optional[bool] = None

class TaskUpdateResponse(BaseModel):
    id: int
    title: str
    completed: bool
    deleted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class TaskDeleteResponse(BaseModel):
    id:int
    title: str
    deleted: bool
    deleted_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class TaskRestoreResponse(BaseModel):
    id:int
    title: str
    updated_at: datetime

    class Config:
        orm_mode = True