from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from pydantic import BaseModel, EmailStr, ValidationError
from typing import List, Optional
from email_utils import send_confirmation_email
from fastapi.responses import HTMLResponse


from crud import get_all_students, get_student_by_id, create_student, register, update_student, delete_student

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    dob: str
    address: str
    gender: str
    phone: List[str]


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    dob: List = Form(...),
    address: str = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
):
    phone_numbers = [p.strip() for p in phone.split(",")]
    try:
        register(name, email, dob, phone_numbers, address, gender)
        send_confirmation_email(email)
        return templates.TemplateResponse("register.html", {"request": request, "message": "Registration Successful!"})
    except ValidationError as e:
        return templates.TemplateResponse("register.html", {"request": request, "errors": e.errors()})


@app.get("/")
async def read_students(request: Request):
    students = get_all_students()
    return templates.TemplateResponse("register.html", {"request": request, "students": students})


@app.get("/students/create/")
async def create_student_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/students/create/")
async def create_student_handler(request: Request, name: str = Form(...), age: int = Form(...)):
    create_student(name, age)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


@app.get("/students/update/{student_id}")
async def update_student_form(request: Request, student_id: int):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("update.html", {"request": request, "student": student})


@app.post("/students/update/{student_id}")
async def update_student_handler(request: Request, student_id: int, name: str = Form(...), age: int = Form(...)):
    update_student(student_id, name, age)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


@app.post("/students/delete/{student_id}")
async def delete_student_handler(student_id: int):
    delete_student(student_id)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)
