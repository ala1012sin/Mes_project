from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.quality_inspections import QualityInspection
from models.quality_results import QualityResult
from models.master_defect_code import MasterDefectCode
from decimal import Decimal
from models.master_operation import MasterOperation
from models.master_equipment import MasterEquipment
from models.master_product import MasterProduct
from models.master_operation import MasterOperation
from models.master_equipment import MasterEquipment
from models.work_order import WorkOrder
from datetime import datetime



def inspection_list_orders(db: Session):
    """작업지시 목록 조회 (제품 정보 포함)"""
    q = (
        db.query(
            QualityInspection.inspection_id,
            QualityInspection.order_id,
            QualityInspection.product_id,
            QualityInspection.inspection_qty,
            QualityInspection.inspector,
            QualityInspection.inspection_date,
            QualityInspection.status,
            MasterProduct.name
            
        )
        .join(MasterProduct, QualityInspection.product_id == MasterProduct.product_id)
        .order_by(QualityInspection.inspection_date.asc())
    )

    rows = q.all()

    # 템플릿에서 쓰기 편하도록 dict 리스트로 변환
    items = []
    for r in rows:
        items.append({
            "inspection_id": r.inspection_id,
            "order_id": r.order_id,
            "product_id": r.product_id,
            "inspection_qty": r.inspection_qty,
            "inspector": r.inspector,
            "inspection_date": r.inspection_date,
            "status": r.status,
            
        })
    orders_list = db.query(WorkOrder).order_by(WorkOrder.order_id).all()
    products = db.query(MasterProduct).order_by(MasterProduct.product_id).all()

    return {
        "items": items,
        "total": len(items),
        "orders": orders_list,
        "products": products
    }
    
    
def inspection_create_order(db: Session, order_id: str, product_id: str, inspection_qty: int, inspector: str, inspection_date: str, status: str):
    """품질검사 생성 (라우터에서 받은 원시 문자열을 변환/저장)"""
    planned_qty = int(inspection_qty)
    due_dt = datetime.fromisoformat(inspection_date)  # 'YYYY-MM-DDTHH:MM' 형태 지원
    
    order = QualityInspection(
        order_id=order_id,
        product_id=product_id,
        inspection_qty=planned_qty,
        inspector=inspector,
        inspection_date=due_dt,
        status=status,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def inspection_list_result(db: Session):
    """품질검사 결과 목록 조회 (제품 정보 포함)"""
    q = (
        db.query(
            QualityResult.inspection_id,
            QualityResult.inspector,
            QualityResult.passed_qty,
            QualityResult.defect_qty,
            QualityResult.defect_rate,
            QualityResult.defect_code,
            QualityResult.inspection_time,
            QualityResult.notes,
            QualityResult.start_ts, 
            QualityResult.end_ts,
            QualityInspection.product_id,  
            MasterProduct.name
             
        )
        .join(QualityInspection, QualityResult.inspection_id == QualityInspection.inspection_id)
        .join(MasterProduct, QualityInspection.product_id == MasterProduct.product_id)
        .order_by(QualityResult.start_ts.desc()) 
    )

    rows = q.all()

    items = []
    for r in rows:
        items.append({
            "inspection_id": r.inspection_id,
            "product_id": r.product_id,
            "product_name": r.name,
            "inspector": r.inspector,
            "passed_qty": r.passed_qty,
            "defect_qty": r.defect_qty,
            "defect_rate": r.defect_rate,
            "defect_code": r.defect_code,
            "inspection_time": r.inspection_time,
            "notes": r.notes,
            "start_ts": r.start_ts,
            "end_ts": r.end_ts,
        })
        
    products = db.query(MasterProduct).order_by(MasterProduct.product_id).all()
    inspections = db.query(QualityInspection).order_by(QualityInspection.inspection_date.desc()).all()
    defect_codes = db.query(MasterDefectCode).order_by(MasterDefectCode.defect_code).all()

    return {
        "items": items,
        "total": len(items),
        "inspections": inspections, # ❗️ '검사' 드롭다운용
        "defect_codes": defect_codes, # ❗️ '불량코드' 드롭다운용
        "products": products, # ❗️ '제품' 드롭다운용
    }
    
    
def inspection_create_result(
    db: Session,
    inspection_id: str,
    inspector: str,
    passed_qty: int,
    defect_qty: int,
    defect_code: str,
    start_ts_str: str,
    end_ts_str: str,
    notes: str
):
    try:
        start_dt = datetime.fromisoformat(start_ts_str)
        end_dt = datetime.fromisoformat(end_ts_str)
        inspection_time_sec = int((end_dt - start_dt).total_seconds()) 
        if inspection_time_sec < 0:
            raise Exception("종료 시간이 시작 시간보다 빠를 수 없습니다.")
    except ValueError:
        raise Exception("날짜 형식이 올바르지 않습니다.")

    total_qty = passed_qty + defect_qty
    defect_rate = Decimal(0)
    if total_qty > 0:
        defect_rate = (Decimal(defect_qty) / Decimal(total_qty)) * 100

    new_result = QualityResult(
        inspection_id=inspection_id, 
        inspector=inspector,
        passed_qty=passed_qty,
        defect_qty=defect_qty,
        defect_code=defect_code if defect_code else None, 
        defect_rate=defect_rate,
        start_ts=start_dt,
        end_ts=end_dt,
        inspection_time=inspection_time_sec,
        notes=notes
    )
    db.add(new_result)
    
    inspection = db.query(QualityInspection).filter(
        QualityInspection.inspection_id == inspection_id
    ).first()
    if inspection:
        inspection.status = "COMPLETED"
        
    db.commit()
    db.refresh(new_result)
    return new_result