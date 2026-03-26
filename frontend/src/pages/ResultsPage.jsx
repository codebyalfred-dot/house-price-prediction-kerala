import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import ComparisonCard from "../components/ComparisonCard";
import InsightPanel from "../components/InsightPanel";
import MapCard from "../components/MapCard";
import PropertySuggestions from "../components/PropertySuggestions";
import ResultSummary from "../components/ResultSummary";

const RESULT_STORAGE_KEY = "kerala-house-price-result";

function ResultsPage() {
  const location = useLocation();
  const [resultBundle, setResultBundle] = useState(location.state || null);

  useEffect(() => {
    if (location.state) {
      setResultBundle(location.state);
      return;
    }

    const rawBundle = sessionStorage.getItem(RESULT_STORAGE_KEY);
    if (!rawBundle) {
      return;
    }

    try {
      setResultBundle(JSON.parse(rawBundle));
    } catch {
      sessionStorage.removeItem(RESULT_STORAGE_KEY);
    }
  }, [location.state]);

  if (!resultBundle) {
    return (
      <section className="panel empty-state">
        <span className="eyebrow">No result loaded</span>
        <h1>Run a prediction to view the full insights dashboard.</h1>
        <p>The latest result is stored in session storage after a successful prediction.</p>
        <Link className="primary-link" to="/predict">
          Go to Prediction Form
        </Link>
      </section>
    );
  }

  const { formData, prediction, locationInfo, recommendations } = resultBundle;

  return (
    <div className="page-stack">
      <ResultSummary formData={formData} prediction={prediction} />
      <ComparisonCard prediction={prediction} />
      <InsightPanel locationInfo={locationInfo} prediction={prediction} />
      <MapCard locationInfo={locationInfo} />
      <PropertySuggestions formData={formData} locationInfo={locationInfo} recommendations={recommendations} />
    </div>
  );
}

export default ResultsPage;

