from pydantic import BaseModel

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
    profilePhoto: str
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
    profilePhoto: str
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