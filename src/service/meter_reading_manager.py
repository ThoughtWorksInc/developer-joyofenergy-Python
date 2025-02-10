from src.domain.electricity_reading import ElectricityReading
from src.repository.smart_meter_repository import SmartMeterRepository
from src.domain.smart_meter import SmartMeter


class MeterReadingManager:
    def __init__(self, smart_meter_repository: SmartMeterRepository):
        self.smart_meter_repository = smart_meter_repository

    def store_reading(self, json):
        smart_meter_id = json["smartMeterId"]
        if smart_meter_id is None:
            raise IllegalArgumentError("Smart meter id must be provided!")
        electricity_readings = list(map(lambda x: ElectricityReading(x), json["electricityReadings"]))
        smart_meter: SmartMeter = self.smart_meter_repository.find_by_id(smart_meter_id)
        if smart_meter:
            smart_meter.add_readings(electricity_readings)
        else:
            meter = SmartMeter(price_plan=None, electricity_readings=electricity_readings)
            self.smart_meter_repository.save(smart_meter_id, meter)

    def read_readings(self, smart_meter_id: str):
        smart_meter: SmartMeter = self.smart_meter_repository.find_by_id(smart_meter_id)
        if smart_meter is None:
            return []
        return smart_meter.electricity_readings


class IllegalArgumentError(ValueError):
    pass
