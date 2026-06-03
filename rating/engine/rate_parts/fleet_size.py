# rating/engine/rate_parts/fleet_size.py
#
# Fleet Size factor parts — one function per coverage. Coverages are Liability, Comprehensive, Collision
#
#
# Dataset shape (from S3):
  # {
  #   "state": "OH",
  #   "rate_type": "Fleet Size Factor",
  #   "source_file": "oh_fleet_factor.csv",
  #   "coverage_type": "Collision",
  #   "powered_vehicles_low": "15",
  #   "powered_vehicles_high": "19",
  #   "vehicle_category": "Light Trucks (0 - 10,000 lbs GVWR)",
  #   "rating_classification": "Private Passenger Types",
  #   "business_use_class": "Service",
  #   "fleet_factor": "0.93",
  #   "processed_date_time": "Thu Sep 07 2023 13:25:07 GMT-0400 (Eastern Daylight Time)"
  # },
# One row per coverage_type -- same pattern as policy tier
# motorized_vehicle_count comes from the QuoteVersion (count of motorized vehicles only)
# Trailers are excluded from this count


from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext


RATE_PART_CATEGORY = "Fleet Factor"
DATASET_NAME = "Fleet Factor"


def _find_fleet_size_factor(
    dataset: list,
    coverage_type: str,
    vehicle_category: str,
    rating_classification: str,
    business_use_class: str,
    motorized_vehicle_count: int,
) -> Optional[str]:
    
    if not dataset:
        return None
    for row in dataset:
        if (
            row.get("coverage_type") == coverage_type 
            and row.get("vehicle_category") == vehicle_category
            and row.get("rating_classification") == rating_classification
            and row.get("business_use_class") == business_use_class
            and int(row.get("powered_vehicles_high",0)) >= motorized_vehicle_count
            and int(row.get("powered_vehicles_low",0)) <= motorized_vehicle_count
        ):
            return row.get("fleet_factor")
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

def _find_fleet_factor(ctx: VehicleRatingContext, coverage_type: str) -> Optional[str]:
    """Shared lookup -- passes all required fields to _find_fleet_size_factor"""
    dataset = ctx.get_dataset(DATASET_NAME)
    return _find_fleet_size_factor(
        dataset, 
        coverage_type = coverage_type,
        vehicle_category=ctx.vehicle_category,
        rating_classification=ctx.rating_classification,
        business_use_class=ctx.business_use_class,
        motorized_vehicle_count=ctx.motorized_vehicle_count,
        )


# ── One function per coverage ─────────────────────────────────────────────────

def fetch_fleet_size_liability_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_fleet_factor(ctx,"Liability")
    return _make_rate_part(ctx, "liabilityFleetFactor", "Liability", value)

def fetch_fleet_size_collision_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_fleet_factor(ctx,"Collision")
    return _make_rate_part(ctx, "collisionFleetFactor", "Collision", value)

def fetch_fleet_size_comprehensive_factor(ctx: VehicleRatingContext) -> dict:
    value = _find_fleet_factor(ctx,"Comprehensive")
    return _make_rate_part(ctx, "comprehensiveFleetFactor", "Comprehensive", value)

