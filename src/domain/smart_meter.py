from dataclasses import dataclass
from .price_plan import PricePlan
from .electricity_reading import ElectricityReading


@dataclass
class SmartMeter:
    """Data class contains smart meter details."""

    price_plan: PricePlan
    electricity_readings: list[ElectricityReading]

    def add_readings(self, readings: list[ElectricityReading]):
        self.electricity_readings = readings + self.electricity_readings
