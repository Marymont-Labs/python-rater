# rating/engine/rate_parts/truckload_dumping.py
#
# Truckload Dumping parts — one record has dumping_factor
#
#
# Dataset shape (from S3):
#  {
#     "state": "OH",
#     "rate_type": "Truckload Dumping Factor",
#     "source_file": "oh_truckload_dumping.csv",
#     "coverage_type": "Collision",
#     "rating_classification": "Public Auto",
#     "capable_dumping": "no",
#     "dumping_factor": "1",
#     "processed_date_time": "Thu Sep 07 2023 13:25:48 GMT-0400 (Eastern Daylight Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Truckload Dumping Factor"
DATASET_NAME = "Heavy Dumping Factor"


def _find_truckload_data(
    dataset: list,
    # coverage_type: str,
    rating_classification: str,
    capable_dumping: int

) -> Optional[dict]:
   
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("rating_classification") == rating_classification 
            and row.get("capable_dumping") == capable_dumping
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

def _get_row(ctx: VehicleRatingContext) -> Optional[dict]:
      dataset = ctx.get_dataset(DATASET_NAME)
      return _find_truckload_data(
        dataset,
        rating_classification=ctx.rating_classification,    
        capable_dumping=ctx.capable_dumping 
      )


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_dumping_collision_factor(ctx: VehicleRatingContext) -> dict:
    row = _get_row(ctx)
    value = row.get("dumping_factor") if row else None 
    return _make_rate_part(ctx, "collisionDumpingFactor","Collision",value)

