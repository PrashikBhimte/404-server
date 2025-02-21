from fastapi import APIRouter, HTTPException, Depends
from classModels import StudentCheated
from dependencies import get_user_id, get_faculty_details
from supabase_client import supabase

router = APIRouter()

allowed_designations = ["HOD"]

@router.post('/register')
def register_student_cheated(student: StudentCheated, id : str = Depends(get_user_id)):
    
    student = dict(student)

    designation = get_faculty_details(id)['designation']
    if designation not in allowed_designations:
        raise HTTPException(status_code=400, detail="Only HOD can register a student as cheated")
    
    student_details = dict(supabase.table("Student").select("*").eq("collegeRegNo", student["collegeRegNo"]).execute().data[0])

    if not student_details:
        raise HTTPException(status_code=400, detail="Student not found")
    
    student["id"] = student_details['id']
    student["name"] = student_details['fullName']

    faculty_details = dict(supabase.table("Faculty").select("*").eq("collegeId", student['invigilatorCollegeId']).execute().data[0])

    if not faculty_details:
        raise HTTPException(status_code=400, detail="Faculty not found")
    
    student["invigilatorName"] = faculty_details['fullName']
    student["invigilatorId"] = faculty_details['id']

    response = supabase.table("StudentCheated").insert(student).execute()
    
    if response['error']:
        raise HTTPException(status_code=400, detail="Failed to register student as cheated")
    
    return {"status": "Successfully registered student as cheated", "response" : response}


@router.get('/get')
def get_student_cheated():

    response = supabase.table("StudentCheated").select("*").execute()

    if response['error']:
        raise HTTPException(status_code=400, detail="Failed to fetch cheated students")

    return response['data']