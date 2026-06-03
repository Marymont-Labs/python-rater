# rating/engine/rate_parts/ocn_factor.py
#
# Original Cost New (OCN) / Stated value Factor - Liability, Comprehesive, Collision
#
# 
# Primary ClassDataset shape (from S3):
# {
#     "state": "OH",
#     "rate_type": "Original Cost New Factor",
#     "source_file": "oh_original_cost_new.csv",
#     "coverage_type": "Collision",
#     "rating_classification": "Private Passenger Types",
#     "vehicle_category": "",
#     "ocn_price_low": "0",
#     "ocn_price_high": "999",
#     "ocn_factor_array": "[1.03, 0.95, 0.92, 0.83, 0.78, 0.56, 0.4, 0.31, 0.23, 0.17, 0.15, 0.12, 0.1, 0.08, 0.07, 0.05, 0.04, 0.04, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]",
#     "processed_date_time": "Thu Sep 07 2023 13:25:28 GMT-0400 (Eastern Daylight Time)",
#     "ocn_factor": [
#       "1.03",
#       " 0.95",
#       " 0.92",
#       " 0.83",
#       " 0.78",
#       " 0.56",
#       " 0.4",
#       " 0.31",
#       " 0.23",
#       " 0.17",
#       " 0.15",
#       " 0.12",
#       " 0.1",
#       " 0.08",
#       " 0.07",
#       " 0.05",
#       " 0.04",
#       " 0.04",
#       " 0.03",
#       " 0.02",
#       " 0.02",
#       " 0.02",
#       " 0.01",
#       " 0.01",
#       " 0.01",
#       " 0.01",
#       " 0.01",
#       " 0.01"
#     ] <-- array is indexed by model year
#   },
#
# Two lookup strategies based on rating_classification:
# 
# Public Auto:
#   - Price range matched against vehicle_value_stated
#   - Always uses ocn_factor[0] (no model year indexing)
# 
# All others (Private Passenger Types, Trucks and Tractors, Trailers):
#   - Price range matched against vehicle_value_ocn
#   - Uses ocn_factor[ctx.age_group_index]
#   - Trucks And Tractors and Trailers also match on vehicle_category
# 

from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Original Cost New/Stated Value Factor"
DATASET_NAME = "Original Cost New / Stated Value Factor"

PUBLIC_AUTO = "Public Auto"
PRIVATE_PASSENGER = "Private Passenger Types" 
TRUCKS = "Trucks And Tractors"
TRAILERS = "Trailers"

# -----Core lookup -------------------------
def _find_ocn_row(
        dataset: list,
        coverage_type: str,
        rating_classification: str,
        vehicle_category: str,
        price_value: int
        ) -> Optional[dict]:


    if not dataset:
        return None
    for row in dataset:
        if row.get("coverage_type") != coverage_type:
            continue
        if row.get("rating_classification") != rating_classification:
            continue
        # Trucks and Trailers also filter by vehicle_category
        if coverage_type == "Liability" and rating_classification in (TRUCKS, TRAILERS):
            if row.get("vehicle_category") != vehicle_category:
                continue
        if (
            int(row.get("ocn_price_high",0)) >= price_value
            and int(row.get("ocn_price_low",0)) <= price_value
        ):
            return row
    return None

def _get_factor_value(row: dict, age_group_index: int, rating_classification: str) -> Optional[str]:
  
    ocn_factor = row.get("ocn_factor",[])
    if not ocn_factor:
        return None
    if rating_classification == PUBLIC_AUTO:
        index = 0
    else: 
        index = age_group_index
    # guard against index out of range
    if index >= len(ocn_factor):
        index = len(ocn_factor) - 1
    return str(ocn_factor[index]).strip()

def _find_value(
        ctx: VehicleRatingContext,
        coverage_type: str,
) -> Optional[str]:
    """
    Select the correcct price field and index strategy based on rating_classification, 
    then find the matching row and extract the factor value.
    """
    dataset = ctx.get_dataset(DATASET_NAME)
    rating_classification = ctx.rating_classification

    # Public Auto uses stated value; everyone else uses OCN
    if rating_classification == PUBLIC_AUTO:
        price_value = int(ctx.vehicle_value_stated or 0)
    else:
        price_value = int(ctx.vehicle_value_ocn or 0)

    row = _find_ocn_row(
        dataset,
        coverage_type=coverage_type,
        rating_classification=rating_classification,
        vehicle_category=ctx.vehicle_category,
        price_value=price_value,
    )
    if not row:
        return None
    return _get_factor_value(row, int(ctx.age_group_index or 0),rating_classification)

# -------Shared rate builder

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

def fetch_ocn_liability_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_value(ctx, "Liability")
    return _make_rate_part(ctx,"liabilityOCNFactor","Liability",value)

def fetch_ocn_collision_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_value(ctx, "Collision")
    return _make_rate_part(ctx,"collisionOCNFactor","Collision",value)
    
def fetch_ocn_comprehensive_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_value(ctx, "Comprehensive")
    return _make_rate_part(ctx,"comprehensiveOCNFactor","Comprehensive",value)