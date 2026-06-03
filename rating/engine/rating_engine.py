# rating/engine/rating_engine.py
#
# RatingEngine — top-level orchestrator.
#
# Called from main.py:
#     engine = RatingEngine()
#     result = engine.rate(quote)
#
# Pipeline:
#   For each QuoteVersion (Good / Better / Best):
#     Phase 1 — load_datasets()         : fetch + filter all S3 lookup tables
#     Phase 2 — _rate_all_vehicles()    : for each vehicle, produce all rate parts
#     Phase 3 — _assemble_output()      : build the gbbData response structure
#
# Auto insurance is rated at the vehicle level.
# Each vehicle produces its own set of rate part objects.
# All vehicles on a QuoteVersion share the same Phase 1 datasets.

import asyncio
import logging
from typing import Any, Dict, List
from uuid import uuid4

from rating.models.quote import Quote
from rating.engine.dataset_loader import load_datasets
from rating.engine.vehicle_context import VehicleRatingContext
from rating.engine.rate_parts.loss_cost import (
    fetch_loss_cost_liability_rate,
    fetch_loss_cost_pip_rate,
    fetch_loss_cost_medpay_rate,
    fetch_loss_cost_collision_rate,
    fetch_loss_cost_comprehensive_rate,
    fetch_loss_cost_umbi_rate,
    fetch_loss_cost_uimbi_rate,
)

from rating.engine.rate_parts.loss_cost_umbi import (
    fetch_loss_cost_umbi_rate
)

from rating.engine.rate_parts.loss_cost_uimbi import (
    fetch_loss_cost_uimbi_rate
)

from rating.engine.rate_parts.raca_adjustment import (
    fetch_raca_ocp_liability_rate,
    fetch_raca_ocp_collision_rate,
    fetch_raca_ocp_comprehensive_rate
)

from rating.engine.rate_parts.loss_cost_multiplier import (
    fetch_lcm_liability_rate,
    fetch_lcm_medpay_rate, 
    fetch_lcm_pip_rate, 
    fetch_lcm_um_rate, 
    fetch_lcm_uim_rate,
    fetch_lcm_collision_rate,
    fetch_lcm_comprehensive_rate
)

from rating.engine.rate_parts.policy_tier import (
    fetch_policy_tier_liability_rate, 
    fetch_policy_tier_medpay_rate, 
    fetch_policy_tier_pip_rate, 
    fetch_policy_tier_collision_rate
)

from rating.engine.rate_parts.increased_limits import (
    fetch_increased_limits_liability_rate
)

from rating.engine.rate_parts.class_factors import (
    fetch_class_factor_liability_rate,
    fetch_class_factor_collision_rate,
    fetch_class_factor_comprehensive_rate
)

from rating.engine.rate_parts.age_group import (
    fetch_age_group_liability_rate,
)

from rating.engine.rate_parts.fleet_size import (
    fetch_fleet_size_liability_factor,
    fetch_fleet_size_collision_factor,
    fetch_fleet_size_comprehensive_factor,
)

from rating.engine.rate_parts.naics_factor import (
    fetch_naics_liability_factor,
    fetch_naics_collision_factor,
    fetch_naics_comprehensive_factor,
)

from rating.engine.rate_parts.liability_deductible import (
    fetch_liability_deductible_factor
)

from rating.engine.rate_parts.pd_deductible import (
    fetch_collision_deductible_factor,
    fetch_comprehensive_deductible_factor
)

from rating.engine.rate_parts.truckload_dumping import (
    fetch_dumping_collision_factor
)

from rating.engine.rate_parts.ocn_factor import (
    fetch_ocn_liability_factor,
    fetch_ocn_collision_factor,
    fetch_ocn_comprehensive_factor
)

from rating.engine.rate_parts.rate_category import (
    fetch_rate_category_liability_factor,
    fetch_rate_category_medpay_factor, 
    fetch_rate_category_pip_factor, 
    fetch_rate_category_um_factor,  
    fetch_rate_category_uim_factor, 
    fetch_rate_category_collision_factor, 
    fetch_rate_category_comprehensive_factor,
)

logger = logging.getLogger(__name__)


# ── Rate part fetchers in calculation order ───────────────────────────────────
# This list drives Phase 2. Add new factors here as they are built.
# Each entry is a callable: (VehicleRatingContext) -> dict

RATE_PART_FETCHERS = [
    # ── Row 1: Base Loss Cost ─────────────────────────────────────────────────
    fetch_loss_cost_liability_rate,
    fetch_loss_cost_pip_rate,
    fetch_loss_cost_medpay_rate,
    fetch_loss_cost_collision_rate,
    fetch_loss_cost_comprehensive_rate,
    fetch_loss_cost_umbi_rate,
    fetch_loss_cost_uimbi_rate,

    # ── Row 2: RACA Adjustment Factor ──────────────────────
    # fetch_raca_ocp_liability_rate,
    # fetch_raca_ocp_comprehensive_rate,
    # fetch_raca_ocp_collision_rate,

    # ── Row 3: Loss Cost Multiplier  ─────────────────────────
    # fetch_lcm_liability_rate,
    # fetch_lcm_pip_rate,
    # fetch_lcm_medpay_rate,
    # fetch_lcm_collision_rate,
    # fetch_lcm_comprehensive_rate,
    # fetch_lcm_um_rate,
    # fetch_lcm_uim_rate,

    # ── Row 4: Driver Score / Policy Tier ───────────────────
    # fetch_policy_tier_liability_rate,
    # fetch_policy_tier_pip_rate,
    # fetch_policy_tier_medpay_rate,
    # fetch_policy_tier_collision_rate,

    # ── Row 5: Increased Limits Factor ──────────────────────
    # fetch_increased_limits_liability_rate,

    # ── Row 6: Primary and Secondary Class Factors  ─────────────────────────
    # fetch_class_factor_liability_rate,
    # fetch_class_factor_collision_rate,
    # fetch_class_factor_comprehensive_rate,

    # ── Row 7: Age Group Factor  ─────────────────────────
    # fetch_age_group_liability_rate,

    # ── Row 8: Fleet Size Factor  ─────────────────────────
    # fetch_fleet_size_liability_factor,
    # fetch_fleet_size_collision_factor,
    # fetch_fleet_size_comprehensive_factor,

    # ── Row 9: NAICS Factor  ─────────────────────────
    # fetch_naics_liability_factor,
    # fetch_naics_collision_factor,
    # fetch_naics_comprehensive_factor,

    # ── Row 10: Deductible Factor  ─────────────────────────
    # fetch_liability_deductible_factor,
    # fetch_collision_deductible_factor,
    # fetch_comprehensive_deductible_factor,

    # ── Row 11: Heavy Dumping Factor  ─────────────────────────
    # fetch_dumping_collision_factor,

    # ── Row 12: Original Cost New (OCN) Factor  ─────────────────────────
    # fetch_ocn_liability_factor,
    # fetch_ocn_collision_factor,
    # fetch_ocn_comprehensive_factor,


    # ── Row 13: Rate Category Factor  ─────────────────────────
    # fetch_rate_category_liability_factor,
    # fetch_rate_category_medpay_factor, 
    # fetch_rate_category_pip_factor, 
    # fetch_rate_category_um_factor,  
    # fetch_rate_category_uim_factor, 
    # fetch_rate_category_collision_factor, 
    # fetch_rate_category_comprehensive_factor,
]


class RatingEngine:
    """
    Stateless engine — create once, call rate() per quote.
    """

    def rate(self, quote: Quote) -> List[Dict[str, Any]]:
        """Synchronous entry point for main.py."""
        return asyncio.run(self._rate_async(quote))

    # ── Async pipeline ────────────────────────────────────────────────────────

    async def _rate_async(self, quote: Quote) -> List[Dict[str, Any]]:
        """Rate all QuoteVersions concurrently."""
        version_results = await asyncio.gather(
            *[self._rate_version(qv) for qv in quote.quote_versions]
        )
        return self._build_response(quote, version_results)

    async def _rate_version(self, qv) -> Dict[str, Any]:
        """
        Full pipeline for one QuoteVersion (Good / Better / Best).

        Phase 1: fetch + filter all S3 datasets once for this version.
        Phase 2: for each vehicle, run all rate part fetchers.
        Phase 3: assemble gbbData output.
        """
        logger.info("RatingEngine: rating version '%s' (%s)", qv.quote_version_name, qv.quote_version_id)

        # ── Phase 1: Load datasets ────────────────────────────────────────────
        datasets = await load_datasets(qv)
        logger.debug("RatingEngine: loaded %d datasets for version '%s'",
                     len(datasets), qv.quote_version_name)

        # ── Phase 2: Rate each vehicle ────────────────────────────────────────
        # All vehicles on this version share the same datasets.
        # Each vehicle produces its own list of rate part dicts.
        vehicle_count = len(qv.vehicles)
        all_rate_parts = []

        for vehicle in qv.vehicles:
            ctx = VehicleRatingContext(
                quote_version=qv,
                vehicle=vehicle,
                vehicle_count=vehicle_count,
                datasets=datasets,
            )
            vehicle_rate_parts = self._rate_vehicle(ctx)
            all_rate_parts.extend(vehicle_rate_parts)
            logger.debug(
                "RatingEngine: vehicle %d produced %d rate parts",
                vehicle.vehicle_index, len(vehicle_rate_parts)
            )

        # ── Phase 3: Assemble output ──────────────────────────────────────────
        return {
            "quoteVersionId": qv.quote_version_id,
            "gbbName": qv.quote_version_name,
            "rateVersionKey": qv.quote_version_rate_key,
            "gbbData": [
                [],              # gbbData[0]: premium summaries (added in next step)
                all_rate_parts,  # gbbData[1]: full rate part audit trail
            ]
        }

    def _rate_vehicle(self, ctx: VehicleRatingContext) -> List[dict]:
        """
        Run every rate part fetcher for one vehicle.
        Returns a list of rate part dicts in calculation order.
        Empty dicts {} (inapplicable factors) are included as placeholders.
        """
        rate_parts = []
        for fetcher in RATE_PART_FETCHERS:
            try:
                result = fetcher(ctx)
                rate_parts.append(result)
            except Exception as exc:
                logger.warning(
                    "RatingEngine: %s failed for vehicle %d — %s",
                    fetcher.__name__, ctx.vehicle_index, exc
                )
                rate_parts.append({})
        return rate_parts

    def _build_response(self, quote: Quote, version_results: list) -> List[Dict[str, Any]]:
        """Wrap all version results in the top-level quote envelope."""
        return [
            {
                "quoteId": quote.quote_id,
                "quoteVersionData": version_results,
            }
        ]