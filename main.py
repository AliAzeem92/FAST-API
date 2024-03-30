from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Define the Student model
class Student(BaseModel):
    name: str
    age: int
    grade: str

# Initialize FastAPI
app = FastAPI()

# In-memory database to store students
students_db: Dict[int, Student] = {}


# Routes for CRUD operations

# Create a new student
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    student_id = len(students_db) + 1
    students_db[student_id] = student
    return student

# Retrieve all students
@app.get("/students/")
def read_students():
    return students_db.values()

# Retrieve specific student details
@app.get("/students/{student_id}")
def read_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

# Update a student's details
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[student_id] = student
    return student

# Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"message": "Student deleted successfully"}
