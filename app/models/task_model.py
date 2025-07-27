
#======= CREATE THE DATABASE MODEL ======
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.config.database import Base

#====== DEFINES THE DB TABLE FIELDS ======
class TaskDB(Base):
    __tablename__ = "tasks"

    id= Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)