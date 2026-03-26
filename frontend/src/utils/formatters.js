import apartmentIllustration from "../assets/apartment.svg";
import villaIllustration from "../assets/villa.svg";

export function formatCurrencyLakhs(value) {
  if (value == null || Number.isNaN(Number(value))) {
    return "INR 0";
  }

  const numericValue = Number(value);
  if (numericValue >= 100) {
    return `INR ${(numericValue / 100).toFixed(2)} Cr`;
  }
  return `INR ${numericValue.toFixed(2)} Lakhs`;
}

export function formatCurrencyInr(value) {
  if (value == null || Number.isNaN(Number(value))) {
    return "INR 0";
  }

  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

export function formatDistance(distanceKm) {
  return `${Number(distanceKm).toFixed(1)} km`;
}

export function getPropertyIllustration(propertyType) {
  return propertyType === "Villa" ? villaIllustration : apartmentIllustration;
}

export function getDeltaLabel(deltaLakhs) {
  if (deltaLakhs > 0) {
    return `+${deltaLakhs.toFixed(2)} Lakhs vs city average`;
  }
  return `${deltaLakhs.toFixed(2)} Lakhs vs city average`;
}

