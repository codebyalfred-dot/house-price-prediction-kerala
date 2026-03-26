import { Link } from "react-router-dom";

import HeroSection from "../components/HeroSection";

const featureCards = [
  {
    title: "Accurate price estimation",
    description: "Run an XGBoost-backed valuation using core property details and location-aware features.",
  },
  {
    title: "Real-world decision support",
    description: "Review weather, nearby schools, hospitals, and neighborhood highlights in one place.",
  },
  {
    title: "Market-aware suggestions",
    description: "Compare predicted value to city averages and jump into live property portals for follow-up research.",
  },
];

function HomePage() {
  return (
    <div className="page-stack">
      <HeroSection />

      <section className="feature-grid">
        {featureCards.map((feature) => (
          <article className="panel" key={feature.title}>
            <span className="eyebrow">Feature</span>
            <h2>{feature.title}</h2>
            <p>{feature.description}</p>
          </article>
        ))}
      </section>

      <section className="cta-banner panel panel-elevated">
        <div>
          <span className="eyebrow">Ready to explore a property?</span>
          <h2>Start with a price prediction, then work through the local context.</h2>
        </div>
        <Link className="primary-link" to="/predict">
          Launch Predictor
        </Link>
      </section>
    </div>
  );
}

export default HomePage;

