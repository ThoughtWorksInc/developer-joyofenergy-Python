from unittest import TestCase
from unittest.mock import MagicMock

from src.repository.smart_meter_repository import SmartMeterRepository
from src.repository.price_plan_repository import PricePlanRepository
from src.domain.smart_meter import SmartMeter
from src.service.price_plan_comparator import PricePlanComparator


class TestPricePlanComparator(TestCase):
    def setUp(self):
        self.smart_meter_repository = SmartMeterRepository()
        self.price_plan_repository = PricePlanRepository()

    def test_recommend_cheapest_price_plans(self):
        dummy_smart_meter = SmartMeter(None, [])
        self.smart_meter_repository.find_by_id = MagicMock()
        self.smart_meter_repository.find_by_id.return_value = dummy_smart_meter
        self.price_plan_repository.get_list_of_spend_against_each_price_plan_for = MagicMock()

        price_plan_comparator = PricePlanComparator(self.price_plan_repository, self.smart_meter_repository)
        smart_meter_id, limit = "smart-meter-100", 10
        price_plan_comparator.recommend_cheapest_price_plans(smart_meter_id, limit)

        self.smart_meter_repository.find_by_id.assert_called_once_with(smart_meter_id)
        self.price_plan_repository.get_list_of_spend_against_each_price_plan_for.assert_called_once_with(
            dummy_smart_meter, limit
        )
