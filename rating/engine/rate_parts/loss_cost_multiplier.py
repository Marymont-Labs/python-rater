# rating/engine/rate_parts/loss_cost_multiplier.py
#
# Loss Cost Multiplier rates are read directly from the quote version object
#

from uuid import uuid4
from typing import Optional
from rating.engine.vehicle_context import VehicleRatingContext

RATE_PART_CATEGORY = "Lost Cost Multiplier"
DATASET_NAME = "Lost Cost Multiplier"

# ── One function per coverage ─────────────────────────────────────────────────

def fetch_lcm_liability_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmLiabilityFactor",
        "rateCategory": "Liability",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.liability_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_medpay_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmMedpayFactor",
        "rateCategory": "MedPay",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.medpay_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_pip_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmPipFactor",
        "rateCategory": "PIP",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.pip_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_comprehensive_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmComprehensiveFactor",
        "rateCategory": "Comprehensive",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.comprehensive_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_collision_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmCollisionFactor",
        "rateCategory": "Collision",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.collision_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_um_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmUMFactor",
        "rateCategory": "UMBI",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.um_lcm,   # ← resolved from QuoteVersion directly
    }

def fetch_lcm_uim_rate(ctx: VehicleRatingContext) -> dict:
    return {
        "ratePartId": str(uuid4()),
        "ratePartCategory": "Lost Cost Multiplier",
        "rateName": "lcmUIMFactor",
        "rateCategory": "UIMBI",
        "vehicleIndex": ctx.vehicle_index,
        "totalVehicles": ctx.vehicle_count,
        "ratingClassification": ctx.rating_classification,
        "vehicleItemType": ctx.vehicle_item_type,
        "value": ctx.uim_lcm,   # ← resolved from QuoteVersion directly
    }
