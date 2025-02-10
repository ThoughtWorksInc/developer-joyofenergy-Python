from .domain.price_plan import PricePlan
from .generator.electricity_reading_generator import generate_electricity_readings
from .repository.price_plan_repository import PricePlanRepository
from .repository.smart_meter_repository import SmartMeterRepository
from .domain.smart_meter import SmartMeter

DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER = "Dr Evil's Dark Energy"
THE_GREEN_ECO_ENERGY_SUPPLIER = "The Green Eco"
POWER_FOR_EVERYONE_ENERGY_SUPPLIER = "Power for Everyone"

MOST_EVIL_PRICE_PLAN_ID = "price-plan-0"
RENEWBLES_PRICE_PLAN_ID = "price-plan-1"
STANDARD_PRICE_PLAN_ID = "price-plan-2"

def populate_smart_meters_with_readings():
    most_evil_price_plan = PricePlan(MOST_EVIL_PRICE_PLAN_ID, DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER, 10)
    renewbles_price_plan = PricePlan(RENEWBLES_PRICE_PLAN_ID, THE_GREEN_ECO_ENERGY_SUPPLIER, 2)
    standard_price_plan = PricePlan(STANDARD_PRICE_PLAN_ID, POWER_FOR_EVERYONE_ENERGY_SUPPLIER, 1)

    price_plans = [most_evil_price_plan, renewbles_price_plan, standard_price_plan]
    price_plan_repository = PricePlanRepository()
    price_plan_repository.store(price_plans)

    smart_meter_repository: SmartMeterRepository = SmartMeterRepository()
    smart_meter_repository.save("smart-meter-0", SmartMeter(most_evil_price_plan, []))
    smart_meter_repository.save("smart-meter-1", SmartMeter(renewbles_price_plan, generate_electricity_readings(7)))
    smart_meter_repository.save("smart-meter-2", SmartMeter(most_evil_price_plan, generate_electricity_readings(20)))
    smart_meter_repository.save("smart-meter-3", SmartMeter(standard_price_plan, generate_electricity_readings(12)))
    smart_meter_repository.save("smart-meter-4", SmartMeter(renewbles_price_plan, generate_electricity_readings(3)))


def initialize_data():
    populate_smart_meters_with_readings()