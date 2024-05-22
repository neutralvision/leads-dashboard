from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Lead, LeadState, LeadCreate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create")
async def root(lead: LeadCreate, db: Session = Depends(get_db)):

    new_lead = Lead(
        FIRST_NAME=lead.FIRST_NAME,
        LAST_NAME=lead.LAST_NAME,
        EMAIL=lead.EMAIL,
        RESUME=lead.RESUME,
        STATE=LeadState.PENDING
    )

    try:
        db.add(new_lead)
        db.commit()
    except Exception as e:
        print("error with /create")
        print(e)
        # TODO: add better error handling, share across apis
        raise HTTPException(status_code=500, detail="Internal Server Error")

    print("successfully added new lead with id: {}".format(new_lead.LEAD_ID))
    return new_lead.LEAD_ID


@app.get("/get")
async def root():
    return "not implemented"


@app.post("/update")
async def root():
    return "not implemented"
