from dataclasses import dataclass
from typing import Optional


@dataclass
class Driver:
    driver_id:  Optional[str] = None 
    quote_id:  Optional[str] = None  
    quote_version_id:  Optional[str] = None  
    driver_index:  Optional[int] = None  
    driver_first_name:  Optional[str] = None 
    driver_last_name:  Optional[str] = None  
    driver_dob_year:  Optional[str] = None  
    driver_dob_month:  Optional[str] = None  
    driver_dob_day:  Optional[str] = None  
    driver_license_number:  Optional[str] = None  
    driver_license_state:  Optional[str] = None  
    clue_driver_first_name:  Optional[str] = None  
    clue_driver_last_name:  Optional[str] = None  
    clue_dob_year:  Optional[str] = None 
    clue_dob_month:  Optional[str] = None  
    clue_dob_day:  Optional[str] = None  
    clue_driver_license_number:  Optional[str] = None 
    clue_driver_license_state:  Optional[str] = None 
    vehicle_driver_age:  Optional[int] = None
    vehicle_driver_attract_score:  Optional[int] = None  
    driver_points:  Optional[int] = None 
    driver_cdl:  Optional[bool] = None 