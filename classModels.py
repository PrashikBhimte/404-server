from pydantic import BaseModel
from typing import List, Dict, Any

class User(BaseModel):
    role: str
    data: dict

class Student(BaseModel):
    id : str
    branch: str
    club: str
    collegeRegNo: str
    email: str
    fullName: str
    parentEmail: str
    parentPhone: int
    position: str
    year: str
    password: str

class Faculty(BaseModel):
    id : str
    collegeId: str
    department: str
    desgination: str
    email: str
    fullName: str
    phone: int
    password: str

class LoginDetails(BaseModel):
    email : str
    password : str

class TokenRequest(BaseModel):
    access_token : str
    refresh_token : str

class ElectionDetails(BaseModel):
    poistion : str
    year_eligible : dict
    branch_eligible : dict
    requirments : str
    start : str
    end : str

class Candidate(BaseModel) :
    electionId : int
    manifesto : str
    proposals : str

class Vote(BaseModel) :
    candidateId : str
    electionId : int

class DoctorAdvice(BaseModel):
    collegeRegNo : str
    symptoms : str
    advice : str
    no_of_rest_days : int

class InOutReg(BaseModel):
    collegeRegNo : str
    in_or_out : str

class StudentCheated(BaseModel):
    collegeRegNo : str
    reason : str
    proofUrl : str
    date : str
    examination : str
    invigilatorCollegeId : str
    subject : str
    semester : str

class Complaint(BaseModel):
    complaint_text: str

class ComplaintVote(BaseModel):
    complaintId : str

class FacilityApplication(BaseModel):
    facilitiy: str
    # studentId: str
    # facultyId: str
    # status: str
    forDate: str
    timeDuration: str
    purpose: str
    # forwardedSchema: List[Dict[str, Any]]

class ActionSchema(BaseModel):
    facultyId: str
    dateTime: str
    action: str