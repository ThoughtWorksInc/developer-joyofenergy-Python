from functools import cache
from src.domain.electricity_reading import ElectricityReading
from src.domain.smart_meter import SmartMeter
from src.service.time_converter import time_elapsed_in_hours
from functools import reduce


def calculate_time_elapsed(readings):
    min_time = min(map(lambda r: r.time, readings))
    max_time = max(map(lambda r: r.time, readings))
    return time_elapsed_in_hours(min_time, max_time)


@cache
class PricePlanRepository:
    def __init__(self):
        self.price_plans = []

    def store(self, new_price_plans):
        self.price_plans += new_price_plans

    def get_price_plans(self):
        return self.price_plans[::]

    def clear(self):
        self.price_plans = []

    def get_list_of_spend_against_each_price_plan_for(self, smart_meter: SmartMeter, limit=None) -> list:
        readings = smart_meter.electricity_readings
        if len(readings) < 1:
            return []

        average = self.calculate_average_reading(readings)
        time_elapsed = calculate_time_elapsed(readings)
        consumed_energy = average / time_elapsed

        price_plan_repository = PricePlanRepository()
        price_plans = price_plan_repository.get_price_plans()

        def cost_from_plan(price_plan):
            cost = {}
            cost[price_plan.name] = consumed_energy * price_plan.unit_rate
            return cost

        list_of_spend = list(map(cost_from_plan, self.cheapest_plans_first(price_plans)))

        return list_of_spend[:limit]

    def cheapest_plans_first(self, price_plans) -> list:
        return list(sorted(price_plans, key=lambda plan: plan.unit_rate))

    def calculate_average_reading(self, readings: ElectricityReading) -> float:
        total = reduce((lambda p, c: p + c), map(lambda r: r.reading, readings), 0)
        return total / len(readings)
