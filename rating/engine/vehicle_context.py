# rating/engine/vehicle_context.py
#
# VehicleRatingContext — the per-vehicle context passed to every rate-part fetcher.
# Wraps a QuoteVersion + specific Vehicle + shared datasets.
#
# This is what every fetch_*_rate(ctx) function receives.
# It exposes both vehicle-level and quote-version-level fields as properties
# so fetchers stay clean: ctx.rating_classification, ctx.liability_lcm, etc.

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from rating.models.quote_version import QuoteVersion
from rating.models.vehicle import Vehicle


@dataclass
class VehicleRatingContext:
    quote_version: QuoteVersion
    vehicle: Vehicle
    vehicle_count: int
    datasets: Dict[str, Any] = field(default_factory=dict)

    # ── Dataset access ────────────────────────────────────────────────────────
    def get_dataset(self, name: str):
        return self.datasets.get(name)

    # ── Vehicle shortcuts ─────────────────────────────────────────────────────
    @property
    def vehicle_index(self) -> int:
        return self.vehicle.vehicle_index

    @property
    def rating_classification(self) -> Optional[str]:
        return self.vehicle.rating_classification

    @property
    def vehicle_item_type(self) -> Optional[str]:
        return self.vehicle.vehicle_item_type

    @property
    def vehicle_category(self) -> Optional[str]:
        return self.vehicle.vehicle_category

    @property
    def vehicle_classification(self) -> Optional[str]:
        return self.vehicle.vehicle_classification

    @property
    def age_group_index(self) -> Optional[str]:
        return self.vehicle.age_group_index

    @property
    def vehicle_value_ocn(self) -> Optional[int]:
        return self.vehicle.vehicle_value_ocn

    @property
    def vehicle_value_stated(self) -> Optional[int]:
        return self.vehicle.vehicle_value_stated
    
    @property
    def liability_limit_type(self) -> Optional[str]:
        return self.vehicle.liability_limit_type

    @property
    def liability_increased_limit(self) -> Optional[str]:
        return self.vehicle.liability_increased_limit

    @property
    def liability_deductible(self) -> Optional[str]:
        return self.vehicle.liability_deductible

    @property
    def comp_limit(self) -> Optional[str]:
        return self.vehicle.comp_limit

    @property
    def comp_peril_option(self) -> Optional[str]:
        return self.vehicle.comp_peril_option

    @property
    def coll_limit(self) -> Optional[str]:
        return self.vehicle.coll_limit

    @property
    def capable_dumping(self) -> Optional[str]:
        return self.vehicle.capable_dumping

    @property
    def has_mechanical_lift(self) -> Optional[str]:
        return self.vehicle.has_mechanical_lift

    @property
    def personal_use(self) -> Optional[str]:
        return self.vehicle.personal_use

    @property
    def is_owner_operated(self) -> Optional[str]:
        return self.vehicle.is_owner_operated

    @property
    def is_operated_by_employees(self) -> Optional[str]:
        return self.vehicle.is_operated_by_employees

    @property
    def is_covered_by_workers_comp(self) -> Optional[str]:
        return self.vehicle.is_covered_by_workers_comp

    @property
    def motorized_vehicle_count(self) -> Optional[str]:
        return self.vehicle.motorized_vehicle_count

    @property
    def operator_license_limit(self) -> Optional[str]:
        return self.vehicle.operator_license_limit

    @property
    def operator_driving_context(self) -> Optional[str]:
        return self.vehicle.operator_driving_context

    @property
    def liability_symbol_relativity(self) -> Optional[str]:
        return self.vehicle.liability_symbol_relativity

    @property
    def comprehensive_symbol_relativity(self) -> Optional[str]:
        return self.vehicle.comprehensive_symbol_relativity

    @property
    def collision_symbol_relativity(self) -> Optional[str]:
        return self.vehicle.collision_symbol_relativity

    @property
    def vehicle_driver_cdl(self) -> Optional[str]:
        return getattr(self.vehicle, "vehicle_driver_cdl", None)

    # ── QuoteVersion shortcuts ────────────────────────────────────────────────
    @property
    def state_abbreviation(self) -> Optional[str]:
        return self.quote_version.state_abbreviation

    @property
    def zip_code(self) -> Optional[str]:
        return self.quote_version.zip_code

    @property
    def naics_code(self) -> Optional[str]:
        return self.quote_version.naics_code

    @property
    def business_use_class(self) -> Optional[str]:
        return self.quote_version.business_use_class

    @property
    def radius_class(self) -> Optional[str]:
        return self.quote_version.radius_class

    @property
    def fleet_class(self) -> Optional[str]:
        return self.quote_version.fleet_class
    
    @property
    def motorized_vehicle_count(self) -> Optional[int]:
        return self.quote_version.motorized_vehicle_count

    @property
    def average_attract_score(self) -> Optional[int]:
        return self.quote_version.average_attract_score

    @property
    def average_driver_points(self) -> Optional[int]:
        return self.quote_version.average_driver_points

    @property
    def average_driver_age(self) -> Optional[int]:
        return self.quote_version.average_driver_age

    @property
    def medpay_option(self) -> Optional[str]:
        return self.quote_version.medpay_options

    @property
    def umbi_option(self) -> Optional[str]:
        return self.quote_version.umbi_option

    @property
    def umbi_limit_value(self) -> Optional[str]:
        return self.quote_version.umbi_limit_value

    @property
    def uimbi_option(self) -> Optional[str]:
        return self.quote_version.uimbi_option

    @property
    def uimbi_limit_value(self) -> Optional[str]:
        return self.quote_version.uimbi_limit_value

    @property
    def paid_in_full_discount(self) -> Optional[str]:
        return self.quote_version.paid_in_full_discount

    @property
    def liability_discretionary_credit(self) -> Optional[str]:
        return self.quote_version.liability_discretionary_credit

    @property
    def comprehensive_discretionary_credit(self) -> Optional[str]:
        return self.quote_version.comprehensive_discretionary_credit

    @property
    def collision_discretionary_credit(self) -> Optional[str]:
        return self.quote_version.collision_discretionary_credit

    @property
    def has_liability(self) -> Optional[str]:
        return self.quote_version.has_liability

    @property
    def has_medpay(self) -> Optional[str]:
        return self.quote_version.has_medpay

    @property
    def has_pip(self) -> Optional[str]:
        return self.quote_version.has_pip

    @property
    def has_um(self) -> Optional[str]:
        return self.quote_version.has_um

    @property
    def has_uim(self) -> Optional[str]:
        return self.quote_version.has_uim

    @property
    def has_comprehensive(self) -> Optional[str]:
        return self.quote_version.has_comprehensive

    @property
    def has_collision(self) -> Optional[str]:
        return self.quote_version.has_collision

    # ── LCM resolution (artisan vs public by rating_classification) ───────────
    @property
    def liability_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_liability_lcm
        return self.quote_version.artisan_liability_lcm

    @property
    def medpay_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_medpay_lcm
        return self.quote_version.artisan_medpay_lcm

    @property
    def pip_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_pip_lcm
        return self.quote_version.artisan_pip_lcm

    @property
    def comprehensive_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_comprehensive_lcm
        return self.quote_version.artisan_comprehensive_lcm

    @property
    def collision_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_collision
        return self.quote_version.artisan_collision_lcm

    @property
    def um_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_um_lcm
        return self.quote_version.artisan_um_lcm

    @property
    def uim_lcm(self) -> Optional[str]:
        if self.rating_classification == "Public Auto":
            return self.quote_version.public_uim_lcm
        return self.quote_version.artisan_uim_lcm