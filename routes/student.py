from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies import get_user_id
from supabase_client import supabase
from classModels import StudentId

router = APIRouter()

@router.get('/details')
def get_student_details(id : str = Depends(get_user_id)):

    user_details = dict(supabase.table('Student').select("*").eq("id", id).execute())
    
    if len(user_details['data']) != 0:
        return dict(user_details['data'][0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.")


@router.get("/all")
async def get_all_students(branch: str = Query(None), year: int = Query(None)):

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

@router.post('/deatils_by_id')
def get_student_details_by_id(studentDetails : StudentId):

    if studentDetails.StudentId:
        user_details = dict(supabase.table('Student').select("*").eq("id", studentDetails.StudentId).execute())
    elif studentDetails.collegeRegNo:
        user_details = dict(supabase.table('Student').select("*").eq("collegeRegNo", studentDetails.collegeRegNo).execute())
    else :
        raise HTTPException(status_code=400, detail="Either StudentId or collegeRegNo is required.")

    if len(user_details['data']) != 0:
        return dict(user_details['data'][0])
    else :
        raise HTTPException(status_code=404, detail="User details not found, may be access token is incorrect or failed.")