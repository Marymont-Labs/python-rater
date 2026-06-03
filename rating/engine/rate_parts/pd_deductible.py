# rating/engine/rate_parts/pd_deductible.py
#
# Physical Damange Deductible parts — Comprehensive and Collision
#
#
# Dataset shape (from S3):
#  {
#     "state": "OH",
#     "rate_type": "Physical Damage Deductible Factors",
#     "source_file": "oh_pd_deductible.csv",
#     "coverage_type": "Collision",
#     "rating_classification": "Trucks And Tractors",
#     "perils_type": "All Perils",
#     "limit_values": "2000",
#     "pd_deductible_factor": "0.32",
#     "processed_date_time": "Thu Sep 07 2023 13:25:42 GMT-0400 (Eastern Daylight Time)"
#   },
#
# Comprehensive matches on coverage_type + rating_classification + perils_type + limit_values
# Collision matchs on coverage_type + rating_classification + limit_values ; perils_type is always "All Periles" for collision


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Deductible Factor"
DATASET_NAME = "PD Deductible Factor"


def _find_pd_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    perils_type: str,   # s3 column name
    limit_values: str,  # s3 column name
) -> Optional[dict]:
    
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type 
            and row.get("rating_classification") == rating_classification 
            and row.get("perils_type") == perils_type
            and str(row.get("limit_values")) == str(limit_values)
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

def fetch_comprehensive_deductible_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_pd_row(
        dataset,
        coverage_type="Comprehensive",
        rating_classification=ctx.rating_classification,
        perils_type=ctx.comp_peril_option,
        limit_values=ctx.comp_limit
    )
    value = row.get("pd_deductible_factor") if row else None 
    return _make_rate_part(ctx, "comprehensiveDeductibleFactor", "Comprehensive",value)

def fetch_collision_deductible_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_pd_row(
        dataset,
        coverage_type="Collision",
        rating_classification=ctx.rating_classification,
        perils_type="All Perils",
        limit_values=ctx.coll_limit
    )
    value = row.get("pd_deductible_factor") if row else None 
    return _make_rate_part(ctx, "collisionDeductibleFactor", "Collision",value)

