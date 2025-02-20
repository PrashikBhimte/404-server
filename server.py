from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.session import router as session_routes
from routes.student import router as student_routes
from routes.faculty import router as faculty_routes
from routes.election import router as election_routes
from routes.doctorAdvice import router as doctor_routes

server = FastAPI()

server.include_router(session_routes)
server.include_router(student_routes, prefix='/student')
server.include_router(faculty_routes, prefix='/faculty')
server.include_router(election_routes, prefix='/election')
server.include_router(doctor_routes, prefix="/doctor")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://192.168.1.138:5173"
]

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.get('/')
def home():
    return "Hello world!"
