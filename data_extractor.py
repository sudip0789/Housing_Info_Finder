import requests
import re
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = "https://developers.homesage.ai/api/properties/info/"
API_KEY = os.getenv("HOMESAGE_API_KEY")

def fetch_property_data(property_address):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "property_address": property_address
    }

    response = requests.get(API_BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        #print(response.json())

        # Extract necessary details
        address = response.json().get("address", {})
        status = response.json().get("status", {})

        listing_price = response.json().get("listing_price", {})
        dom = response.json().get("dom", {})
        if not dom:
            dom = response.json().get("list_date", {})
            if dom:
                dom = datetime.datetime.strptime(dom, '%Y-%m-%dT%H:%M:%SZ')
                dom  = (datetime.datetime.utcnow() - dom).days
        estimated_value = response.json().get("estimated_value", {})

        home_value = response.json().get("home_value", [])
        if not estimated_value:
          estimated_value = (
              max(home_value, key=lambda x: (int(x["year"]), int(x["month"])))
              if home_value else {}
          )
          estimated_value = estimated_value.get("estimate",{})

        size = response.json().get("sf", {})
        lot = response.json().get("lot", {})
        if not size:
          size = lot.get("lot_acres")
        property_features = response.json().get("property_features", {})
        location_community = response.json().get("location_community", {})
        property_type = location_community.get("property_type", {})
        county = location_community.get("county", {})
        school_district = location_community.get("school_district", {})
        parking = response.json().get("parking", {})
        interior_features = response.json().get("interior_features", [])
        schools = response.json().get("school_ratings", [])

        return {
           "address": address,
            "status": status,
            "listing_price": listing_price,
            "days_on_market": dom,
            "estimated_value": estimated_value,
            "size": size,
            "property_features": property_features,
            "property_type": property_type,
            "county": county,
            "school_district": school_district,
            "parking": parking,
            "interior_features": interior_features,
            "schools": schools
        }
    else:
        return {"error": response.status_code, "message": response.text}
    

def extract_zip_code(address):
    # Refined regex to match ZIP codes 
    zip_code_pattern = r'\b\d{5}(?:-\d{4})?\b(?:(?=\s*$)|(?=,)|(?=\s+[A-Z]{2}))'
    match = re.search(zip_code_pattern, address)
    if match:
        # Extract only the first 5 digits of the ZIP code
        zip_code = match.group(0)[:5]
        return zip_code
    else:
        print("No ZIP code found.")
        return None
    
def get_estimated_value_by_zip(file_path, zip_code):
    df = pd.read_csv(file_path)
    # RegionName and zip_code are of the same type
    df['RegionName'] = df['RegionName'].astype(str) 
    zip_code = str(zip_code)  
    
    # Filter the DataFrame
    filtered_df = df[df['RegionName'] == zip_code]
    if filtered_df.empty:
        return None
    else: 
        # Get the value from the '2024-11-30' column
        value = filtered_df['2024-11-30'].iloc[0]
        return value