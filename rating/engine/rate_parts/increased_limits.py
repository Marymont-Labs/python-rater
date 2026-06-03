# rating/engine/rate_parts/increased_limits.py
#
# Increased Limits rate parts — one function per coverage. Coverages are Liability
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Increased Limits" dataset from ctx.datasets
#   2. Find the row where rating_classification, vehicle_category, limit_type, and limit_values match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
#     {
#    "state": "OH",
#    "rate_type": "Liability Limit Factors",
#    "source_file": "oh_increased_limits.csv",
#    "coverage_type": "Liability",
#    "rating_classification": "Private Passenger Types",
#    "vehicle_category": "Light Trucks (0 - 10,000 lbs GVWR)",
#    "limit_type": "Combined Single Limit",
#    "limit_values": "25000",
#    "increased_limit_factor": "0.72",
#    "processed_date_time": "Thu Sep 07 2023 13:24:39 GMT-0400 (Eastern Daylight Time)"
#  },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Increased Limit Factor"
DATASET_NAME = "Increased Limit Factor"


def _find_increased_limits_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    vehicle_category: str,
    liability_limit_type: str, # matches S3 column: limit_type
    liability_increased_limit: int # matches S3 column: limit_values
) -> Optional[str]:

    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type
            and row.get("rating_classification") == rating_classification
            and row.get("vehicle_category") == vehicle_category 
            and row.get("limit_type") == liability_limit_type 
            and str(row.get("limit_values")) == str(liability_increased_limit)
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


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_increased_limits_liability_rate(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_increased_limits_row(
        dataset,
        coverage_type = "Liability",
        rating_classification=ctx.rating_classification,
        vehicle_category=ctx.vehicle_category,
        liability_limit_type=ctx.liability_limit_type,
        liability_increased_limit=ctx.liability_increased_limit
        )
    value = str(row.get("increased_limit_factor")) if row else None
      
    return _make_rate_part(ctx, "increasedLimitsLiabilityFactor", "Liability", value)


