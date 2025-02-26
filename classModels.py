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
    year: str
    password: str

class StudentId(BaseModel):
    collegeRegNo : str | None
    StudentId : str | None

class Faculty(BaseModel):
    id : str
    collegeId: str
    department: str
    desgination: str
    email: str
    fullName: str
    phone: int
    password: str

class FacultyId(BaseModel):
    facultyId : str | None
    collegeId : str | None

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

class ElectionId(BaseModel) :
    electionId : int

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
    # proofUrl : str
    # date : str
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
    forDate: str
    timeDuration: str
    purpose: str

class ActionSchema(BaseModel):
    action: str
    applicationId : str

class Application(BaseModel):
    type : str
    title : str
    description : str

class ApplicationAction(BaseModel):
    action : str
    applicationId : str
    forwardedTo : str | None

class ApplicationId(BaseModel):
    applicationId : str

class Budget(BaseModel):
    categorie : str
    name : str
    totalBudget : int

class Expense(BaseModel):
    categorie : str
    name : str
    amount : int
    reason : str

class FundRelease(BaseModel):
    categorie : str
    name : str
    reason : str
    amount : int

class FacilityBook(BaseModel):
    facility : str
    date : str
    fromTime : str
    toTime : str

class Date(BaseModel):
    date : str