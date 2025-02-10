from src.domain.smart_meter import SmartMeter
from functools import cache


@cache
class SmartMeterRepository:
    def __init__(self):
        self.smart_meters = {}

    def find_by_id(self, meter_id: str):
        return self.smart_meters.get(meter_id)

    def save(self, smart_meter_id: str, meter: SmartMeter):
        self.smart_meters[smart_meter_id] = meter

    def get_all_meters(self) -> list[SmartMeter]:
        return self.smart_meters.values()
