from http import HTTPStatus
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Path, Query

from ..service.account_service import AccountService
from src.repository.price_plan_repository import PricePlanRepository
from src.repository.smart_meter_repository import SmartMeterRepository
from .models import OPENAPI_EXAMPLES, PricePlanComparisons

router = APIRouter(
    prefix="/price-plans",
    tags=["Price Plan Comparator Controller"],
)


@router.get(
    "/compare-all/{smart_meter_id}",
    response_model=PricePlanComparisons,
    description="Compare prices for all plans for a given meter",
)
def compare(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):
    smart_meter_repository = SmartMeterRepository()
    smart_meter = smart_meter_repository.find_by_id(smart_meter_id)
    price_plan_repository = PricePlanRepository()
    list_of_spend_against_price_plans = price_plan_repository.get_list_of_spend_against_each_price_plan_for(smart_meter)
    if len(list_of_spend_against_price_plans) < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        account_service = AccountService()
        return {
            "pricePlanId": account_service.get_price_plan(smart_meter_id),
            "pricePlanComparisons": list_of_spend_against_price_plans,
        }


@router.get(
    "/recommend/{smart_meter_id}",
    response_model=List[Dict],
    description="View recommended price plans for usage",
)
def recommend(
    smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES),
    limit: int = Query(description="Number of items to return", default=None),
):
    smart_meter_repository = SmartMeterRepository()
    smart_meter = smart_meter_repository.find_by_id(smart_meter_id)
    price_plan_repository = PricePlanRepository()
    list_of_spend_against_price_plans = price_plan_repository.get_list_of_spend_against_each_price_plan_for(
        smart_meter, limit
    )
    return list_of_spend_against_price_plans
