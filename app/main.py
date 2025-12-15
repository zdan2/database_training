from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from .db import engine, Base, SessionLocal
from .models import Nursery
from .sheets_client import fetch_records
from .import_service import import_nurseries

CREDS_JSON = "app/secrets/service_account.json"
SPREADSHEET_ID = "12DsHjyslvx8Nw5QFayqWFg1tv8ggdCjW1cLxR_tWOjc"
WORKSHEET_TITLE = "シート1"

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

@app.get("/nurseries", response_class=HTMLResponse)
def page(request: Request):
    return templates.TemplateResponse("nurseries/page.html", {"request": request})

@app.get("/nurseries/list", response_class=HTMLResponse)
def list_partial(request: Request):
    with SessionLocal() as db:
        items = list(db.scalars(select(Nursery).order_by(Nursery.source_id)))
    return templates.TemplateResponse("nurseries/_list.html", {"request": request, "items": items})

@app.post("/import/nurseries", response_class=HTMLResponse)
def import_from_sheet(request: Request):
    records = fetch_records(CREDS_JSON, SPREADSHEET_ID, WORKSHEET_TITLE)
    with SessionLocal() as db:
        result = import_nurseries(db, records)
    with SessionLocal() as db:
        items = list(db.scalars(select(Nursery).order_by(Nursery.source_id)))
    return templates.TemplateResponse(
        "nurseries/_import_result_and_list.html",
        {"request": request, "result": result, "items": items},
    )
