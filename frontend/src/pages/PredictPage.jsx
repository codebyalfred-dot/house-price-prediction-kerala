import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../api/client";
import Loader from "../components/Loader";
import PredictionForm from "../components/PredictionForm";
import { useAuth } from "../context/AuthContext";
import { defaultResultFallback } from "../utils/cityData";

const RESULT_STORAGE_KEY = "kerala-house-price-result";

function buildLocationFallback(formData) {
  return {
    location: formData.location,
    coordinates: { lat: 10.0, lng: 76.0 },
    map_embed_url: `https://www.google.com/maps?q=${encodeURIComponent(`${formData.location}, Kerala`)}&z=13&output=embed`,
    weather: defaultResultFallback.weather,
    nearby_facilities: defaultResultFallback.nearby_facilities,
    climate_summary: "Local API data was unavailable, so fallback area information is being shown.",
    area_highlights: defaultResultFallback.area_highlights,
    hero_image_url: "",
  };
}

function buildRecommendationFallback(formData, prediction) {
  return {
    location: formData.location,
    property_type: formData.property_type,
    budget_lakhs: prediction.predicted_price_lakhs,
    portals: [
      {
        name: "99acres",
        url: `https://www.99acres.com/search/property/buy/${encodeURIComponent(formData.property_type.toLowerCase())}/${encodeURIComponent(formData.location + " kerala")}`,
        note: "Fallback property search link generated locally.",
      },
      {
        name: "MagicBricks",
        url: `https://www.magicbricks.com/property-for-sale/residential-real-estate?keyword=${encodeURIComponent(formData.location + " kerala")}`,
        note: "Fallback property search link generated locally.",
      },
    ],
    local_tips: [
      "Use the predicted price as a negotiation baseline.",
      "Compare at least three active listings before shortlisting.",
      "Verify road access, maintenance cost, and flood history.",
    ],
    suggested_localities: defaultResultFallback.suggested_localities,
  };
}

function PredictPage() {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState("");

  async function handlePrediction(payload) {
    setServerError("");
    setLoading(true);

    try {
      const prediction = await api.predict(payload, token);
      const [locationInfoResult, recommendationsResult] = await Promise.allSettled([
        api.getLocationInfo(payload.location, payload.property_type),
        api.getRecommendations(payload.location, payload.property_type, prediction.predicted_price_lakhs),
      ]);

      const bundle = {
        formData: payload,
        prediction,
        locationInfo:
          locationInfoResult.status === "fulfilled"
            ? locationInfoResult.value
            : buildLocationFallback(payload),
        recommendations:
          recommendationsResult.status === "fulfilled"
            ? recommendationsResult.value
            : buildRecommendationFallback(payload, prediction),
      };

      sessionStorage.setItem(RESULT_STORAGE_KEY, JSON.stringify(bundle));
      navigate("/results", { state: bundle });
    } catch (error) {
      setServerError(error.message || "Unable to complete the price prediction.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack">
      <section className="two-column-layout">
        <PredictionForm loading={loading} onSubmit={handlePrediction} serverError={serverError} />

        <aside className="panel helper-panel">
          <span className="eyebrow">How it works</span>
          <h2>From form input to decision-ready insight</h2>
          <p>
            The backend converts your property details into a feature set for the trained model, then layers the
            valuation with city benchmarks, nearby facilities, and location-specific recommendations.
          </p>
          <ul className="plain-list">
            <li>XGBoost valuation with city-aware engineered features</li>
            <li>Weather and place enrichment with API fallback support</li>
            <li>Investment score and market comparison for quick interpretation</li>
          </ul>
          {loading ? <Loader label="Fetching valuation and local insights..." /> : null}
        </aside>
      </section>
    </div>
  );
}

export default PredictPage;

