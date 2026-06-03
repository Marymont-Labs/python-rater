from dataclasses import dataclass, field
from typing import List, Optional

from rating.models.vehicle import Vehicle
from rating.models.driver import Driver

# from rating.services.fetchers import (
#     get_loss_cost_multiplier_by_zip
# )


@dataclass
class QuoteVersion:
    quote_version_id: str
    quote_version_name: str
    quote_id: str
    garaging_zip_code: str
    effective_date: str 
    company_name: Optional[str] = None
    street_address: Optional[str] = None 
    business_city: Optional[str] = None 
    business_state: Optional[str] = None 
    business_zip_code: Optional[str] = None
    contact_name: Optional[str] = None 
    contact_first_name: Optional[str] = None 
    contact_last_name: Optional[str] = None 
    contact_email_address: Optional[str] = None 
    billing_is_garaging_zip: Optional[str] = None 
    consent_to_3rd_party_data: Optional[str] = None 
    radius_class: Optional[str] = None 
    years_in_business: Optional[str] = None 
    other_insurance_parties: Optional[str] = None 
    zip_code: Optional[str] = None 
    knockout_indicator: Optional[str] = None 
    area_codes: Optional[str] = None 
    business_structure: Optional[str] = None 
    iso_territory_id: Optional[str] = None 
    artisan_collision_lcm: Optional[str] = None 
    artisan_comprehensive_lcm: Optional[str] = None 
    artisan_liability_lcm: Optional[str] = None 
    artisan_medpay_lcm: Optional[str] = None 
    artisan_pip_lcm: Optional[str] = None 
    artisan_um_lcm: Optional[str] = None 
    artisan_uim_lcm: Optional[str] = None 
    public_collision: Optional[str] = None 
    public_comprehensive_lcm: Optional[str] = None 
    public_liability_lcm: Optional[str] = None 
    public_medpay_lcm: Optional[str] = None 
    public_pip_lcm: Optional[str] = None 
    public_um_lcm: Optional[str] = None 
    public_uim_lcm: Optional[str] = None 
    latitude: Optional[str] = None 
    longitude: Optional[str] = None 
    primary_city: Optional[str] = None 
    state_abbreviation: Optional[str] = None 
    state_name: Optional[str] = None 
    naics_code: Optional[str] = None 
    naics_description: Optional[str] = None 
    naics_group: Optional[str] = None 
    liability_limit: Optional[str] = None 
    deductible: Optional[int] = None 
    vehicle_count: Optional[int] = None
    vehicle_classification: Optional[str] = None 
    vehicle_category: Optional[str] = None 
    rating_classification: Optional[str] = None 
    radius_class: Optional[str] = None
    quote_context: Optional[str] = None 
    business_use_class: Optional[str] = None 
    gbb_quote_version: Optional[str] = None 
    medpay_options: Optional[str] = None 
    liability_increased_limits: Optional[str] = None 
    liability_limit_type: Optional[str] = None 
    liability_deductible: Optional[str] = None 
    liability_discretionary_credit: Optional[str] = None 
    comprehensive_discretionary_credit: Optional[str] = None 
    collision_discretionary_credit: Optional[str] = None 
    umbi_option: Optional[str] = None 
    is_umbi_stacked: Optional[str] = None 
    umbi_limit_value: Optional[str] = None 
    umbi_exposure_count: Optional[str] = None  
    uimbi_option: Optional[str] = None  
    is_uimbi_stacked: Optional[str] = None 
    is_uimbi_selected: Optional[str] = None  
    uimbi_limit_value: Optional[str] = None  
    uimbi_exposure_count: Optional[str] = None  
    paid_in_full_discount: Optional[str] = None   
    fleet_class: Optional[str] = None  
    total_vehicle_count: Optional[str] = None  
    total_driver_count: Optional[str] = None   
    loss_cost_key: Optional[str] = None  
    loss_cost_umbi_key: Optional[str] = None  
    loss_cost_uimbi_key: Optional[str] = None  
    policy_tier_key: Optional[str] = None   
    raca_adjustment_key: Optional[str] = None  
    increased_limit_key: Optional[str] = None  
    primary_class_key: Optional[str] = None  
    secondary_class_key: Optional[str] = None  
    naics_business_class_key: Optional[str] = None  
    fleet_key: Optional[str] = None 
    age_group_key: Optional[str] = None  
    ocn_stated_value_key: Optional[str] = None 
    liability_deductible_key: Optional[str] = None  
    pd_deductible_key: Optional[str] = None  
    driver_history_key: Optional[str] = None  
    private_passenger_key: Optional[str] = None  
    named_insured_key: Optional[str] = None  
    heavy_dumping_key: Optional[str] = None  
    rate_category_key: Optional[str] = None
    state_coverage_option_key: Optional[str] = None 
    state_profile_key: Optional[str] = None  
    state_quote_defaults_key: Optional[str] = None  
    discretionary_credit_key: Optional[str] = None  
    vehicle_type_mapping_key: Optional[str] = None 
    cdpf_vehicle_discovery: Optional[str] = None  
    cdpf_firmo_annual_sales: Optional[str] = None  
    cdpf_firmo_company_name: Optional[str] = None  
    cpdf_firmo_dba: Optional[str] = None  
    cdpf_firmo_establishment_type: Optional[str] = None 
    cdpf_firmo_executive_type: Optional[str] = None  
    cdpf_firmo_fein: Optional[str] = None  
    cdpf_firmo_naics_code: Optional[str] = None  
    cdpf_firmo_naics_description: Optional[str] = None  
    cdpf_firmo_num_employees: Optional[str] = None  
    cdpf_firmo_phone: Optional[str] = None 
    cdpf_firmo_url: Optional[str] = None  
    cdpf_firmo_year_start: Optional[str] = None  
    average_attract_score: Optional[int] = None  
    average_driver_points: Optional[int] = None
    average_driver_age: Optional[int] = None  
    quote_rate_key: Optional[str] = None  
    quote_version_rate_key: Optional[str] = None  
    is_customized: Optional[str] = None  
    rate_category_key: Optional[str] = None 
    has_collision: Optional[str] = None   
    has_comprehensive: Optional[str] = None   
    has_liability: Optional[str] = None  
    has_medpay: Optional[str] = None  
    has_pip: Optional[str] = None  
    has_uim: Optional[str] = None  
    has_um: Optional[str] = None  
    motorized_vehicle_count: Optional[int] = None
    vehicles: List[Vehicle] = field(default_factory=list)
    drivers: List[Driver] = field(default_factory=list)

    def __post_init__(self):
        self.fleet_class = (
            "Fleet" if len(self.vehicles) >= 5 else "Non-fleet"
        )
        self.motorized_vehicle_count = sum(
            1 for vehicle in self.vehicles
            if vehicle.vehicle_is_motorized == "yes"
        )

        if self.drivers: 
            self.average_driver_age = round(
                sum(driver.vehicle_driver_age for driver in self.drivers) 
                / len(self.drivers),
                0
            )
            self.average_driver_points = round(
                sum(driver.driver_points for driver in self.drivers)
                / len(self.drivers),
                0
            )
            self.average_attract_score = round(
                sum(driver.vehicle_driver_attract_score for driver in self.drivers)
                / len(self.drivers),
                0
            )