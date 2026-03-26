import { useEffect, useState } from "react";

import { getPropertyIllustration } from "../utils/formatters";

function PropertySuggestions({ formData, locationInfo, recommendations }) {
  const fallbackImage = getPropertyIllustration(formData.property_type);
  const [imageSrc, setImageSrc] = useState(locationInfo.hero_image_url || fallbackImage);

  useEffect(() => {
    setImageSrc(locationInfo.hero_image_url || fallbackImage);
  }, [fallbackImage, locationInfo.hero_image_url]);

  return (
    <section className="suggestion-grid">
      <article className="panel image-card">
        <div className="section-heading">
          <span className="eyebrow">Property Inspiration</span>
          <h2>{formData.property_type} visual</h2>
        </div>
        <img
          alt={`${formData.property_type} in ${formData.location}`}
          className="property-image"
          onError={() => setImageSrc(fallbackImage)}
          src={imageSrc}
        />
        <div className="chip-row">
          {locationInfo.area_highlights.map((item) => (
            <span className="chip" key={item}>
              {item}
            </span>
          ))}
        </div>
      </article>

      <article className="panel">
        <div className="section-heading">
          <span className="eyebrow">Property Suggestions</span>
          <h2>Continue your search</h2>
        </div>
        <div className="portal-list">
          {recommendations.portals.map((portal) => (
            <a className="portal-card" href={portal.url} key={portal.name} rel="noreferrer" target="_blank">
              <div>
                <strong>{portal.name}</strong>
                <p>{portal.note}</p>
              </div>
              <span>Open</span>
            </a>
          ))}
        </div>

        <div className="stacked-copy">
          <h3>Suggested localities</h3>
          <p>{recommendations.suggested_localities.join(", ")}</p>
          <h3>Buying tips</h3>
          {recommendations.local_tips.map((tip) => (
            <p key={tip}>{tip}</p>
          ))}
        </div>
      </article>
    </section>
  );
}

export default PropertySuggestions;

