from datetime import date

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext

from models import (
    create_user,
    get_user_by_email,
    get_all_users,
    get_user,
    add_user,
    update_user,
    delete_user
)

# ---------------------------------
# APP CONFIG
# ---------------------------------
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="mysecretkey123"
)

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ---------------------------------
# REGISTER
# ---------------------------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, error: str | None = None):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"error": error}
    )


@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    existing_user = get_user_by_email(email)

    if existing_user:
        return RedirectResponse(
            "/register?error=Email+already+exists",
            status_code=303
        )

    hashed_password = pwd_context.hash(password)

    create_user(
        name,
        email,
        hashed_password
    )

    return RedirectResponse(
        "/login?registered=1",
        status_code=303
    )

# ---------------------------------
# LOGIN
# ---------------------------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None, registered: bool = False):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": error, "registered": registered}
    )


@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_email(email)

    if user and pwd_context.verify(
        password,
        user["password"]
    ):
        request.session["user"] = user["name"]
        request.session["user_id"] = user["id"]

        return RedirectResponse(
            "/",
            status_code=303
        )

    return RedirectResponse(
        "/login?error=Invalid+email+or+password",
        status_code=303
    )

# ---------------------------------
# LOGOUT
# ---------------------------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        "/login",
        status_code=303
    )

# ---------------------------------
# HOME
# ---------------------------------
@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    show_header: bool = True,
    show_footer: bool = True
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    users = get_all_users()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "users": users,
            "username": request.session["user"],
            "show_header": show_header,
            "show_footer": show_footer,
            "current_year": date.today().year
        }
    )

# ---------------------------------
# ADD PAGE
# ---------------------------------
@app.get("/add", response_class=HTMLResponse)
def add_page(request: Request,show_header: bool = True,
    show_footer: bool = True):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )
    users = get_all_users()
    return templates.TemplateResponse(
        request,
        "add.html",
        {
            "users": users,
            "username": request.session["user"],
            "show_header": show_header,
            "show_footer": show_footer,
            "current_year": date.today().year
        }
    )

# ---------------------------------
# INSERT USER
# ---------------------------------
@app.post("/add")
def insert_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    add_user(name, email)

    return RedirectResponse(
        "/",
        status_code=303
    )

# ---------------------------------
# EDIT PAGE
# ---------------------------------
@app.get("/edit/{user_id}", response_class=HTMLResponse)
def edit_page(
    request: Request,
    user_id: int,
    show_header: bool = True,
    show_footer: bool = True
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    user = get_user(user_id)

    return templates.TemplateResponse(
        request,
        "edit.html",
        {
            "user": user,
            "username": request.session["user"],
            "show_header": show_header,
            "show_footer": show_footer,
            "current_year": date.today().year
        }
    )

# ---------------------------------
# UPDATE USER
# ---------------------------------
@app.post("/edit/{user_id}")
def edit_user(
    request: Request,
    user_id: int,
    name: str = Form(...),
    email: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    update_user(
        user_id,
        name,
        email
    )

    return RedirectResponse(
        "/",
        status_code=303
    )

# ---------------------------------
# DELETE USER
# ---------------------------------
@app.get("/delete/{user_id}")
def remove_user(
    request: Request,
    user_id: int
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    delete_user(user_id)

    return RedirectResponse(
        "/",
        status_code=303
    )