from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pprint import pprint
import pymysql

app = FastAPI()

templates = Jinja2Templates(directory="templates") 
templates.env.cache = {}

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,    
        database="fastapi_db",
        cursorclass=pymysql.cursors.DictCursor
    )


# -------------------------
# VIEW ALL (HTML PAGE)
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    pprint(users)
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users
    })


# -------------------------
# ADD PAGE
# -------------------------
@app.get("/add", response_class=HTMLResponse)
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


# -------------------------
# INSERT
# -------------------------
@app.post("/add")
def add_user(name: str = Form(...), email: str = Form(...)):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)


# -------------------------
# EDIT PAGE
# -------------------------
@app.get("/edit/{user_id}", response_class=HTMLResponse)
def edit_page(request: Request, user_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    db.close()

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "user": user
    })


# -------------------------
# UPDATE
# -------------------------
@app.post("/edit/{user_id}")
def update_user(user_id: int, name: str = Form(...), email: str = Form(...)):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)


# -------------------------
# DELETE
# -------------------------
@app.get("/delete/{user_id}")
def delete_user(user_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)