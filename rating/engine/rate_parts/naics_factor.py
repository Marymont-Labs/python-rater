# rating/engine/rate_parts/naics_factor.py
#
# NAICS parts — one record has naics_factor
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Secondary Class and NAICS Factors" dataset from ctx.datasets
#   2. Find the row where naics_code and rating_classification match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
# {
#     "state": "OH",
#     "rate_type": "NAICS Factor",
#     "source_file": "oh_naics_factor.csv",
#     "coverage_type": "Collision",
#     "naics_code": "111110",
#     "naics_description": "Soybean Farming",
#     "rating_classification": "Trailers",
#     "naics_factor": "1",
#     "secondary_factor": "1",
#     "processed_date_time": "Thu Sep 07 2023 13:25:02 GMT-0400 (Eastern Daylight Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "NAICS Factor"
DATASET_NAME = "Secondary Class and NAICS Factors"


def _find_naics_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    naics_code: int

) -> Optional[dict]:
    """
    Mirror of the JS inner loop:
        naicsObj.rating_classification == 'Private Passenger Types'
        && naicsObj.naics_code == '111110'
    """
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type 
            and row.get("rating_classification") == rating_classification 
            and row.get("naics_code") == naics_code
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

def fetch_naics_liability_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_naics_row(
        dataset,
        coverage_type="Liability",
        rating_classification=ctx.rating_classification,
        naics_code=ctx.naics_code
    )
    value = row.get("naics_factor") if row else None
    return _make_rate_part(ctx, "liabilityNaicsFactor", "Liability",value)

def fetch_naics_collision_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_naics_row(
        dataset,
        coverage_type="Collision",
        rating_classification=ctx.rating_classification,
        naics_code=ctx.naics_code
    )
    value = row.get("naics_factor") if row else None
    return _make_rate_part(ctx, "collisionNaicsFactor", "Collision",value)

def fetch_naics_comprehensive_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_naics_row(
        dataset,
        coverage_type="Comprehensive",
        rating_classification=ctx.rating_classification,
        naics_code=ctx.naics_code
    )
    value = row.get("naics_factor") if row else None
    return _make_rate_part(ctx, "comprehensiveNaicsFactor", "Comprehensive",value)
