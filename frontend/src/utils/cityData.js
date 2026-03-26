export const keralaCities = [
  "Kochi",
  "Thiruvananthapuram",
  "Kozhikode",
  "Thrissur",
  "Kollam",
  "Kottayam",
  "Kannur",
  "Alappuzha",
  "Palakkad",
  "Malappuram",
  "Wayanad",
];

export const defaultResultFallback = {
  weather: {
    temperature_c: 28,
    condition: "Typical seasonal conditions",
    humidity: 78,
    wind_speed_kph: 14,
    source: "Frontend fallback",
  },
  nearby_facilities: [
    { name: "Neighbourhood School", category: "School", distance_km: 3.2, address: "Kerala" },
    { name: "City Care Hospital", category: "Hospital", distance_km: 4.7, address: "Kerala" },
  ],
  area_highlights: ["Stable residential demand", "Access to schools and hospitals", "Strong end-user appeal"],
  suggested_localities: ["Prime Residential Pocket", "Transit-Friendly Zone", "Family-Oriented Layout"],
};
