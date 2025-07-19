#!/bin/bash


# Run the FastAPI application using uvicorn
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn app.main:app --reload
