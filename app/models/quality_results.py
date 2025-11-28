from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from core.database import Base
import uuid

class QualityResult(Base):
    __tablename__ = "quality_results"

    result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inspection_id = Column(UUID(as_uuid=True), ForeignKey("quality_inspections.inspection_id"), nullable=False)
    inspector = Column(String, nullable=False)
    passed_qty = Column(Integer, nullable=False)
    defect_qty = Column(Integer, nullable=False)
    defect_code = Column(String, ForeignKey("master_defect_codes.defect_code"), nullable=True,)
    defect_rate = Column(DECIMAL(5, 2), nullable=True)
    start_ts = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_ts = Column(DateTime, nullable=False, default=datetime.utcnow)
    inspection_time = Column(Integer, nullable=True)  # in seconds
    notes = Column(String(500), nullable=True)