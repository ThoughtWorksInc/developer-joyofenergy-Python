from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.electricity_reading import ElectricityReading
from src.service.time_converter import iso_format_to_unix_time
from src.repository.smart_meter_repository import SmartMeterRepository
from src.service.meter_reading_manager import MeterReadingManager
from src.domain.smart_meter import SmartMeter


class TestMeterReadingManager(TestCase):
    def setUp(self):
        self.repository = SmartMeterRepository()
        self.repository.save = MagicMock()
        self.meter_reading_manager = MeterReadingManager(self.repository)

    def test_call_repository_to_store_readings(self):
        json = {
            "smartMeterId": "meter-45",
            "electricityReadings": [
                {"time": iso_format_to_unix_time("2015-03-02T08:55:00"), "reading": 0.812},
                {"time": iso_format_to_unix_time("2015-09-02T08:55:00"), "reading": 0.23},
            ],
        }

        self.meter_reading_manager.store_reading(json)

        self.repository.save.assert_called_with(
            "meter-45",
            SmartMeter(None, electricity_readings=[
                ElectricityReading({"time": iso_format_to_unix_time("2015-03-02T08:55:00"), "reading": 0.812}),
                ElectricityReading({"time": iso_format_to_unix_time("2015-09-02T08:55:00"), "reading": 0.23}),
            ]),
        )
