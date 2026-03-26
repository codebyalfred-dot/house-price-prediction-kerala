import { formatCurrencyLakhs, getDeltaLabel } from "../utils/formatters";

function ComparisonCard({ prediction }) {
  return (
    <section className="comparison-grid">
      <article className="panel">
        <div className="section-heading">
          <span className="eyebrow">Price Comparison</span>
          <h2>Against the city average</h2>
        </div>
        <div className="comparison-row">
          <div className="metric-card">
            <span>Predicted price</span>
            <strong>{formatCurrencyLakhs(prediction.predicted_price_lakhs)}</strong>
          </div>
          <div className="metric-card">
            <span>Average city price</span>
            <strong>{formatCurrencyLakhs(prediction.city_average_price_lakhs)}</strong>
          </div>
          <div className="metric-card">
            <span>Difference</span>
            <strong>{getDeltaLabel(prediction.delta_from_city_average_lakhs)}</strong>
          </div>
        </div>
      </article>
    </section>
  );
}

export default ComparisonCard;
