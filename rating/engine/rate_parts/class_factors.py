# rating/engine/rate_parts/class_factors.py
#
# Class Factor parts — liability, collision, and comprehensive rates
#
# The class factor = primary_class_factor + secondary_class_factor (summed)
# This combined value is then multiplied by the other factors in the column
# 
# Primary ClassDataset shape (from S3):
#    "state": "OH",
#    "rate_type": "Primary Class Factor",
#    "source_file": "oh_primary_class.csv",
#    "primary_class_input_dimensions (2).rate_type": "Primary Class Factor",
#    "vehicle_classification": "Public Auto Not Otherwise Classified",
#    "radius_class": "Local (Up To 50 Miles)",
#    "business_use_class": "Service",
#    "fleet_class": "Non-fleet",
#    "class_code": "585",
#    "primaryclass_liab_factor": "0.55",
#    "primaryclass_coll_factor": "1.25",
#    "primaryclass_comp_factor": "1.25",
#    "processed_date_time": "Thu Sep 07 2023 13:24:52 GMT-0400 (Eastern Daylight Time)"
#  },
# Secondary Class / NAICS Dataset shape from s3:
#  {
#     "state": "OH",
#     "rate_type": "NAICS Factor",
#     "source_file": "oh_naics_factor.csv",
#     "coverage_type": "Collision",
#     "naics_code": "111110",
#     "naics_description": "Soybean Farming",
#     "rating_classification": "Trucks And Tractors",
#     "naics_factor": "1",
#     "secondary_factor": "1",
#     "processed_date_time": "Thu Sep 07 2023 13:25:02 GMT-0400 (Eastern Daylight Time)"
#   },
#


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Class Factor"
PRIMARY_DATASET = "Primary Class Factor"
SECONDARY_DATASET = "Secondary Class and NAICS Factors"

# ------Primary Class lookup -------------------------
def _find_primary_class_row(ctx: VehicleRatingContext) -> Optional[dict]:
    dataset = ctx.get_dataset(PRIMARY_DATASET)

    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("vehicle_classification") == ctx.vehicle_classification
            and row.get("radius_class") == ctx.radius_class 
            and row.get("business_use_class") == ctx.business_use_class 
            and row.get("fleet_class").strip() == ctx.fleet_class.strip()
        ):
            return row
    return None

# ---------Secondary class lookup ------------------------
def _find_secondary_class_row(ctx: VehicleRatingContext, coverage_type: str) -> float:
    dataset = ctx.get_dataset(SECONDARY_DATASET)
    if not dataset:
      return 0.0
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type 
            and row.get("rating_classification") == ctx.rating_classification 
            and row.get("naics_code") == ctx.naics_code 
        ):
            return float(row.get("naics_factor",0))
        return 0.0
    
def _combined_factor(primary: float, secondary: float) -> str:
    return str(round(round(primary,3) + round(secondary,3),3))

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

def fetch_class_factor_liability_rate(ctx: VehicleRatingContext) -> dict:
    row = _find_primary_class_row(ctx)
    if not row:
        return {}
    primary = float(row.get("primaryclass_liab_factor",0))
    secondary = _find_secondary_class_row(ctx, "Liability")
    value = _combined_factor(primary, secondary)
    return _make_rate_part(ctx, "liabilityClassFactor","Liability",value)

def fetch_class_factor_collision_rate(ctx: VehicleRatingContext) -> dict:
    row = _find_primary_class_row(ctx)
    if not row:
        return {}
    primary = float(row.get("primaryclass_coll_factor",0))
    secondary = _find_secondary_class_row(ctx, "Collision")
    value = _combined_factor(primary, secondary)
    return _make_rate_part(ctx, "collisionClassFactor","Collision",value)

def fetch_class_factor_comprehensive_rate(ctx: VehicleRatingContext) -> dict:
    row = _find_primary_class_row(ctx)
    if not row:
        return {}
    primary = float(row.get("primaryclass_comp_factor",0))
    secondary = _find_secondary_class_row(ctx, "Comprehensive")
    value = _combined_factor(primary, secondary)
    return _make_rate_part(ctx, "comprehensiveClassFactor","Comprehensive",value)
    