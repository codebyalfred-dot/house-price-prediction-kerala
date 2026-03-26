import { formatCurrencyInr, formatCurrencyLakhs, getDeltaLabel } from "../utils/formatters";

function ResultSummary({ prediction, formData }) {
  return (
    <section className="panel result-hero">
      <div>
        <span className="eyebrow">Predicted Property Value</span>
        <h1>{prediction.formatted_price || formatCurrencyLakhs(prediction.predicted_price_lakhs)}</h1>
        <p>{prediction.summary}</p>
      </div>

      <div className="result-metrics">
        <div className="metric-card">
          <span>Estimated in INR</span>
          <strong>{formatCurrencyInr(prediction.predicted_price_inr)}</strong>
        </div>
        <div className="metric-card">
          <span>Market Position</span>
          <strong>{prediction.price_position}</strong>
          <p>{getDeltaLabel(prediction.delta_from_city_average_lakhs)}</p>
        </div>
        <div className="metric-card">
          <span>Configuration</span>
          <strong>
            {formData.bhk} BHK {formData.property_type}
          </strong>
          <p>{formData.area_sqft} sqft</p>
        </div>
      </div>
    </section>
  );
}

export default ResultSummary;

