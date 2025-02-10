from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Path

from .models import OPENAPI_EXAMPLES, ElectricReading, Readings
from src.service.meter_reading_manager import MeterReadingManager
from src.repository.smart_meter_repository import SmartMeterRepository

smart_meter_repository = SmartMeterRepository()
meter_reading_manager = MeterReadingManager(smart_meter_repository)

router = APIRouter(prefix="/readings", tags=["Readings"])


@router.post(
    "/store",
    response_model=ElectricReading,
    description="Store Readings",
)
def store(data: ElectricReading):
    meter_reading_manager.store_reading(data.model_dump(mode="json"))
    return data


@router.get(
    "/read/{smart_meter_id}",
    response_model=List[Readings],
    description="Get Stored Readings",
)
def read(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):
    readings = meter_reading_manager.read_readings(smart_meter_id)
    if len(readings) < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found")
    else:
        return [r.to_json() for r in readings]
