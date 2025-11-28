from core.database import Base, engine

# 생산관리 마스터
from models import master_product
from models import master_operation
from models import master_operation_standard
from models import master_equipment

# 품질관리 마스터
from models import master_defect_code
from models import master_inspection_item

# 작업지시서 
from models.work_order import WorkOrder

# 생산 실적
from models.work_result import WorkResult

# 품질검사
from models.quality_inspections import QualityInspection
from models.quality_results import QualityResult

# 센서 에러 검출
from models.equipment_sensor_data import EquipmentSensor

# 이미지 분류 활용
from models.master_part import MasterPart
from models.part import Part

def create_tables():
    Base.metadata.create_all(bind=engine)