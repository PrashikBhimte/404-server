from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from datetime import datetime
from supabase_client import supabase, supabase_url
from classModels import Budget, Expense
from dependencies import get_user_id, get_faculty_details
import json

router = APIRouter()

authorisedFaculty = ['Director', 'HOD']

@router.get("/all")
async def yearly_budgets():
    try:
        response = supabase.table('Budgets').select('*').execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/add')
async def add_budget(budget: Budget, id: str = Depends(get_user_id)):

    user = get_faculty_details(id)

    if user['desgination'] not in authorisedFaculty :
        raise HTTPException(status_code=401, detail="You are not authorised.")
    try:
        budget = dict(budget)
        budget['year'] = int(datetime.now().year)
        budget['availableFund'] = budget['totalBudget']
        budget['fundSpent'] = 0
        
        response = supabase.table('Budgets').insert(budget).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/expense')
async def add_expense(expense: str = Form(...), file: UploadFile = File(...), id : str = Depends(get_user_id)):
    try:
        expense_data = json.loads(expense)
        expense = Expense(**expense_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid expense JSON data")
    
    try :
        response = list(supabase.table('FundAuthority').select("*").execute().data)

        for i in response:
            if id == i['id'] and expense.categorie == i['categorie'] and expense.name == i['name'] :
                try:
                    expense = dict(expense)
                    year = int(datetime.now().year)
                    expense['proofUrl'] = ""

                    response = supabase.table('Expenses').insert(expense).execute()
                    print('working')
                    if not response.data:
                        raise HTTPException(status_code=400, detail="Failed to insert expense")

                    id = response.data[0]['id']

                    response = supabase.table('Budgets').select('*').eq('year', year).eq('categorie', expense['categorie']).eq('name', expense['name']).execute()
                    if not response.data:
                        raise HTTPException(status_code=404, detail="Budget not found")

                    budget = response.data[0]
                    budget['fundSpent'] += expense['amount']
                    budget['availableFund'] -= expense['amount']

                    supabase.table('Budgets').update(budget).eq('id', budget['id']).execute()

                    file_extension = file.filename.split(".")[-1]
                    file_name = f"{id}.{file_extension}"
                    file_content = await file.read()

                    upload_response = supabase.storage.from_("profile-images").upload(
                        file_name, file_content, {"content-type": file.content_type}
                    )
                    if not upload_response:
                        raise HTTPException(status_code=500, detail="File upload failed")

                    image_url = f"{supabase_url}/storage/v1/object/public/profile-images//{file_name}"
                    supabase.table('Expenses').update({"proofUrl": image_url}).eq('id', id).execute()

                    return {"message": "Expense added successfully", "proofUrl": image_url}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))

        raise HTTPException(status_code=400, detail="categories and names does not exits.")
    except :
        raise HTTPException(status_code=400, detail="categories and names does not exits.")

@router.get('/expenses')
async def get_expenses():
    try:
        response = supabase.table('Expenses').select('*').execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
