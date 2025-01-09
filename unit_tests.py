import unittest
from unittest.mock import patch, Mock
import datetime
import pandas as pd
from io import StringIO

from data_extractor import fetch_property_data, get_estimated_value_by_zip, extract_zip_code  
from text_generator import generate_property_overview, debug_property_address  


class TestDataExtractor(unittest.TestCase):

    @patch("data_extractor.requests.get")
    def test_fetch_property_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "address": "123 Main St, Springfield, IL 62704",
            "status": "Active",
            "listing_price": 250000,
            "dom": None,
            "list_date": "2023-11-01T00:00:00Z",
            "estimated_value": 260000,
            "home_value": [
                {"year": "2023", "month": "10", "estimate": 255000}
            ],
            "sf": 1800,
            "property_features": {"beds": 3, "full_baths": 2},
            "location_community": {"property_type": "Single Family", "county": "Sangamon", "school_district": "District 186"},
            "parking": {"garage": 2},
            "interior_features": ["Hardwood Floors", "Fireplace"],
            "school_ratings": [{"name": "Lincoln Elementary", "rating": 8, "distance_in_miles": 1.2, "grades": ["K", "5"], "funding_type": "Public"}]
        }
        mock_get.return_value = mock_response

        result = fetch_property_data("123 Main St, Springfield, IL 62704")

        self.assertEqual(result["address"], "123 Main St, Springfield, IL 62704")
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["listing_price"], 250000)
        self.assertEqual(result["days_on_market"], (datetime.datetime.utcnow() - datetime.datetime(2023, 11, 1)).days)
        self.assertEqual(result["estimated_value"], 260000)
        self.assertEqual(result["size"], 1800)

    @patch("data_extractor.requests.get")
    def test_fetch_property_data_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Property not found"
        mock_get.return_value = mock_response

        result = fetch_property_data("Invalid Address")

        self.assertEqual(result["error"], 404)
        self.assertEqual(result["message"], "Property not found")

    def test_extract_zip_code(self):
        self.assertEqual(extract_zip_code("123 Main St, Springfield, IL 62704"), "62704")
        self.assertIsNone(extract_zip_code("Invalid Address"))

    def test_get_estimated_value_by_zip(self):
        test_data = pd.DataFrame({
            "RegionName": ["62704", "62703"],
            "2024-11-30": [250000, 230000]
        })
        test_file_path = "test_data.csv"
        test_data.to_csv(test_file_path, index=False)

        result = get_estimated_value_by_zip(test_file_path, "62704")
        self.assertEqual(result, 250000)

        result = get_estimated_value_by_zip(test_file_path, "99999")
        self.assertIsNone(result)

    @patch("text_generator.OpenAI")
    def test_generate_property_overview(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="A beautiful single-family home with 3 bedrooms and 2 baths in Springfield."))]
        )

        property_data = {
            "status": "Active",
            "listing_price": 250000,
            "estimated_value": 260000,
            "size": 1800,
            "property_features": {"beds": 3, "full_baths": 2},
            "county": "Sangamon",
            "property_type": "Single Family",
            "interior_features": ["Hardwood Floors", "Fireplace"],
            "school_district": "District 186"
        }

        result = generate_property_overview(property_data)
        self.assertIn("A beautiful single-family home", result)

    @patch("text_generator.OpenAI")
    def test_debug_property_address(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Address is valid."))]
        )

        result = debug_property_address("123 Main St, Springfield, IL 62704")
        self.assertEqual(result, "Address is valid.")

if __name__ == "__main__":
    unittest.main()