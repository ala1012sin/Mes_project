from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, DateTime
from core.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class EquipmentSensor(Base):
    __tablename__ = "equipment_sensor_data"

    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)                 
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)                     
    equipment_id = Column(String(50), ForeignKey("master_equipment.equipment_id"), nullable=False)
    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    rpm = Column(Integer, nullable=False)
    pressure = Column(Float, nullable=False)
    status = Column(Integer, nullable=True)