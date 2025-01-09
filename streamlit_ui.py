import streamlit as st
from data_extractor import fetch_property_data, get_estimated_value_by_zip, extract_zip_code  
from text_generator import generate_property_overview, debug_property_address  


# Streamlit App
st.title("Property Information Viewer")
st.write("Enter the address below to get property information.")

# Input field for property address
property_address = st.text_input("Enter property address:")

if property_address:
    with st.spinner("Fetching property data..."):
        # Fetch property data
        property_data = fetch_property_data(property_address)
    if "error" in property_data:
        st.error(f"Error fetching data: {property_data['message']}")
        
        # Debugging the address
        debug_output = debug_property_address(property_address)
        st.subheader("Debugging Address Issues")
        
        st.markdown(debug_output)
    else:
        # Display property overview
        st.subheader("Property Overview")
        address = property_data.get("address", None)
        st.write(f"**Property Address:** {address}")
        overview = generate_property_overview(property_data)
        st.write(overview)

         # Button to view details
        if st.button("View Detailed Information"):
            st.subheader("Property Details")

            # Status
            status = property_data.get("status", None)
            if status:
                st.write(f"**Status:** {status}")

            # Listing price
            listing_price = property_data.get("listing_price", None)
            if listing_price:
                st.write(f"**Listing Price:** ${listing_price:,.2f}")

            # Days on the Markey
            days_on_market = property_data.get("days_on_market", None)
            if status.lower() == "active" and days_on_market:
                st.write(f"**Days on Market:** ${days_on_market}")

            # Estimated value
            estimated_value = property_data.get("estimated_value", None)
            if estimated_value:
                st.write(f"**Estimated Value:** ${estimated_value:,.2f}")

            # Size
            size = property_data.get("size", None)
            if size:
                st.write(f"**Size:** {size} sq ft")

            # Property Type
            property_type = property_data.get("property_type", None)
            if property_type:
                st.write(f"**Property Type:** {property_type}")

            # County
            county = property_data.get("county", None)
            if county:
                st.write(f"**County:** {county}")

            # School District
            school_district = property_data.get("school_district", None)
            if school_district:
                st.write(f"**School District:** {school_district}")

            # Property features
            property_features = property_data.get("property_features", None)
            garage_spaces = property_features.get("garage", None) if property_features else None
            if property_features:
                st.markdown("### Property Features:")
                feature_mapping = {
                    "beds": "Bedrooms",
                    "full_baths": "Full Bathrooms",
                    "half_baths": "Half Bathrooms",
                    "stories": "Stories",
                    "basement": "Basement",
                    "style": "Style",
                    "new_construction": "New Construction",
                    "year_built": "Year Built",
                    "cooling": "Cooling",
                    "garage": "Garage Spaces",
                }
                for key, label in feature_mapping.items():
                    value = property_features.get(key)
                    if value not in [None, False, '', 0]:
                        st.write(f"- {label}: {value}")

                zip_code = extract_zip_code(address)
                if zip_code:
                    fp1 = 'data/single_home_value_estimate.csv'
                    fp2 = 'data/condos_value_estimate.csv'
                    estimated_value_byZip = get_estimated_value_by_zip(fp1, zip_code)
                    if estimated_value_byZip is not None:
                        st.write(f"**Estimated Single Family Home Value at zip code {zip_code}:** ${estimated_value_byZip:,.2f}")
                    else:
                        st.write("**Estimated Single Family Home Value for this area {zip_code} zip code not availabe")
                    
                    estimated_value_byZip_condo = get_estimated_value_by_zip(fp2, zip_code)
                    if estimated_value_byZip_condo is not None:
                        st.write(f"**Estimated Condo Value at zip code {zip_code}:** ${estimated_value_byZip_condo:,.2f}")
                    else:
                        st.write("**Estimated Condo Value for this area {zip_code} zip code not availabe")


            # Parking features
            parking = property_data.get("parking", None)
            if (
                not garage_spaces
                and parking
                and any(value not in [None, '', 0] for value in parking.values())
            ):
                st.markdown("### Parking Features:")
                for key, value in parking.items():
                    if value not in [None, '', 0]:
                        st.write(f"- {key.replace('_', ' ').title()}: {value}")

            # Interior features
            interior_features = property_data.get("interior_features", None)
            if interior_features:
                st.markdown("### Interior Features:")
                for feature in interior_features:
                    st.write(f"- {feature}")

            # Schools
            schools = property_data.get("schools", None)
            if schools:
                st.markdown("### Nearby Schools:")
                for school in schools:
                    school_name = school.get("name", "Unknown School")
                    school_rating = school.get("rating", "N/A")
                    distance = school.get("distance_in_miles", "N/A")
                    grades = ", ".join(school.get("grades", []))
                    school_type = school.get("funding_type", "N/A").capitalize()

                    st.markdown(f"- **<span style='font-size: 18px;'>{school_name}:</span>**", unsafe_allow_html=True)
                    st.write(f"Rating: {school_rating}, Distance: {distance} miles, Grades: {grades}, Type: {school_type}")