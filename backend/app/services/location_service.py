from urllib.parse import quote_plus

import httpx

from app.core.config import get_settings
from app.data.city_profiles import get_city_profile


class LocationService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def get_location_info(self, location: str, property_type: str) -> dict:
        profile = get_city_profile(location)
        coordinates = await self._resolve_coordinates(location, profile)
        weather = await self._get_weather(coordinates, profile)
        nearby_facilities = await self._get_nearby_facilities(location, coordinates, profile)
        hero_image_url = profile["property_images"].get(property_type, profile["property_images"]["Apartment"])

        return {
            "location": location,
            "coordinates": coordinates,
            "map_embed_url": (
                f"https://www.google.com/maps?q={coordinates['lat']},{coordinates['lng']}&z=13&output=embed"
            ),
            "weather": weather,
            "nearby_facilities": nearby_facilities,
            "climate_summary": profile["climate"]["summary"],
            "area_highlights": profile["highlights"],
            "hero_image_url": hero_image_url,
            "maps_search_url": f"https://www.google.com/maps/search/{quote_plus(location + ', Kerala')}",
        }

    async def _resolve_coordinates(self, location: str, profile: dict) -> dict:
        if not self.settings.google_maps_api_key:
            return profile["coordinates"]

        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": f"{location}, Kerala, India", "key": self.settings.google_maps_api_key}

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(geocode_url, params=params)
                response.raise_for_status()
            payload = response.json()
            results = payload.get("results", [])
            if results:
                geometry = results[0].get("geometry", {}).get("location", {})
                if "lat" in geometry and "lng" in geometry:
                    return {"lat": geometry["lat"], "lng": geometry["lng"]}
        except Exception:
            pass

        return profile["coordinates"]

    async def _get_weather(self, coordinates: dict, profile: dict) -> dict:
        if not self.settings.openweather_api_key:
            return {
                "temperature_c": profile["climate"]["temp_c"],
                "condition": "Typical seasonal conditions",
                "humidity": profile["climate"]["humidity"],
                "wind_speed_kph": 14.0,
                "source": "Fallback climate profile",
            }

        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": coordinates["lat"],
            "lon": coordinates["lng"],
            "units": "metric",
            "appid": self.settings.openweather_api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(weather_url, params=params)
                response.raise_for_status()
            payload = response.json()
            return {
                "temperature_c": round(payload["main"]["temp"], 1),
                "condition": payload["weather"][0]["description"].title(),
                "humidity": int(payload["main"]["humidity"]),
                "wind_speed_kph": round(float(payload["wind"]["speed"]) * 3.6, 1),
                "source": "OpenWeather",
            }
        except Exception:
            return {
                "temperature_c": profile["climate"]["temp_c"],
                "condition": "Typical seasonal conditions",
                "humidity": profile["climate"]["humidity"],
                "wind_speed_kph": 14.0,
                "source": "Fallback climate profile",
            }

    async def _get_nearby_facilities(self, location: str, coordinates: dict, profile: dict) -> list[dict]:
        if not self.settings.google_maps_api_key:
            return profile["nearby_facilities"]

        place_types = ["school", "hospital"]
        collected: list[dict] = []
        nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                for place_type in place_types:
                    response = await client.get(
                        nearby_url,
                        params={
                            "location": f"{coordinates['lat']},{coordinates['lng']}",
                            "radius": 4000,
                            "type": place_type,
                            "key": self.settings.google_maps_api_key,
                        },
                    )
                    response.raise_for_status()
                    payload = response.json()
                    for entry in payload.get("results", [])[:2]:
                        collected.append(
                            {
                                "name": entry.get("name", f"{place_type.title()} in {location}"),
                                "category": place_type.title(),
                                "distance_km": round(1.5 + len(collected) * 1.1, 1),
                                "address": entry.get("vicinity", f"{location}, Kerala"),
                            }
                        )
            if collected:
                return collected
        except Exception:
            pass

        return profile["nearby_facilities"]


location_service = LocationService()

