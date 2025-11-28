from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from core.database import get_db
from core.templates import templates
from models.quality_inspections import QualityInspection
from models.quality_results import QualityResult
from services import inspection as svc

router = APIRouter(tags=["inspections"])


@router.get("/orders", response_class=HTMLResponse)
def list_inspection_orders(request: Request, db: Session = Depends(get_db)):
    data = svc.inspection_list_orders(db)

    return templates.TemplateResponse(
        "inspections_list.html",
        {"request": request, **data}
    )


@router.post("/orders")
def create_inspection(
    db: Session = Depends(get_db),
    order_id: str = Form(...),
    product_id: str = Form(...),
    inspection_qty: int = Form(...),
    inspector: str = Form(...),
    inspection_date: str = Form(...),
    status: str = Form(...),
):
    svc.inspection_create_order(db, order_id, product_id, inspection_qty, inspector, inspection_date, status)

    return RedirectResponse(url="/inspections/orders", status_code=303)


@router.get("/result", response_class=HTMLResponse)
def list_inspection_results(request: Request, db: Session = Depends(get_db)):
    # ❗️ 서비스 함수가 폼에 필요한 데이터(inspections, defect_codes)도 반환
    data = svc.inspection_list_result(db) 
    return templates.TemplateResponse(
        "inspections_result.html",
        {"request": request, **data}
    )

@router.post("/result")
def create_inspection_result(
    db: Session = Depends(get_db),
    inspection_id: str = Form(...),
    inspector: str = Form(...),
    passed_qty: int = Form(...),
    defect_qty: int = Form(...),
    defect_code: str = Form(...),
    start_ts: str = Form(...),
    end_ts: str = Form(...),
    notes: str = Form(default=""),
):
    svc.inspection_create_result(
        db=db,
        inspection_id=inspection_id,
        inspector=inspector,
        passed_qty=passed_qty,
        defect_qty=defect_qty,
        defect_code=defect_code,
        start_ts_str=start_ts,
        end_ts_str=end_ts,
        notes=notes
    )
    return RedirectResponse(url="/inspections/result", status_code=303)