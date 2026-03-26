import { formatCurrencyLakhs } from "../utils/formatters";

function InsightPanel({ prediction, locationInfo }) {
  return (
    <section className="insight-grid">
      <article className="panel">
        <div className="section-heading">
          <span className="eyebrow">Investment Readiness</span>
          <h2>{prediction.investment_score} opportunity</h2>
        </div>
        <div className="score-meter">
          <div className="score-fill" style={{ width: `${prediction.investment_score_value}%` }} />
        </div>
        <div className="stacked-copy">
          <p>Area popularity: {prediction.area_popularity}</p>
          <p>
            City benchmark: {formatCurrencyLakhs(prediction.city_average_price_lakhs)} for a comparable property in{" "}
            {locationInfo.location}
          </p>
          <p>
            Confidence band: {formatCurrencyLakhs(prediction.confidence_band_lakhs.lower)} to{" "}
            {formatCurrencyLakhs(prediction.confidence_band_lakhs.upper)}
          </p>
        </div>
      </article>

      <article className="panel">
        <div className="section-heading">
          <span className="eyebrow">Local Climate Snapshot</span>
          <h2>{locationInfo.weather.condition}</h2>
        </div>
        <div className="weather-grid">
          <div className="metric-card">
            <span>Temperature</span>
            <strong>{locationInfo.weather.temperature_c} C</strong>
          </div>
          <div className="metric-card">
            <span>Humidity</span>
            <strong>{locationInfo.weather.humidity}%</strong>
          </div>
          <div className="metric-card">
            <span>Wind</span>
            <strong>{locationInfo.weather.wind_speed_kph} km/h</strong>
          </div>
          <div className="metric-card">
            <span>Source</span>
            <strong>{locationInfo.weather.source}</strong>
          </div>
        </div>
        <p className="muted-copy">{locationInfo.climate_summary}</p>
      </article>
    </section>
  );
}

export default InsightPanel;

