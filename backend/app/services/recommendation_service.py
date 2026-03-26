from urllib.parse import quote_plus

from app.data.city_profiles import get_city_profile


class RecommendationService:
    def get_recommendations(
        self,
        location: str,
        property_type: str,
        budget_lakhs: float | None = None,
    ) -> dict:
        profile = get_city_profile(location)
        slug_location = quote_plus(f"{location} kerala")
        property_query = quote_plus(property_type.lower())
        budget_note = (
            f"Prioritize listings near INR {budget_lakhs:.0f} lakhs and compare builder premiums."
            if budget_lakhs
            else "Review recent listings and compare them against the system estimate."
        )

        portals = [
            {
                "name": "99acres",
                "url": f"https://www.99acres.com/search/property/buy/{property_query}/{slug_location}",
                "note": "Strong for broker-led city inventory and resale comparisons.",
            },
            {
                "name": "MagicBricks",
                "url": f"https://www.magicbricks.com/property-for-sale/residential-real-estate?keyword={slug_location}",
                "note": "Useful for apartment communities and price trend snapshots.",
            },
            {
                "name": "NoBroker",
                "url": f"https://www.nobroker.in/property/sale/{slug_location}",
                "note": "Helpful for owner-posted listings and quick budget filtering.",
            },
        ]

        local_tips = [
            budget_note,
            f"Check transaction activity in {', '.join(profile['suggested_localities'][:2])} before negotiating.",
            "Ask for waterlogging history, access-road width, and maintenance charges during site visits.",
        ]

        return {
            "location": location,
            "property_type": property_type,
            "budget_lakhs": round(budget_lakhs, 2) if budget_lakhs is not None else None,
            "portals": portals,
            "local_tips": local_tips,
            "suggested_localities": profile["suggested_localities"],
        }


recommendation_service = RecommendationService()
