import logging
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Lead, LeadCreate

app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint for ping tests"""
    return "hello world!"


@app.post("/create")
async def create_leads(lead: LeadCreate, db: Session = Depends(get_db)):
    """Creates a new lead in the database"""

    new_lead = Lead(
        FIRST_NAME=lead.FIRST_NAME,
        LAST_NAME=lead.LAST_NAME,
        EMAIL=lead.EMAIL,
        RESUME=lead.RESUME
    )

    try:
        db.add(new_lead)
        db.commit()
    except Exception as e:
        logging.exception("Error with /create {}".format(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

    logging.info("successfully added new lead with id: {}".format(new_lead.LEAD_ID))
    return new_lead.LEAD_ID


@app.get("/get")
async def get_leads(lead_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Gets a specific lead or all leads from the database, depending on `lead_id`"""

    # query with specific lead_id if provided
    if lead_id is not None:
        lead = db.query(Lead).filter(Lead.LEAD_ID == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead with id {} not found".format(lead_id))
        return [lead]

    # if no lead_id provided, query all
    leads = db.query(Lead).all()
    logging.info("found {} leads for generic /get".format(len(leads)))
    return leads


@app.post("/update")
async def update_leads(lead: LeadCreate, lead_id: int, db: Session = Depends(get_db)):
    """Updates a specific lead in the database"""

    # grab existing entry
    lead_to_update = db.query(Lead).filter(Lead.LEAD_ID == lead_id).first()

    if not lead_to_update:
        raise HTTPException(status_code=404, detail="Lead with id {} not found".format(lead.LEAD_ID))

    # map values that need updating. only resume is optional
    lead_to_update.FIRST_NAME = lead.FIRST_NAME
    lead_to_update.LAST_NAME = lead.LAST_NAME
    lead_to_update.EMAIL = lead.EMAIL
    if lead.RESUME:
        lead_to_update.RESUME = lead.RESUME

    try:
        db.commit()
    except Exception as e:
        logging.error("error with /update with lead_id: {}, {}".format(lead.id, e))
        raise HTTPException(status_code=500, detail="Unknown error with updating lead")

    logging.info("successfully updated lead with id: {}".format(lead_to_update.LEAD_ID))
    return lead_to_update.LEAD_ID

