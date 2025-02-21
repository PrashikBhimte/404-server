from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import os
from supabase_client import supabase

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic models
class Application(BaseModel):
    id: int
    type: str
    title: str
    description: str
    status: str
    priority: int
    created_at: str
    updated_at: str

class ApplicationCreate(BaseModel):
    type: str
    title: str
    description: str

class ApplicationUpdate(BaseModel):
    status: str
    priority: int

# Create APIRouter
router = APIRouter()

@router.post("/applications/", response_model=Application)
async def create_application(application: ApplicationCreate):
    response = supabase.table('applications').insert(application.dict()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

@router.get("/applications/", response_model=List[Application])
async def get_applications():
    response = supabase.table('applications').select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.get("/applications/{application_id}", response_model=Application)
async def get_application(application_id: int):
    response = supabase.table('applications').select("*").eq('id', application_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="Application not found")
    return response.data[0]

@router.put("/applications/{application_id}", response_model=Application)
async def update_application(application_id: int, application: ApplicationUpdate):
    response = supabase.table('applications').update(application.dict()).eq('id', application_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

@router.delete("/applications/{application_id}", response_model=dict)
async def delete_application(application_id: int):
    response = supabase.table('applications').delete().eq('id', application_id).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Application deleted successfully"}

# Include router in the app
