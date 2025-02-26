from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from classModels import StudentCheated
from dependencies import get_user_id, get_faculty_details
from supabase_client import supabase, supabase_url
import json

router = APIRouter()

allowed_designations = ["HOD"]

@router.post('/register')
async def register_student_cheated(student: str = Form(...), file : UploadFile = File(...) , id : str = Depends(get_user_id)):

    try:
        student_data = json.loads(student)
        student = StudentCheated(**student_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid expense JSON data")
    
    student = dict(student)

    designation = get_faculty_details(id)['desgination']
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
    student['proofUrl'] = ""
    student.pop('invigilatorCollegeId')

    response = dict(supabase.table("StudentCheated").insert(student).execute().data[0])

    file_extension = file.filename.split(".")[-1]
    file_name = f"{response['id']}.{file_extension}"

    file_content = await file.read()

    res = supabase.storage.from_("cheated-proof").upload(
            file_name, file_content, {"content-type": file.content_type}
        )

    image_url = f"{supabase_url}/storage/v1/object/public/cheated-proof//{file_name}"

    response['proofUrl'] = image_url

    response = dict(supabase.table("StudentCheated").update(response).eq('id', response['id']).execute().data[0])
    
    return {"status": "Successfully registered student as cheated", "response" : response}


@router.get('/get')
def get_student_cheated():

    response = supabase.table("StudentCheated").select("*").execute()

    return response.data