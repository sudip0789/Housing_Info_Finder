from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI GPT model
def generate_property_overview(property_data):
    client = OpenAI(api_key = OPENAI_API_KEY)

    # Construct the prompt using the provided property details
    prompt = f"""
    Generate a brief and engaging property overview based on the following details:
    - Status (don't mention it if it is sold or off market): {property_data.get('status', 'N/A')}
    - Listing Price (mention the price if it is active on the market): {property_data.get('listing_price', 'N/A')}
    - Estimated Value: {property_data.get('estimated_value', 'N/A')}
    - Size: {property_data.get('size', 'N/A')}
    - Features: {property_data.get('property_features', 'N/A')}
    - County: {property_data.get('county', 'N/A')}
    - Property Type: {property_data.get('property_type', 'N/A')}
    - Interior features: {property_data.get('interior_features', 'N/A')}
    - School district: {property_data.get('school_district', 'N/A')}
    Focus on keeping it short, and skip any parameter that is N/A or null.
    """
    # Create a chat completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates property overviews."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )

    # Return the generated content
    return completion.choices[0].message.content.strip()

def debug_property_address(property_address):
    client = OpenAI(api_key = OPENAI_API_KEY)

    prompt = f"""
    Validate the address: "{property_address}". Ensure it follows the format 
    "Street Number Street Name, City, State (abbreviated), Zip Code". 
    Examples of valid formats:
    - 8309 Brookhaven Cir, Discovery Bay, CA 94505
    - 303 S Lakeshore Dr, Lake City, MN 55041

    If valid, confirm or suggest improvements (e.g., remove unit/apt details). 
    If invalid, explain why and suggest corrections. Focus on typos, missing components, 
    or invalid formats. Suggest valid alternatives if possible.
    """

    # Create a chat completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are an address validation and correction expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.7
    )

    # Access the generated content
    return completion.choices[0].message.content.strip()
