from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import get_user_id
from supabase_client import supabase

router = APIRouter()

@router.get('/details')
def get_student_details(id : str = Depends(get_user_id)):

    user_details = dict(supabase.table('Student').select("*").eq("id", id).execute())
    
    if user_details['count'] != 0:
        return dict(user_details['data'][0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.")


@router.get("/allstudents")
async def get_students(branch: str = Query(None), year: int = Query(None)):

    try:
        query = supabase.table("Students").select("*")

        if branch:
            query = query.eq("branch", branch)

        if year:
            query = query.eq("year", year)

        response = query.execute()

        if not response.data:
            return {"message": "No students found with the given filters"}

        return {"students": response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
