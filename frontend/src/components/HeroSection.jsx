import { Link } from "react-router-dom";

function HeroSection() {
  return (
    <section className="hero-grid">
      <div className="hero-copy panel panel-elevated">
        <span className="eyebrow">AI valuation for Kerala real estate</span>
        <h1>Estimate house prices with market context, lifestyle insights, and on-ground discovery cues.</h1>
        <p>
          Predict the likely value of apartments and villas across Kerala using an XGBoost-powered backend, then
          explore climate, nearby facilities, and listing recommendations before making your next move.
        </p>
        <div className="hero-actions">
          <Link className="primary-link" to="/predict">
            Start Prediction
          </Link>
          <Link className="ghost-link" to="/signup">
            Create Account
          </Link>
        </div>
      </div>

      <div className="hero-stats panel">
        <div className="stat-card">
          <span>Model</span>
          <strong>XGBoost Regressor</strong>
          <p>Structured for mixed numeric and categorical features.</p>
        </div>
        <div className="stat-card">
          <span>Coverage</span>
          <strong>Kerala Cities</strong>
          <p>Includes valuation context and city-specific benchmarks.</p>
        </div>
        <div className="stat-card">
          <span>Insights</span>
          <strong>Weather + Facilities</strong>
          <p>Builds a richer decision view beyond the predicted price.</p>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;

