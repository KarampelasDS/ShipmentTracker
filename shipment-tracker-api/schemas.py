import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class StatusEventCreate(BaseModel):
    status: str
    note: Optional[str] = None

class StatusEventOut(BaseModel):
    id: uuid.UUID
    status: str
    note: Optional[str] = None
    occurred_at: datetime

    class Config:
        from_attributes = True

class ShipmentCreate(BaseModel):
    tracking_number: str
    recipient_name: str
    destination_country: str
    carrier: str

class ShipmentOut(BaseModel):
    id: uuid.UUID
    tracking_number: str
    recipient_name: str
    destination_country: str
    status: str
    carrier: str
    created_at: datetime

    class Config:
        from_attributes = True

class ShipmentDetail(ShipmentOut):
    events: List[StatusEventOut] = []