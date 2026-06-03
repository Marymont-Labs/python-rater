# rating/engine/rate_parts/rate_category.py
#
# Rate Category parts — one record has rate_category_factor
# The purpose of this factor is to set a switch (1 or 0) for the differences in states. 
# Some states have PIP or MedPay. Some states have both. Some states combine UM and UIM. Others do not.
# 
# 
# Dataset shape (from S3):
#  {
#     "state": "OH",
#     "rate_type": "Rate Category Factors",
#     "source_file": "oh_rate_category.csv",
#     "coverage_type": "Liability",
#     "coverage_value": "yes",
#     "rate_category_factor": "1",
#     "processed_date_time": "Thu Sep 07 2023 13:26:18 GMT-0400 (Eastern Daylight Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Rate Category Factor"
DATASET_NAME = "Rate Category Factor"


def _find_rate_cateogry_row(
    dataset: list,
    coverage_type: str
) -> Optional[dict]:
   
    if not dataset:
        return None
    for row in dataset:  
      if row.get("coverage_type") == coverage_type:
        return row
    return None


def _make_rate_part(
    ctx: VehicleRatingContext,
    rate_name: str,
    rate_category: str,
    value: Optional[str],
) -> dict:
    """Build the rate part dict. Returns {} if no matching row found."""
    if value is None:
        return {}
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": RATE_PART_CATEGORY,
        "rateName": rate_name,
        "rateCategory": rate_category,
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": value,
    }

def _find(ctx: VehicleRatingContext, coverage_type: str) -> Optional[str]:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_rate_cateogry_row(dataset, coverage_type)
    return row.get("rate_category_factor") if row else None
      


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_rate_category_liability_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "liabilityRateCategoryFactor","Liability",_find(ctx,"Liability"))

def fetch_rate_category_medpay_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "medpayRateCategoryFactor","MedPay",_find(ctx,"MedPay"))

def fetch_rate_category_pip_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "pipRateCategoryFactor","PIP",_find(ctx,"PIP"))

def fetch_rate_category_um_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "umRateCategoryFactor","UMBI",_find(ctx,"UMBI"))

def fetch_rate_category_uim_factor(ctx: VehicleRatingContext) -> dict: 
    return _make_rate_part(ctx, "uimRateCategoryFactor","UIMBI",_find(ctx,"UIMBI"))

def fetch_rate_category_collision_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "collisionRateCategoryFactor","Collision",_find(ctx,"Collision"))

def fetch_rate_category_comprehensive_factor(ctx: VehicleRatingContext) -> dict:
    return _make_rate_part(ctx, "comprehensiveRateCategoryFactor","Comprehensive",_find(ctx,"Comprehensive"))

