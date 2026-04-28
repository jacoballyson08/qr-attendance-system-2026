from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_db
from fastapi.staticfiles import StaticFiles
import qrcode
import os



from controllers.attendance_controller import (
    register_user,
    login_user,
    scan_attendance,
    attendance_records
)

app = FastAPI()
app.mount("/qrcodes", StaticFiles(directory="qrcodes"), name="qrcodes")
templates = Jinja2Templates(directory="templates")



# HOME
@app.get("/")
def home():
    return RedirectResponse("/login")


# LOGIN PAGE
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# REGISTER PAGE
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@app.get("/my-qr/{student_id}", response_class=HTMLResponse)
def my_qr(request: Request, student_id: str):

    return templates.TemplateResponse(
        request=request,
        name="my_qr.html",
        context={
            "request": request,
            "student_id": student_id
        }
    )

# REGISTER USER
@app.post("/register")
def register(
    student_id: str = Form(...),
    name: str = Form(...),
    password: str = Form(...)
):

    # save user
    register_user(student_id, name, password)

    # generate QR
    qr = qrcode.make(student_id)

    # save QR image
    file_path = f"qrcodes/{student_id}.png"
    qr.save(file_path)

    # redirect to QR page
    return RedirectResponse(
        f"/my-qr/{student_id}",
        status_code=303
    )


# LOGIN USER
@app.post("/login")
def login(student_id: str = Form(...), password: str = Form(...)):

    user = login_user(student_id, password)

    if user is None:
        return RedirectResponse("/login?error=1", status_code=303)

    return RedirectResponse("/dashboard", status_code=303)


# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    records = attendance_records()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"records": records}
    )

@app.get("/scanner", response_class=HTMLResponse)
def scanner_page(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="scanner.html",
        context={"request": request}
    )

# QR SCAN
@app.get("/scan")
def scan(student_id: str):

    user = scan_attendance(student_id)

    if not user:
        return {"error": "Student not found"}

    return {
        "message": "Attendance recorded",
        "name": user["name"]
    }


@app.post("/admin/reset-attendance")
def admin_reset_attendance(password: str = Form(...)):
    if password != "admin123":
        return {"error": "Unauthorized"}

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM attendance")
    db.commit()
    db.close()

    return RedirectResponse("/dashboard", status_code=303)