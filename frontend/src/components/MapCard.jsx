import { formatDistance } from "../utils/formatters";

function MapCard({ locationInfo }) {
  return (
    <section className="map-layout">
      <article className="panel map-card">
        <div className="section-heading">
          <span className="eyebrow">Location Map</span>
          <h2>{locationInfo.location}</h2>
        </div>
        <div className="map-frame">
          <iframe
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            src={locationInfo.map_embed_url}
            title={`${locationInfo.location} map`}
          />
        </div>
      </article>

      <article className="panel">
        <div className="section-heading">
          <span className="eyebrow">Nearby Facilities</span>
          <h2>Schools and hospitals</h2>
        </div>
        <div className="facility-list">
          {locationInfo.nearby_facilities.map((facility) => (
            <div className="facility-item" key={`${facility.category}-${facility.name}`}>
              <div>
                <strong>{facility.name}</strong>
                <p>
                  {facility.category} - {facility.address}
                </p>
              </div>
              <span>{formatDistance(facility.distance_km)}</span>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}

export default MapCard;
