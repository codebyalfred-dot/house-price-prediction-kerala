const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function humanizeField(field) {
  return field
    .replaceAll("_", " ")
    .replaceAll(".", " ")
    .replace(/\s+/g, " ")
    .trim();
}

function formatDetail(detail) {
  if (!detail) {
    return null;
  }

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => formatDetail(item))
      .filter(Boolean);

    if (messages.length === 0) {
      return null;
    }

    return [...new Set(messages)].join(" | ");
  }

  if (typeof detail === "object") {
    if (typeof detail.msg === "string") {
      const location = Array.isArray(detail.loc)
        ? detail.loc.filter((part) => part !== "body").join(" ")
        : "";
      const prefix = location ? `${humanizeField(location)}: ` : "";
      return `${prefix}${detail.msg}`;
    }

    if (typeof detail.message === "string") {
      return detail.message;
    }
  }

  return null;
}

async function request(path, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };

  if (options.body !== undefined && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const config = {
    ...options,
    headers,
  };

  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, config);
  } catch {
    const frontendOrigin = typeof window !== "undefined" ? window.location.origin : "your frontend origin";
    throw new Error(
      `Unable to reach the backend at ${API_BASE_URL}. Make sure the FastAPI server is running and ALLOWED_ORIGINS includes ${frontendOrigin}.`,
    );
  }

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      formatDetail(payload?.detail) ||
      formatDetail(payload?.message) ||
      (typeof payload === "string" && payload) ||
      "Something went wrong while calling the API.";
    throw new Error(message);
  }

  return payload;
}

export const api = {
  baseUrl: API_BASE_URL,
  getCities: () => request("/cities"),
  predict: (data, token) =>
    request("/predict", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: JSON.stringify(data),
    }),
  getLocationInfo: (location, propertyType) =>
    request(`/location-info?location=${encodeURIComponent(location)}&property_type=${encodeURIComponent(propertyType)}`),
  getRecommendations: (location, propertyType, budgetLakhs) => {
    const params = new URLSearchParams({
      location,
      property_type: propertyType,
    });

    if (budgetLakhs) {
      params.append("budget_lakhs", String(budgetLakhs));
    }

    return request(`/recommendations?${params.toString()}`);
  },
  login: (data) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  signup: (data) =>
    request("/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getMe: (token) =>
    request("/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
};
