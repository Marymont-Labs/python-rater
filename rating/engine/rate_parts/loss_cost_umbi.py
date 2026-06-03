# rating/engine/rate_parts/loss_cost_umbi.py
#
# Base Loss Cost UMBI rate parts — one function per coverage.
#
# 
# 
# Loss Cost UM Dataset shape (from S3):
#   {
#     "state": "OH",
#     "rate_type": "Base Loss Cost",
#     "source_file": "oh_loss_cost_umbi.csv",
#     "coverage_type": "UMBI",
#     "limit_type": "Single Limits",
#     "coverage_category": "",
#     "coverage_subcategory": "",
#     "coverage_name": "Single Limits UMBI",
#     "rating_classification": "Public Auto",
#     "limit_values": "no coverage",
#     "exposure_count": "0",
#     "umbi_factor": "1",
#     "processed_date_time": "Thu Sep 07 2023 13:23:45 GMT-0400 (Eastern Daylight Time)"
#   },
# 

from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Base Loss Cost"
DATASET_NAME = "Territory Base Loss Cost UMBI"


def _find_loss_cost_umbi_row(
    dataset: list,
    coverage_type: str,
    rating_classification: str,
    umbi_option: str, # matches S3 column: coverage_name
    umbi_limit_value: str, # matches S3 column: limit_values
) -> Optional[dict]:
    
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type
            and row.get("rating_classification") == rating_classification
            and row.get("coverage_name") == umbi_option
            and row.get("limit_values") == umbi_limit_value
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


def fetch_loss_cost_umbi_rate(ctx: VehicleRatingContext) -> dict:
      dataset = ctx.get_dataset(DATASET_NAME)
      row = _find_loss_cost_umbi_row(
        dataset,
        coverage_type ="UMBI",
        rating_classification=ctx.rating_classification,    
        umbi_option=ctx.umbi_option,
        umbi_limit_value=ctx.umbi_limit_value,  
      )
      value = row.get("umbi_factor") if row else None
      return _make_rate_part(ctx, "umbiLossCostRate", "UMBI", value)


