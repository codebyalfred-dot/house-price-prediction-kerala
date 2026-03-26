import { useState } from "react";

import { keralaCities } from "../utils/cityData";

const initialFormState = {
  location: "Kochi",
  bhk: "3",
  area_sqft: "1500",
  bathrooms: "3",
  age_of_property: "5",
  floor: "4",
  total_floors: "12",
  parking: "true",
  furnishing: "Semi",
  facing: "East",
  property_type: "Apartment",
};

function PredictionForm({ onSubmit, loading, serverError }) {
  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  }

  function validate(payload) {
    const nextErrors = {};

    if (!payload.location) nextErrors.location = "Please choose a city.";
    if (payload.area_sqft <= 200) nextErrors.area_sqft = "Area should be greater than 200 sqft.";
    if (payload.floor > payload.total_floors) nextErrors.floor = "Floor cannot exceed total floors.";
    if (payload.age_of_property > 80) nextErrors.age_of_property = "Age looks too high.";
    if (payload.bhk < 1 || payload.bhk > 10) nextErrors.bhk = "BHK must stay between 1 and 10.";

    return nextErrors;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const normalizedPayload = {
      ...formData,
      bhk: Number(formData.bhk),
      area_sqft: Number(formData.area_sqft),
      bathrooms: Number(formData.bathrooms),
      age_of_property: Number(formData.age_of_property),
      floor: Number(formData.floor),
      total_floors: Number(formData.total_floors),
      parking: formData.parking === "true",
    };

    const nextErrors = validate(normalizedPayload);
    setErrors(nextErrors);

    if (Object.keys(nextErrors).length > 0) {
      return;
    }

    await onSubmit(normalizedPayload);
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="section-heading">
        <span className="eyebrow">Property Details</span>
        <h2>Run a Kerala property valuation</h2>
      </div>

      <div className="form-grid">
        <label>
          <span>Location</span>
          <select name="location" value={formData.location} onChange={handleChange}>
            {keralaCities.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
          {errors.location ? <small>{errors.location}</small> : null}
        </label>

        <label>
          <span>BHK</span>
          <input min="1" max="10" name="bhk" onChange={handleChange} type="number" value={formData.bhk} />
          {errors.bhk ? <small>{errors.bhk}</small> : null}
        </label>

        <label>
          <span>Area (sqft)</span>
          <input min="200" name="area_sqft" onChange={handleChange} type="number" value={formData.area_sqft} />
          {errors.area_sqft ? <small>{errors.area_sqft}</small> : null}
        </label>

        <label>
          <span>Bathrooms</span>
          <input min="1" max="10" name="bathrooms" onChange={handleChange} type="number" value={formData.bathrooms} />
        </label>

        <label>
          <span>Age of Property</span>
          <input
            min="0"
            max="80"
            name="age_of_property"
            onChange={handleChange}
            type="number"
            value={formData.age_of_property}
          />
          {errors.age_of_property ? <small>{errors.age_of_property}</small> : null}
        </label>

        <label>
          <span>Floor</span>
          <input min="0" max="80" name="floor" onChange={handleChange} type="number" value={formData.floor} />
          {errors.floor ? <small>{errors.floor}</small> : null}
        </label>

        <label>
          <span>Total Floors</span>
          <input
            min="1"
            max="100"
            name="total_floors"
            onChange={handleChange}
            type="number"
            value={formData.total_floors}
          />
        </label>

        <label>
          <span>Parking</span>
          <select name="parking" value={formData.parking} onChange={handleChange}>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </label>

        <label>
          <span>Furnishing</span>
          <select name="furnishing" value={formData.furnishing} onChange={handleChange}>
            <option value="None">None</option>
            <option value="Semi">Semi</option>
            <option value="Full">Full</option>
          </select>
        </label>

        <label>
          <span>Facing</span>
          <select name="facing" value={formData.facing} onChange={handleChange}>
            <option value="East">East</option>
            <option value="West">West</option>
            <option value="North">North</option>
            <option value="South">South</option>
          </select>
        </label>

        <label>
          <span>Property Type</span>
          <select name="property_type" value={formData.property_type} onChange={handleChange}>
            <option value="Apartment">Apartment</option>
            <option value="Villa">Villa</option>
          </select>
        </label>
      </div>

      {serverError ? <div className="error-banner">{serverError}</div> : null}

      <button className="primary-button" disabled={loading} type="submit">
        {loading ? "Predicting..." : "Predict Price"}
      </button>
    </form>
  );
}

export default PredictionForm;

