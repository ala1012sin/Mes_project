from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from core.database import Base
import uuid

class QualityInspection(Base):
    __tablename__ = "quality_inspections"

    inspection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True),ForeignKey("work_orders.order_id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("master_products.product_id"), nullable=True)
    inspection_qty = Column(Integer, nullable=False)
    inspector = Column(String(100), nullable=True)
    inspection_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(100), default="PENDING", nullable=False)
    notes = Column(String(500), nullable=True)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    
    
    