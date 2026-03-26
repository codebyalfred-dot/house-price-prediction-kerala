from copy import deepcopy


PROPERTY_IMAGE_URLS = {
    "Apartment": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
    "Villa": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80",
}


CITY_PROFILES = {
    "Kochi": {
        "coordinates": {"lat": 9.9312, "lng": 76.2673},
        "average_price_per_sqft": 6500,
        "growth_rate": 8.8,
        "popularity": "High",
        "climate": {"temp_c": 29.0, "humidity": 80, "summary": "Warm coastal weather with strong rental demand near IT corridors."},
        "highlights": ["Metro-linked neighborhoods", "IT hub demand from Kakkanad", "Strong resale movement near Edappally"],
        "suggested_localities": ["Kakkanad", "Edappally", "Tripunithura"],
        "nearby_facilities": [
            {"name": "Rajagiri Public School", "category": "School", "distance_km": 2.8, "address": "Kakkanad, Kochi"},
            {"name": "Lakeshore Hospital", "category": "Hospital", "distance_km": 4.1, "address": "Nettoor, Kochi"},
            {"name": "Cochin International School", "category": "School", "distance_km": 5.5, "address": "Thrikkakara, Kochi"},
            {"name": "Aster Medcity", "category": "Hospital", "distance_km": 7.4, "address": "Cheranalloor, Kochi"},
        ],
    },
    "Thiruvananthapuram": {
        "coordinates": {"lat": 8.5241, "lng": 76.9366},
        "average_price_per_sqft": 6100,
        "growth_rate": 7.9,
        "popularity": "High",
        "climate": {"temp_c": 28.0, "humidity": 78, "summary": "Stable government-driven market with premium demand near Technopark."},
        "highlights": ["Technopark employment zone", "Airport and bypass access", "Steady villa demand in suburban pockets"],
        "suggested_localities": ["Kazhakkoottam", "Kowdiar", "Pattom"],
        "nearby_facilities": [
            {"name": "Loyola School", "category": "School", "distance_km": 3.0, "address": "Sreekariyam, Thiruvananthapuram"},
            {"name": "KIMSHEALTH", "category": "Hospital", "distance_km": 4.2, "address": "Anayara, Thiruvananthapuram"},
            {"name": "St. Thomas Residential School", "category": "School", "distance_km": 6.4, "address": "Mukkolakkal, Thiruvananthapuram"},
            {"name": "PRS Hospital", "category": "Hospital", "distance_km": 5.8, "address": "Killipalam, Thiruvananthapuram"},
        ],
    },
    "Kozhikode": {
        "coordinates": {"lat": 11.2588, "lng": 75.7804},
        "average_price_per_sqft": 5600,
        "growth_rate": 7.2,
        "popularity": "High",
        "climate": {"temp_c": 28.5, "humidity": 82, "summary": "A vibrant coastal market with consistent end-user demand and education-led growth."},
        "highlights": ["Medical college ecosystem", "Retail and trade activity", "Balanced apartment and villa absorption"],
        "suggested_localities": ["Mavoor Road", "Chevayur", "Feroke"],
        "nearby_facilities": [
            {"name": "Devagiri CMI Public School", "category": "School", "distance_km": 3.7, "address": "Devagiri, Kozhikode"},
            {"name": "Baby Memorial Hospital", "category": "Hospital", "distance_km": 2.9, "address": "Indira Gandhi Road, Kozhikode"},
            {"name": "Silver Hills Public School", "category": "School", "distance_km": 4.6, "address": "Paroppadi, Kozhikode"},
            {"name": "MIMS Hospital", "category": "Hospital", "distance_km": 5.2, "address": "Govindapuram, Kozhikode"},
        ],
    },
    "Thrissur": {
        "coordinates": {"lat": 10.5276, "lng": 76.2144},
        "average_price_per_sqft": 5200,
        "growth_rate": 6.8,
        "popularity": "Medium",
        "climate": {"temp_c": 28.0, "humidity": 77, "summary": "Centrally located city with strong family-home demand and dependable resale activity."},
        "highlights": ["Good rail connectivity", "Steady family market", "Festival city with strong civic infrastructure"],
        "suggested_localities": ["Punkunnam", "Ayyanthole", "Ollur"],
        "nearby_facilities": [
            {"name": "Hari Sri Vidya Nidhi School", "category": "School", "distance_km": 2.5, "address": "Punkunnam, Thrissur"},
            {"name": "Jubilee Mission Medical College", "category": "Hospital", "distance_km": 4.3, "address": "East Fort, Thrissur"},
            {"name": "Chinmaya Vidyalaya", "category": "School", "distance_km": 3.9, "address": "Kolazhy, Thrissur"},
            {"name": "Amala Institute of Medical Sciences", "category": "Hospital", "distance_km": 6.1, "address": "Amalanagar, Thrissur"},
        ],
    },
    "Kollam": {
        "coordinates": {"lat": 8.8932, "lng": 76.6141},
        "average_price_per_sqft": 4700,
        "growth_rate": 6.1,
        "popularity": "Medium",
        "climate": {"temp_c": 29.0, "humidity": 79, "summary": "Affordable coastal market with improving connectivity and practical end-user demand."},
        "highlights": ["NH connectivity", "Affordable coastal lifestyle", "Growing apartment demand close to town"],
        "suggested_localities": ["Kadappakada", "Kottiyam", "Mundakkal"],
        "nearby_facilities": [
            {"name": "The Oxford School", "category": "School", "distance_km": 3.1, "address": "Kalluvathukkal, Kollam"},
            {"name": "Travancore Medical College", "category": "Hospital", "distance_km": 5.4, "address": "Uliyakovil, Kollam"},
            {"name": "Infant Jesus School", "category": "School", "distance_km": 4.7, "address": "Tangasseri, Kollam"},
            {"name": "Upasana Hospital", "category": "Hospital", "distance_km": 2.8, "address": "Kollam Town"},
        ],
    },
    "Kottayam": {
        "coordinates": {"lat": 9.5916, "lng": 76.5222},
        "average_price_per_sqft": 5000,
        "growth_rate": 6.5,
        "popularity": "Medium",
        "climate": {"temp_c": 27.5, "humidity": 76, "summary": "Education and healthcare-led market with resilient premium villa pockets."},
        "highlights": ["Healthcare institutions", "High literacy catchment", "Consistent villa demand from NRI buyers"],
        "suggested_localities": ["Ettumanoor", "Pala", "Nagampadam"],
        "nearby_facilities": [
            {"name": "Good Shepherd Public School", "category": "School", "distance_km": 2.2, "address": "Kottayam Town"},
            {"name": "Caritas Hospital", "category": "Hospital", "distance_km": 4.0, "address": "Thellakom, Kottayam"},
            {"name": "Girideepam Bethany School", "category": "School", "distance_km": 5.5, "address": "Vadavathoor, Kottayam"},
            {"name": "Believers Church Medical College Hospital", "category": "Hospital", "distance_km": 7.8, "address": "Thiruvalla Road"},
        ],
    },
    "Kannur": {
        "coordinates": {"lat": 11.8745, "lng": 75.3704},
        "average_price_per_sqft": 4600,
        "growth_rate": 5.9,
        "popularity": "Medium",
        "climate": {"temp_c": 28.2, "humidity": 81, "summary": "Airport spillover and tourism are gradually improving market depth in select zones."},
        "highlights": ["Airport-led catchment", "Growing villa preference", "Coastal and suburban mix of buyers"],
        "suggested_localities": ["Thalassery", "Talap", "Chala"],
        "nearby_facilities": [
            {"name": "St. Michael's Anglo Indian School", "category": "School", "distance_km": 3.6, "address": "Kannur Town"},
            {"name": "Aster MIMS Kannur", "category": "Hospital", "distance_km": 5.1, "address": "Chala, Kannur"},
            {"name": "Ursuline Senior Secondary School", "category": "School", "distance_km": 4.4, "address": "Burnacherry, Kannur"},
            {"name": "AKG Hospital", "category": "Hospital", "distance_km": 6.3, "address": "Talap, Kannur"},
        ],
    },
    "Alappuzha": {
        "coordinates": {"lat": 9.4981, "lng": 76.3388},
        "average_price_per_sqft": 4400,
        "growth_rate": 5.7,
        "popularity": "Medium",
        "climate": {"temp_c": 28.4, "humidity": 83, "summary": "Backwater tourism and retirement demand support a calm, value-driven market."},
        "highlights": ["Tourism belt demand", "Strong lifestyle appeal", "Affordable plotted and villa opportunities"],
        "suggested_localities": ["Cherthala", "Ambalappuzha", "Punnamada"],
        "nearby_facilities": [
            {"name": "St. Joseph's Public School", "category": "School", "distance_km": 3.8, "address": "Alappuzha"},
            {"name": "Sahrudaya Hospital", "category": "Hospital", "distance_km": 2.7, "address": "Alappuzha Town"},
            {"name": "Leo XIII English Medium School", "category": "School", "distance_km": 4.9, "address": "Kalavoor, Alappuzha"},
            {"name": "VSM Hospital", "category": "Hospital", "distance_km": 5.4, "address": "Mavelikara Road"},
        ],
    },
    "Palakkad": {
        "coordinates": {"lat": 10.7867, "lng": 76.6548},
        "average_price_per_sqft": 4200,
        "growth_rate": 5.5,
        "popularity": "Medium",
        "climate": {"temp_c": 30.0, "humidity": 68, "summary": "An affordable inland market with strong value potential and larger plot preferences."},
        "highlights": ["Larger homes at lower entry price", "Industrial corridor potential", "Stable end-user market"],
        "suggested_localities": ["Olavakkode", "Pudussery", "Kalmandapam"],
        "nearby_facilities": [
            {"name": "Bharathamatha School", "category": "School", "distance_km": 2.4, "address": "Palakkad Town"},
            {"name": "Ahalia Foundation Eye Hospital", "category": "Hospital", "distance_km": 6.2, "address": "Kozhippara, Palakkad"},
            {"name": "St. Raphael's School", "category": "School", "distance_km": 4.1, "address": "Palakkad"},
            {"name": "Fort Hospital", "category": "Hospital", "distance_km": 3.6, "address": "West Yakkara, Palakkad"},
        ],
    },
    "Malappuram": {
        "coordinates": {"lat": 11.0732, "lng": 76.0740},
        "average_price_per_sqft": 4300,
        "growth_rate": 5.8,
        "popularity": "Medium",
        "climate": {"temp_c": 28.6, "humidity": 79, "summary": "Growing residential preference fueled by remittance income and family-home demand."},
        "highlights": ["NRI-backed buying interest", "Good value for larger homes", "Steady suburban expansion"],
        "suggested_localities": ["Perinthalmanna", "Kottakkal", "Manjeri"],
        "nearby_facilities": [
            {"name": "MES Central School", "category": "School", "distance_km": 3.3, "address": "Malappuram"},
            {"name": "Moulana Hospital", "category": "Hospital", "distance_km": 4.5, "address": "Perinthalmanna"},
            {"name": "Ideal English School", "category": "School", "distance_km": 5.1, "address": "Kottakkal"},
            {"name": "Almas Hospital", "category": "Hospital", "distance_km": 6.0, "address": "Kottakkal"},
        ],
    },
    "Wayanad": {
        "coordinates": {"lat": 11.6854, "lng": 76.1320},
        "average_price_per_sqft": 3900,
        "growth_rate": 5.2,
        "popularity": "Low",
        "climate": {"temp_c": 24.0, "humidity": 74, "summary": "Cooler climate and tourism appeal make Wayanad attractive for second homes and villas."},
        "highlights": ["Hill-station climate", "Holiday-home potential", "Lower density premium villa market"],
        "suggested_localities": ["Kalpetta", "Sulthan Bathery", "Mananthavady"],
        "nearby_facilities": [
            {"name": "De Paul Public School", "category": "School", "distance_km": 4.6, "address": "Kalpetta, Wayanad"},
            {"name": "DM WIMS Hospital", "category": "Hospital", "distance_km": 7.1, "address": "Meppadi, Wayanad"},
            {"name": "St. Joseph's School", "category": "School", "distance_km": 5.9, "address": "Sulthan Bathery"},
            {"name": "Manipal Hospital", "category": "Hospital", "distance_km": 8.4, "address": "Kalpetta"},
        ],
    },
}


SUPPORTED_LOCATIONS = sorted(CITY_PROFILES.keys())


def get_city_profile(location: str) -> dict:
    profile = CITY_PROFILES.get(location)
    if not profile:
        raise KeyError(f"Unknown location: {location}")
    data = deepcopy(profile)
    data["property_images"] = PROPERTY_IMAGE_URLS.copy()
    return data
