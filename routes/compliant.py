from fastapi import APIRouter, HTTPException, Depends
from classModels import Complaint, ComplaintVote
from supabase_client import supabase
from dependencies import get_user_id, get_faculty_details, is_valguare, get_student_details


router = APIRouter()


@router.post("/submit")
async def submit_complaint(complaint: Complaint, id : str = Depends(get_user_id)):
    try:
    
        if is_valguare(complaint.complaint_text):
            raise HTTPException(status_code=400, detail="Content is found valgaur!")
        
        response = supabase.table("Complaints").insert({"complaint": complaint.complaint_text, "studentId" : id}).execute()
        supabase.table("ComplaintsIdentity").insert({"ShouldRevealVotes": 0, "id" : dict(response.data[0])['id']}).execute()

        return {"message": "Complaint submitted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get")
async def get_complaints():
    try:
        response = supabase.table("Complaints").select("*").execute()

        return dict(response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/vote')
def vote_for_complaint(complaintVote : ComplaintVote, id : str = Depends(get_user_id)):
    try:
        designation = get_faculty_details(id)['desgination'] 

        if designation != "Board Member" :
            raise HTTPException(status_code=401, detail="Your are not authorised to vote here.") 

        complaintsIdentityVotes = dict(supabase.table("ComplaintsIdentity").select("*").eq("id", complaintVote.complaintId).execute().data[0])['ShouldRevealVotes']
         
        response = supabase.table("ComplaintsIdentity").update({"ShouldRevealVotes": complaintsIdentityVotes + 1}).eq("id", complaintVote.complaintId).execute()
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/identities")
async def get_high_voted_complaints_identitites():
    try:
        response = supabase.table("ComplaintsIdentity").select("*").gt("ShouldRevealVotes", 5).execute()

        complaints_data = response.data
        if not complaints_data:
            return {"message": "No complaints found with votes greater than 5"}

        complaint_ids = [item["id"] for item in complaints_data]

        student_response = supabase.table("Complaints").select("*").in_("id", complaint_ids).execute().data

        students = []

        for i in student_response:
            details = get_student_details(i['studentId'])
            details['complaint'] = i['complaint']
            students.append(details)

        return {"high_voted_complaints": students}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
