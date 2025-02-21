from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import get_user_id
from supabase_client import supabase

router = APIRouter()

@router.get('/details')
def get_faculty_details(id : str = Depends(get_user_id)):

    user_details = dict(supabase.table('Faculty').select("*").eq("id", id).execute())

    if user_details['count'] != 0:
        return dict(user_details['data'][0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.")


@router.get("/all")
async def get_all_faculties(department: str = Query(None), designation: str = Query(None)):
    
    try:
        query = supabase.table("Faculty").select("*")

        if department:
            query = query.eq("department", department)

        if designation:
            query = query.eq("desgination", designation)

        response = query.execute()

        if  len(response.data) == 0:
            return {"message": "No faculty found with the given filters"}

        return {"faculty": response.data}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
