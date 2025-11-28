from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.master_operation import MasterOperation
from models.master_equipment import MasterEquipment
from models.master_product import MasterProduct
from models.master_operation import MasterOperation
from models.master_equipment import MasterEquipment
from models.equipment_sensor_data import EquipmentSensor

from datetime import datetime
from fastapi import Request
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import mean_absolute_error

def create_equipment_sensor_data(request: Request, db:Session, data: dict):
    
    sensor_data = EquipmentSensor(
        equipment_id = data['equipment_id'],
        timestamp = data['timestamp'],
        temperature = data['temperature'],
        vibration = data['vibration'],
        current = data['current'],
        rpm = data['rpm'],
        pressure = data['pressure'],
        
    )
    
    new_sensor_data = predict_sensor_anomaly_detection(request, db, sensor_data)
    
    db.add(new_sensor_data)
    db.commit()
    db.refresh(new_sensor_data)
    return new_sensor_data
    
    
def predict_sensor_anomaly_detection(request: Request, db: Session, sensor_data: EquipmentSensor):
    
    model = request.app.state.ai_models["dnn_sensor_anomaly_detection_model"]
    scaler = request.app.state.ai_models["dnn_sensor_anomaly_detection_scaler"]
    
    df = pd.DataFrame([{
        "temperature": sensor_data.temperature,
        "vibration": sensor_data.vibration,
        "current": sensor_data.current,
        "rpm": sensor_data.rpm,
        "pressure": sensor_data.pressure,
        
    }])
    
    
    features = ['temperature', 'vibration', 'current', 'rpm', 'pressure']
    df_features = df[features].values
    
    features_scaled = scaler.transform(df_features)
    
    predict_anomaly_detection = model.predict(features_scaled)
    loss = mean_absolute_error(predict_anomaly_detection, features_scaled)
    threshold = 0.4353479206647769
    status = loss > threshold
    sensor_data.status = int(status)  # 0: 정상, 1: 이상

    print(predict_anomaly_detection, loss, threshold, sensor_data.status)
        
    return sensor_data
    
def list_equipment_sensor_data(request: Request, db: Session):
    """센서 데이터 목록 조회"""
    q = (
        db.query(
            EquipmentSensor.sensor_id,
            EquipmentSensor.timestamp,
            EquipmentSensor.equipment_id,
            EquipmentSensor.temperature,
            EquipmentSensor.vibration,
            EquipmentSensor.current,
            EquipmentSensor.rpm,
            EquipmentSensor.pressure,
            EquipmentSensor.status,
        )
        .order_by(EquipmentSensor.timestamp.desc())
    )

    rows = q.all()

    # 템플릿에서 쓰기 편하도록 dict 리스트로 변환
    items = []
    for r in rows:
        items.append({
            "sensor_id": r.sensor_id,
            "timestamp": r.timestamp,
            "equipment_id": r.equipment_id,
            "temperature": r.temperature,
            "vibration": r.vibration,
            "current": r.current,
            "rpm": r.rpm,
            "pressure": r.pressure,
            "status": r.status,
        })

    return {
        "items": items,
        "total": len(items),
    }
    