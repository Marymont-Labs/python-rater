import json

def increment_list(upper_limit: int) -> list:
  vehicle_count_list = list(range(1,upper_limit + 1))
  return vehicle_count_list

def multiply_list(this_list) -> float:
  total = 1
  for i in this_list:
    total *= float(i)
  return total

def fetch_all_coverages_result(coverage_results:list) -> dict:
  """
  Sums premiums per vehicle across all already-calculated coverage results.
  Receives the list of coverage dicts (each with rateData) so UMBI/UIMBI
  are already divied by the vehicle count before being summed here
  """
  vehicle_totals = {}

  for coverage in coverage_results:
    for item in coverage["rateData"]:
      idx = item["vehicleIndex"]
      vehicle_totals[idx] = vehicle_totals.get(idx, 0.0) + item["premium"]

  total_rate_data = [
    {"vehicleIndex": idx, "premium": vehicle_totals[idx]}
    for idx in sorted(vehicle_totals.keys())
  ]
  
  return {
    "rateName": "Total Premium",
    "rateData": total_rate_data,
    "rateTotals": sum(vehicle_totals.values())
  }

def fetch_coverage_result(rate_version_data:dict, coverage_name: str):
  coverage_rate_version_data = [r for r in rate_version_data if r["rateCategory"] == coverage_name]
  vehicle_count = coverage_rate_version_data[0]["totalVehicles"]
  vehicle_list = increment_list(vehicle_count)
  coverage_premium_list = []
  coverage_rate_dict: dict 
  for i in vehicle_list:
    filtered_rate_parts = [part for part in coverage_rate_version_data if part["vehicleIndex"] == i]
    temp_list =  [f"{float(item['value']):.3f}" for item in filtered_rate_parts]
    coverage_rate_dict: dict[int,str] = {
      "vehicleIndex": i,
      "rateParts": temp_list
    }
    coverage_premium_list.append(coverage_rate_dict)
  
  vehicle_coverage_premium = []
  for j in coverage_premium_list:
    item_dict: dict[int,str] = {
      "vehicleIndex": int(j["vehicleIndex"]),
      "premium": multiply_list(j["rateParts"]),
    }
    vehicle_coverage_premium.append(item_dict)
  total_coverage_premium = sum(item['premium'] for item in vehicle_coverage_premium)
  coverage_result_dict = {
    "rateName": coverage_name,
    "rateData": vehicle_coverage_premium,
    "rateTotals": total_coverage_premium
  }

  return coverage_result_dict

def fetch_um_uim_coverage_result(rate_version_data:dict, coverage_name: str):
  coverage_rate_version_data = [r for r in rate_version_data if r["rateCategory"] == coverage_name]
  vehicle_count = coverage_rate_version_data[0]["totalVehicles"]
  vehicle_list = increment_list(vehicle_count)
  coverage_premium_list = []
  coverage_rate_dict: dict 
  for i in vehicle_list:
    filtered_rate_parts = [part for part in coverage_rate_version_data if part["vehicleIndex"] == i]
    temp_list =  [f"{float(item['value']):.3f}" for item in filtered_rate_parts]
    coverage_rate_dict: dict[int,str] = {
      "vehicleIndex": i,
      "rateParts": temp_list
    }
    coverage_premium_list.append(coverage_rate_dict)
  
  vehicle_coverage_premium = []
  for j in coverage_premium_list:
    item_dict: dict[int,str] = {
      "vehicleIndex": int(j["vehicleIndex"]),
      "premium": multiply_list(j["rateParts"])/vehicle_count,
    }
    vehicle_coverage_premium.append(item_dict)
  total_coverage_premium = sum(item['premium'] for item in vehicle_coverage_premium)
  
  coverage_result_dict = {
    "rateName": coverage_name,
    "rateData": vehicle_coverage_premium,
    "rateTotals": total_coverage_premium
  }
  
  return coverage_result_dict


def premium_generator(rating_data: dict) -> dict:
  # this will fire once each for quote versions good, better, and best
  
  coverage_results = [
    fetch_coverage_result(rating_data, "Liability"),
    fetch_coverage_result(rating_data, "MedPay"),
    fetch_coverage_result(rating_data, "PIP"),
    fetch_coverage_result(rating_data, "Collision"),
    fetch_coverage_result(rating_data, "Comprehensive"),
    fetch_um_uim_coverage_result(rating_data, "UMBI"),
    fetch_um_uim_coverage_result(rating_data, "UIMBI"),
  ]

  total_premium = fetch_all_coverages_result(coverage_results)

  result = coverage_results + [total_premium]

  # data_json = json.dumps(result, indent=2)
  # print("result data in premium_generator:", data_json)
  return result

