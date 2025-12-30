from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import subprocess
import socket

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CODE_SERVER_PORT = 8080
CODE_SERVER_URL = f"http://localhost:{CODE_SERVER_PORT}"
SCRIPT_PATH = "/home/candidate/ui/ui_login/launcher.sh"
RUN_AS_USER = "candidate"

def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False

@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/launch")
def launch(name: str = Form(...)):
    subprocess.Popen(
        ["sudo", "-u", RUN_AS_USER, SCRIPT_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    return RedirectResponse("/starting", status_code=303)

@app.get("/starting", response_class=HTMLResponse)
def starting(request: Request):
    return templates.TemplateResponse("starting.html", {"request": request})

@app.get("/status")
def status():
    if is_port_open("localhost", CODE_SERVER_PORT):
        return {"ready": True, "url": CODE_SERVER_URL}
    return {"ready": False}
