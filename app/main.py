from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from .crud import get_all_students, get_student_by_id, create_student, update_student, delete_student

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def read_students(request: Request):
    students = get_all_students()
    return templates.TemplateResponse("index.html", {"request": request, "students": students})


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
