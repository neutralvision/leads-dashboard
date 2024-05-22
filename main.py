from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Lead, LeadState

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create")
async def root(request: Request, db: Session = Depends(get_db)):
    json_data = await request.json()

    first_name = json_data.get("FIRST_NAME")
    last_name = json_data.get("LAST_NAME")
    email = json_data.get("EMAIL")
    resume = json_data.get("RESUME")

    new_lead = Lead(
        FIRST_NAME=first_name,
        LAST_NAME=last_name,
        EMAIL=email,
        RESUME=resume,
        STATE=LeadState.PENDING
    )
    db.add(new_lead)
    db.commit()


    return "test add lead"


@app.get("/get")
async def root():
    return "not implemented"


@app.post("/update")
async def root():
    return "not implemented"
