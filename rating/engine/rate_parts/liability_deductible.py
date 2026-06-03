# rating/engine/rate_parts/liability_deductible.py
#
# Liability Deductible parts — one record has naics_factor
#
# Pattern (mirrors JS exactly):
#   1. Pull the pre-fetched "Secondary Class and NAICS Factors" dataset from ctx.datasets
#   2. Find the row where naics_code and rating_classification match
#   3. Return a fully-formed rate part dict
#
# Dataset shape (from S3):
# {
#     "state": "OH",
#     "rate_type": "Liability Deductible Factors",
#     "source_file": "oh_liabiity_deductible.csv",
#     "coverage_type": "Liability",
#     "rating_classification": "Trucks And Tractors",
#     "limit_type": "Combined Single Limit",
#     "limit_values": "Full",
#     "liability_deductible_factor": "1",
#     "processed_date_time": "Fri Dec 08 2023 10:19:34 GMT-0500 (Eastern Standard Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Deductible Factor"
DATASET_NAME = "Liability Deductible Factor"


def _find_liability_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    liability_limit_type: str,
    liability_deductible: str

) -> Optional[dict]:
    
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type 
            and row.get("rating_classification") == rating_classification 
            and row.get("limit_type") == liability_limit_type
            and str(row.get("limit_values")) == liability_deductible
        ):
            return row
    return None


def _make_rate_part(
    ctx: VehicleRatingContext,
    # coverage_type: str,
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

def fetch_liability_deductible_factor(ctx: VehicleRatingContext) -> dict:
    dataset = ctx.get_dataset(DATASET_NAME)
    row = _find_liability_row(
        dataset,
        coverage_type="Liability",
        rating_classification=ctx.rating_classification,
        liability_limit_type=ctx.liability_limit_type,
        liability_deductible=ctx.liability_deductible
    )
    value = row.get("liability_deductible_factor") if row else None 
    return _make_rate_part(ctx, "liabilityDeductibleFactor", "Liability",value)

