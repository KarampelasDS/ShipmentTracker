import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc

import models
import schemas
from database import engine, get_db, Base

# Creates tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])


@app.post("/shipments", response_model=schemas.ShipmentOut)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = models.Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@app.get("/shipments", response_model=list[schemas.ShipmentOut])
def list_shipments(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Shipment)
    if status:
        query = query.filter(models.Shipment.status == status)
    return query.order_by(desc(models.Shipment.created_at)).all()


@app.get("/shipments/{shipment_id}", response_model=schemas.ShipmentDetail)
def get_shipment(shipment_id: uuid.UUID, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@app.post("/shipments/{shipment_id}/events", response_model=schemas.StatusEventOut)
def add_status_event(shipment_id: uuid.UUID, event: schemas.StatusEventCreate, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    db_event = models.StatusEvent(shipment_id=shipment_id, **event.model_dump())
    db.add(db_event)

    # cascading update: keep the parent shipment's status in sync
    shipment.status = event.status

    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/shipments/{shipment_id}/events", response_model=list[schemas.StatusEventOut])
def get_shipment_events(shipment_id: uuid.UUID, db: Session = Depends(get_db)):
    return (
        db.query(models.StatusEvent)
        .filter(models.StatusEvent.shipment_id == shipment_id)
        .order_by(models.StatusEvent.occurred_at)
        .all()
    )