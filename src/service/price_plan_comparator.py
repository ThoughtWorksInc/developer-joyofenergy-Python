from src.repository.price_plan_repository import PricePlanRepository
from src.repository.smart_meter_repository import SmartMeterRepository
from src.domain.smart_meter import SmartMeter

class PricePlanComparator:
    def __init__(self, price_plan_repository: PricePlanRepository, smart_meter_repository: SmartMeterRepository):
        self.smart_meter_repository = smart_meter_repository
        self.price_plan_repository = price_plan_repository

    def recommend_cheapest_price_plans(self, smart_meter_id: int, limit: int = 1) -> list:
        smart_meter: SmartMeter = self.smart_meter_repository.find_by_id(smart_meter_id) 
        if smart_meter is None:
            raise RuntimeError("missing args")
        consumption_for_price_plans = self.price_plan_repository.get_list_of_spend_against_each_price_plan_for(smart_meter, limit)
        return sorted(consumption_for_price_plans)

