from fastapi import APIRouter, Request, Depends, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from core.database import get_db
from core.templates import templates
from services import equipment as svc


router = APIRouter(tags=["equipment"])

@router.post("/sensor")
def create_equipment_sensor_data(request: Request, db: Session = Depends(get_db), data: dict = Body(...)):
    print(f"장비 ID    : {data['equipment_id']}")
    print(f"타임스탬프 : {data['timestamp']}")
    print(f"온도       : {data['temperature']}")
    print(f"진동       : {data['vibration']}")
    print(f"전류       : {data['current']}")
    print(f"RPM        : {data['rpm']}")
    print(f"압력       : {data['pressure']}")
    
    svc.create_equipment_sensor_data(request, db, data)
    
    return {"status": "sensor data received"}

@router.get("/sensor", response_class=HTMLResponse)
def list_equipment_sensor_data(
    request: Request, db: Session = Depends(get_db)):
    
    # 장비 센서 데이터 목록 조회
    data = svc.list_equipment_sensor_data(request, db)
    return templates.TemplateResponse(
        "equipment_sensor_list.html",
        {"request": request, **data}    
    )