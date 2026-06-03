# rating/engine/rate_parts/age_group.py
#
# Age Group parts — one record has age_group_factor
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Age Group" dataset from ctx.datasets
#   2. Find the row where rating_classification match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
# {
#     "state": "OH",
#     "rate_type": "Age Group Factor",
#     "source_file": "oh_age_group.csv",
#     "coverage_type": "Liability",
#     "age_group_type": "Original Cost New",
#     "rating_classification": "Private Passenger Types",
#     "age_group_index": "1",
#     "age_group_text": "First Preceding Model Year",
#     "age_group_factor": "0.99",
#     "processed_date_time": "Thu Sep 07 2023 13:25:14 GMT-0400 (Eastern Daylight Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Age Group (Model Year) Factor"
DATASET_NAME = "Age Group (Model Year) Factor"


def _find_age_group_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    age_group_index: int

) -> Optional[dict]:
    """
    Mirror of the JS inner loop:
        if ageGroupObj.rating_classification == 'Private Passenger Types'
    """
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type
            and row.get("rating_classification") == rating_classification 
            and str(row.get("age_group_index")) == str(age_group_index)
        ):
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

# def _get_row(ctx: VehicleRatingContext) -> Optional[dict]:
#       dataset = ctx.get_dataset(DATASET_NAME)
#       return _find_age_group_data(
#         dataset,
#         rating_classification=ctx.rating_classification,    
#         age_group_index=ctx.age_group_index 
#       )
    


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_age_group_liability_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_age_group_row(
        dataset,
        coverage_type ="Liability",
        rating_classification=ctx.rating_classification,    
        age_group_index=ctx.age_group_index 
      )
    value = row.get("age_group_factor") if row else None 
    return _make_rate_part(ctx, "liabilityAgeGroupFactor","Liability",value)
    