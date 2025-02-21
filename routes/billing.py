from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import os
from pydantic import BaseModel
from supabase_client import supabase

router = APIRouter()

class Sponsorship(BaseModel):
    id: int
    name: str
    amount: float
    sponsor: str

class Budget(BaseModel):
    id: int
    category: str
    amount: float
    spent: float

class MessBudget(BaseModel):
    id: int
    month: str
    amount: float
    spent: float

@router.get("/sponsorships", response_model=List[dict])
async def get_sponsorships():
    response = supabase.table("sponsorships").select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.get("/budgets", response_model=List[dict])
async def get_budgets():
    response = supabase.table("budgets").select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.post("/upload_expense_proof")
async def upload_expense_proof(file: UploadFile = File(...)):
    file_location = f"expense_proofs/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    response = supabase.storage().from_("expense_proofs").upload(file_location, file_location)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    
    return {"filename": file.filename, "url": response.data["publicURL"]}

@router.get("/mess_budgets", response_model=List[dict])
async def get_mess_budgets():
    response = supabase.table("mess_budgets").select("*").execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data