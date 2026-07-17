import mysql.connector
from typing import Annotated, Optional
from fastapi import FastAPI, Form, Request # From
from fastapi.responses import RedirectResponse, FileResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()

con = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME")
)

app=FastAPI()

app.add_middleware(SessionMiddleware, secret_key="2365533")
app.mount("/static", StaticFiles(directory="static"), name="static")

def db_addmem(data):
    cursor = con.cursor()
    sql_insert = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s);" # placeholder
    cursor.execute(sql_insert, data) # placeholder
    con.commit()

def db_readmem():
    cursor = con.cursor()
    sql = "SELECT * FROM member;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

#########

def db_addmsg(data):
    cursor = con.cursor()
    sql_insert = "INSERT INTO message (member_id, content) VALUES (%s, %s);" # placeholder
    cursor.execute(sql_insert, data) # placeholder
    con.commit()

def db_readmsg():
    cursor = con.cursor()
    sql = "SELECT message.*, member.name FROM message JOIN member ON message.member_id = member.id ORDER BY message.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def db_delmsg(data):
    cursor = con.cursor()
    sql = "DELETE FROM message WHERE id = %s"
    cursor.execute(sql, (data,)) #不接受字串，只接受tuple()
    con.commit()
#########

@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.post("/signup")
def register(signup_name: str = Form(...), signup_email: str = Form(...), signup_password: str = Form(...)): # Form
    data = (signup_name, signup_email, signup_password)
    db_mem = db_readmem()
    for i in db_mem:
        if i[2] == signup_email:
            return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)
    db_addmem(data)
    return RedirectResponse(url="/", status_code=303) 

@app.post("/login")
def login(request: Request, login_email: str = Form(...), login_password: str = Form(...)):
    data_tocheck = (login_email, login_password)
    data = db_readmem()
    # (1, 'test2', 'test@test.com', 'test', 0, datetime.datetime(2026, 7, 9, 21, 48, 40))
    
    for i in data:
        if data_tocheck[0] == i[2]:
            if data_tocheck[1] == i[3]:
                request.session["logged_in"] = True
                request.session["member_id"] = i[0]
                return RedirectResponse(url="/member", status_code=303) # 307 Temporary Redirect+405 Method Not Allowed ->預設redirect是307
            else:
                return RedirectResponse(url="/ohoh?msg=帳號、密碼輸入錯誤", status_code=303)
    return RedirectResponse(url="/ohoh?msg=帳號、密碼輸入錯誤", status_code=303)

@app.get('/api/auth/status')
def status(request:Request):
    member_id = request.session["member_id"] # .get("member_id")/ 資料型態是 Python 的字典（dict)，它就可以用 .get("key")
    data = db_readmem()
    # (1, 'test2', 'test@test.com', 'test', 0, datetime.datetime(2026, 7, 9, 21, 48, 40))
    for i in data:
        if i[0] == member_id:
            member_name = i[1]
    return {"member_id": member_id, "member_name": member_name}

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    request.session["logged_in"] = False
    return RedirectResponse(url="/")

@app.get("/member")
def member(request: Request):
    is_loggedin = request.session.get("logged_in")
    if not is_loggedin:
        return RedirectResponse(url="/ohoh?msg=沒有正確登入")
    return FileResponse("templates/member.html")

@app.get("/ohoh")
def error(msg: Optional[str] = None):
    return FileResponse("templates/ohoh.html")

@app.post("/api/message")
async def post_message(request: Request):
    try:
        message_header = request.headers
        raw_message_content = await request.json()
        message_content = raw_message_content['content'] # raw_message_content.get('message_content')
        member_id = request.session["member_id"]
        data = (member_id, message_content)
        db_addmsg(data)
        return {"ok": True}
    except:
        return {"error": True}
    
@app.get("/api/message")
def get_message():
    try:
        raw_data = db_readmsg()
        data =[]
        for i in raw_data:
            s = {"name": i[4], "content": i[2], "id":i[0], "member_id":i[1]}
            data.append(s)
        return data
    except:
        return {"error": True}

@app.delete("/api/message/{message_id}")
def del_message(message_id: int, request:Request):
    db_delmsg(message_id)