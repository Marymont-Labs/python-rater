import json

from rating.services.s3_client import s3
from collections import defaultdict
from datetime import date
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()


BUCKET_NAME = os.getenv("BUCKET_NAME")


def get_loss_cost_multiplier_by_zip(zip_code: str):

    key = "public/common/loss_cost_multiplier_zip/99110365-08bb-42a7-a864-d94ef5d231d3.json"

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    data = json.loads(file_content)

    for row in data:

        if row["zip_text"] == zip_code:
            return row

    return None

def get_default_state_data(state_abbreviation: str):

    key = "public/common/state_quote_defaults/f7d0d91f-7dee-41b7-9508-92e0ddbc93e5.json"

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    data = json.loads(file_content)

    results = []

    for row in data:

        if row["state"] == state_abbreviation:
            results.append(row)

    return results

def get_state_factor_keys():

    results = defaultdict(dict)

    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(
        Bucket=BUCKET_NAME,
        Prefix="public/"
    )

    for page in pages:

        for obj in page.get("Contents", []):

            key = obj["Key"]

            if not key.endswith(".json"):
                continue

            parts = key.split("/")

            # public/MD/age_group/file.json

            if len(parts) < 4:
                continue

            state = parts[1]
            folder_name = parts[2]

            results[state][folder_name] = key

    return dict(results)

def get_naics_data(naics_des: str):

    key = "public/common/naics_product_market/naics_product_market.json"

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    data = json.loads(file_content)

    for row in data:

        if row["naics_description"] == naics_des:
            return row

    return None

def get_vehicle_data(vehicle_type: str):

    key = "public/common/vehicle_type_mapping/ee9f179e-78bf-42cd-b8f0-d85d2dc1b524.json"

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    data = json.loads(file_content)

    for row in data:

        if row["vehicle_item_type"] == vehicle_type:
            return row

    return None

def calculate_age(
    birth_year: int,
    birth_month: int,
    birth_day: int
) -> int:

    today = date.today()

    age = today.year - birth_year

    if (today.month, today.day) < (birth_month, birth_day):
        age -= 1

    return age