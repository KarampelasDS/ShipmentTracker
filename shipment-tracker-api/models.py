import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_number = Column(String, unique=True, nullable=False)
    recipient_name = Column(String, nullable=False)
    destination_country = Column(String, nullable=False)
    status = Column(String, nullable=False, default="created")
    carrier = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    events = relationship("StatusEvent", order_by="StatusEvent.occurred_at", cascade="all, delete-orphan")



class StatusEvent(Base):
    __tablename__ = "status_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    note = Column(String, nullable=True)
    occurred_at = Column(DateTime, server_default=func.now())