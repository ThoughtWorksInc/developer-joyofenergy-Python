from unittest import TestCase

from src.domain.electricity_reading import ElectricityReading
from src.repository.smart_meter_repository import SmartMeterRepository
from src.domain.smart_meter import SmartMeter


class TestSmartMeterRepository(TestCase):
    def setUp(self):
        self.repository = SmartMeterRepository()

    def test_find_smart_meter_by_id(self):
        smart_meter_id = "smart_meter_0"
        readings = [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ]
        smart_meter = SmartMeter(None, electricity_readings=readings) 
        self.repository.save(smart_meter_id, smart_meter)
        meter = self.repository.find_by_id(smart_meter_id)
        self.assertEqual(smart_meter, meter)