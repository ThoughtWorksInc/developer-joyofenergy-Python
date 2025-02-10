
from unittest import TestCase

from src.domain.electricity_reading import ElectricityReading
from src.domain.price_plan import PricePlan
from src.repository.price_plan_repository import PricePlanRepository
from src.service.time_converter import iso_format_to_unix_time

class TestPricePlanRepository(TestCase):
    price_plan_repository = PricePlanRepository()


    def test_calculate_costs_against_all_price_plans(self):
        price_plan_repository = PricePlanRepository()
        price_plan_repository.clear()
        price_plan_repository.store(
            [PricePlan("X1", "XS1", 10, []), PricePlan("X2", "XS2", 2, []), PricePlan("X6", "XS6", 1, [])]
        )

        electricity_readings =[
                ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:00:00"), "reading": 0.65}),
                ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:30:00"), "reading": 0.35}),
                ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T10:00:00"), "reading": 0.5}),
        ]
        from src.domain.smart_meter import SmartMeter
        smart_meter = SmartMeter(None, electricity_readings=electricity_readings)
        spend = price_plan_repository.get_list_of_spend_against_each_price_plan_for(smart_meter)    
    
        self.assertEqual(spend[0], {"X6": 0.5})
        self.assertEqual(spend[1], {"X2": 1})
        self.assertEqual(spend[2], {"X1": 5})
