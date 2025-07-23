import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List
from models.task import Task
from services.task_service import TaskManager
from config.get_logger import get_logger
from config.middleware import logging_middleware
from api.task_routes import router as task_router

# Creating our application - like naming our project
app = FastAPI()
app.middleware("http")(logging_middleware)

#logger config
logger = get_logger()
logger.info("Server is starting...")

#task manager instance
task_manager = TaskManager()
	
#mount the router
app.include_router(task_router, prefix="/api")

   



