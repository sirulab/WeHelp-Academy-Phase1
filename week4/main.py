from fastapi import FastAPI, Path, Query, Body, Request, Form
from typing import Annotated
from fastapi.responses import Response, RedirectResponse, HTMLResponse # Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from hotel_data import get_hotel_data

app =  FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

app.mount("/static", StaticFiles(directory="static"), name="static") 
templates = Jinja2Templates(directory="templates")

url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
data = get_hotel_data(url_ch, url_en)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html") # templates.TemplateResponse(name="index.html", context={"request": request})

@app.post("/login")
def login(request: Request, email: str = Form(""), password: str = Form("")):
    if not email or not password:
        return {"success": False, "msg": "請輸入信箱和密碼"}
    
    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED_IN"] = True
        return {"success": True, "msg": ""}
    else:
        return {"success": False, "msg": "信箱或密碼輸入錯誤"}

@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    is_logged_in = request.session.get("LOGGED_IN", False)
    if not is_logged_in:
        return RedirectResponse("/")
    return templates.TemplateResponse(request=request, name="member.html")

@app.get("/logout")
def logout(request: Request):
    request.session["LOGGED_IN"] = False
    return RedirectResponse("/")

@app.get("/ohoh", response_class=HTMLResponse)
def error(request: Request, msg: str = "發生錯誤"):
    return templates.TemplateResponse(request=request, name="error.html", context={"msg": msg})

@app.get("/hotel/{nr}", response_class=HTMLResponse)
def get_hotel(request: Request, nr: int):
    hotel = []
    for item in data: 
        if item[0] == nr: 
            hotel = {
                "name_ch": item[1],
                "name_en": item[2],
                "phone": item[5]
            }
            break
    return templates.TemplateResponse(request=request, name="hotel.html", context={"hotel": hotel})