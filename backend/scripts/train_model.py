import argparse
import json
import re
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.data.city_profiles import CITY_PROFILES  # noqa: E402


RANDOM_SEED = 42
NUM_SAMPLES = 6000
TRAINING_TARGET = "price_lakhs"

CATEGORICAL_FEATURES = ["location", "furnishing", "facing", "property_type"]
NUMERIC_FEATURES = [
    "bhk",
    "area_sqft",
    "bathrooms",
    "age_of_property",
    "floor",
    "total_floors",
    "parking",
    "city_avg_price_per_sqft",
    "floor_ratio",
]

REQUIRED_INPUT_COLUMNS = [
    "location",
    "bhk",
    "area_sqft",
    "bathrooms",
    "age_of_property",
    "floor",
    "total_floors",
    "parking",
    "furnishing",
    "facing",
    "property_type",
]

COLUMN_ALIASES = {
    "location": {"location", "city", "district", "place", "locality"},
    "bhk": {"bhk", "bedroom", "bedrooms", "beds"},
    "area_sqft": {"area_sqft", "area", "sqft", "size_sqft", "super_builtup_area", "builtup_area"},
    "bathrooms": {"bathrooms", "bathroom", "baths", "toilets"},
    "age_of_property": {"age_of_property", "property_age", "age", "building_age"},
    "floor": {"floor", "floor_no", "current_floor"},
    "total_floors": {"total_floors", "total_floor", "building_floors", "floors_total"},
    "parking": {"parking", "has_parking", "car_parking", "parking_available"},
    "furnishing": {"furnishing", "furnishing_status"},
    "facing": {"facing", "direction"},
    "property_type": {"property_type", "property", "home_type", "house_type"},
    "city_avg_price_per_sqft": {"city_avg_price_per_sqft", "avg_price_per_sqft", "market_price_per_sqft"},
    "floor_ratio": {"floor_ratio"},
    TRAINING_TARGET: {"price_lakhs", "price_lakh", "price_in_lakhs", "target", "sale_price", "price"},
}

LOCATION_SYNONYMS = {
    "cochin": "Kochi",
    "trivandrum": "Thiruvananthapuram",
    "calicut": "Kozhikode",
    "alleppey": "Alappuzha",
}

FURNISHING_MAP = {
    "none": "None",
    "unfurnished": "None",
    "semi": "Semi",
    "semi_furnished": "Semi",
    "semifurnished": "Semi",
    "semi furnished": "Semi",
    "full": "Full",
    "furnished": "Full",
    "fully_furnished": "Full",
    "fully furnished": "Full",
}

FACING_MAP = {
    "east": "East",
    "west": "West",
    "north": "North",
    "south": "South",
}

PROPERTY_TYPE_MAP = {
    "apartment": "Apartment",
    "flat": "Apartment",
    "condo": "Apartment",
    "villa": "Villa",
    "house": "Villa",
    "independent_house": "Villa",
    "independent house": "Villa",
}


def generate_dataset(num_samples: int = NUM_SAMPLES) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    locations = list(CITY_PROFILES.keys())
    furnishing_levels = ["None", "Semi", "Full"]
    facing_values = ["East", "West", "North", "South"]
    property_types = ["Apartment", "Villa"]

    rows: list[dict] = []
    for _ in range(num_samples):
        location = rng.choice(locations)
        profile = CITY_PROFILES[location]
        property_type = rng.choice(property_types, p=[0.65, 0.35])
        bhk = int(rng.integers(1, 6))
        area_sqft = float(rng.integers(450, 4200 if property_type == "Villa" else 2600))
        bathrooms = int(np.clip(bhk + rng.integers(-1, 2), 1, 6))
        total_floors = int(rng.integers(1, 25 if property_type == "Apartment" else 4))
        floor = int(rng.integers(0, total_floors + 1))
        age_of_property = int(rng.integers(0, 35))
        parking = int(rng.choice([0, 1], p=[0.3, 0.7]))
        furnishing = rng.choice(furnishing_levels, p=[0.25, 0.45, 0.30])
        facing = rng.choice(facing_values)
        city_avg_price_per_sqft = profile["average_price_per_sqft"]
        floor_ratio = floor / max(total_floors, 1)

        base_price_lakhs = (city_avg_price_per_sqft * area_sqft) / 100000
        type_factor = 1.13 if property_type == "Villa" else 1.0
        age_factor = max(0.72, 1 - (age_of_property * 0.008))
        furnishing_factor = {"None": 0.96, "Semi": 1.03, "Full": 1.09}[str(furnishing)]
        facing_factor = {"East": 1.01, "West": 0.99, "North": 1.0, "South": 1.02}[str(facing)]
        floor_factor = 1 + (0.04 * floor_ratio if property_type == "Apartment" else 0.01 * floor_ratio)
        parking_factor = 1.03 if parking else 0.98
        bhk_bonus = bhk * 1.8
        bathroom_bonus = bathrooms * 1.0
        noise = float(rng.normal(0, 4.5))

        price_lakhs = (
            base_price_lakhs
            * type_factor
            * age_factor
            * furnishing_factor
            * facing_factor
            * floor_factor
            * parking_factor
        ) + bhk_bonus + bathroom_bonus + noise

        rows.append(
            {
                "location": location,
                "bhk": bhk,
                "area_sqft": round(area_sqft, 2),
                "bathrooms": bathrooms,
                "age_of_property": age_of_property,
                "floor": floor,
                "total_floors": total_floors,
                "parking": parking,
                "furnishing": str(furnishing),
                "facing": str(facing),
                "property_type": str(property_type),
                "city_avg_price_per_sqft": city_avg_price_per_sqft,
                "floor_ratio": round(floor_ratio, 3),
                "price_lakhs": round(max(price_lakhs, 10.0), 2),
            }
        )

    return pd.DataFrame(rows)


def normalize_header(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", value.strip().lower())).strip("_")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train the Kerala house price model using synthetic data or a custom CSV file."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Path to a CSV file containing training rows. If omitted, synthetic data will be generated.",
    )
    parser.add_argument(
        "--target-column",
        default=TRAINING_TARGET,
        help="Name of the target column in your CSV. Defaults to price_lakhs.",
    )
    parser.add_argument(
        "--target-unit",
        choices=["lakhs", "inr"],
        default="lakhs",
        help="Unit used by the target column in your CSV. Defaults to lakhs.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=NUM_SAMPLES,
        help="Synthetic sample count when --csv is not provided. Defaults to 6000.",
    )
    return parser.parse_args()


def rename_columns(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    renamed_df = df.copy()
    renamed_df.columns = [normalize_header(column) for column in renamed_df.columns]

    normalized_target = normalize_header(target_column)
    rename_map: dict[str, str] = {}

    for canonical_name, aliases in COLUMN_ALIASES.items():
        if canonical_name == TRAINING_TARGET and normalized_target in renamed_df.columns:
            source_column = normalized_target
        elif canonical_name in renamed_df.columns:
            source_column = canonical_name
        else:
            source_column = next((alias for alias in aliases if alias in renamed_df.columns), None)

        if source_column and source_column != canonical_name:
            rename_map[source_column] = canonical_name

    return renamed_df.rename(columns=rename_map)


def normalize_location(value: object) -> str | float:
    if pd.isna(value):
        return np.nan

    raw_value = str(value).strip()
    key = normalize_header(raw_value)

    if key in LOCATION_SYNONYMS:
        return LOCATION_SYNONYMS[key]

    for location in CITY_PROFILES:
        if normalize_header(location) == key:
            return location

    return raw_value


def normalize_category(value: object, mapping: dict[str, str]) -> str | float:
    if pd.isna(value):
        return np.nan

    normalized_value = normalize_header(str(value))
    return mapping.get(normalized_value, np.nan)


def normalize_parking(value: object) -> int | float:
    if pd.isna(value):
        return np.nan

    if isinstance(value, (bool, np.bool_)):
        return int(value)

    if isinstance(value, (int, float, np.integer, np.floating)):
        return int(float(value) > 0)

    normalized_value = normalize_header(str(value))
    true_values = {"1", "true", "yes", "y", "available"}
    false_values = {"0", "false", "no", "n", "not_available", "none"}

    if normalized_value in true_values:
        return 1
    if normalized_value in false_values:
        return 0
    return np.nan


def load_custom_dataset(csv_path: Path, target_column: str, target_unit: str) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    df = rename_columns(df, target_column)

    required_columns = REQUIRED_INPUT_COLUMNS + [TRAINING_TARGET]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Your CSV is missing required columns after normalization: {missing_text}. "
            "Please rename the columns or use supported aliases."
        )

    prepared_df = df.copy()
    prepared_df["location"] = prepared_df["location"].apply(normalize_location)
    prepared_df["furnishing"] = prepared_df["furnishing"].apply(lambda value: normalize_category(value, FURNISHING_MAP))
    prepared_df["facing"] = prepared_df["facing"].apply(lambda value: normalize_category(value, FACING_MAP))
    prepared_df["property_type"] = prepared_df["property_type"].apply(
        lambda value: normalize_category(value, PROPERTY_TYPE_MAP)
    )
    prepared_df["parking"] = prepared_df["parking"].apply(normalize_parking)

    numeric_columns = [
        "bhk",
        "area_sqft",
        "bathrooms",
        "age_of_property",
        "floor",
        "total_floors",
        TRAINING_TARGET,
    ]
    if "city_avg_price_per_sqft" in prepared_df.columns:
        numeric_columns.append("city_avg_price_per_sqft")
    if "floor_ratio" in prepared_df.columns:
        numeric_columns.append("floor_ratio")

    for column in numeric_columns:
        prepared_df[column] = pd.to_numeric(prepared_df[column], errors="coerce")

    if target_unit == "inr":
        prepared_df[TRAINING_TARGET] = prepared_df[TRAINING_TARGET] / 100000

    if "city_avg_price_per_sqft" not in prepared_df.columns:
        unknown_locations = sorted(
            {
                location
                for location in prepared_df["location"].dropna().unique()
                if location not in CITY_PROFILES
            }
        )
        if unknown_locations:
            raise ValueError(
                "Your CSV contains locations that are not present in backend/app/data/city_profiles.py and "
                "does not provide city_avg_price_per_sqft. Add the column or extend city_profiles.py for: "
                + ", ".join(unknown_locations)
            )
        prepared_df["city_avg_price_per_sqft"] = prepared_df["location"].map(
            lambda location: CITY_PROFILES[location]["average_price_per_sqft"]
        )

    prepared_df["floor_ratio"] = (
        prepared_df["floor"] / prepared_df["total_floors"].replace({0: np.nan})
    ).round(3)

    training_columns = REQUIRED_INPUT_COLUMNS + ["city_avg_price_per_sqft", "floor_ratio", TRAINING_TARGET]
    prepared_df = prepared_df[training_columns].copy()

    invalid_rows = prepared_df[
        prepared_df[training_columns].isna().any(axis=1)
        | (prepared_df["bhk"] < 1)
        | (prepared_df["area_sqft"] <= 0)
        | (prepared_df["bathrooms"] < 1)
        | (prepared_df["age_of_property"] < 0)
        | (prepared_df["floor"] < 0)
        | (prepared_df["total_floors"] < 1)
        | (prepared_df["floor"] > prepared_df["total_floors"])
        | (prepared_df[TRAINING_TARGET] <= 0)
    ]

    if not invalid_rows.empty:
        print(f"Removed {len(invalid_rows)} invalid row(s) from the custom CSV.")
        prepared_df = prepared_df.drop(index=invalid_rows.index)

    if len(prepared_df) < 50:
        raise ValueError(
            "Not enough valid rows remain after cleaning. Please provide at least 50 usable training rows."
        )

    integer_columns = ["bhk", "bathrooms", "age_of_property", "floor", "total_floors", "parking"]
    for column in integer_columns:
        prepared_df[column] = prepared_df[column].round().astype(int)

    return prepared_df


def train_model(df: pd.DataFrame, training_source: str) -> None:
    X = df.drop(columns=[TRAINING_TARGET])
    y = df[TRAINING_TARGET]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ]
    )

    model = XGBRegressor(
        n_estimators=320,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=RANDOM_SEED,
        objective="reg:squarederror",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    mae = float(mean_absolute_error(y_test, predictions))
    r2 = float(r2_score(y_test, predictions))

    models_dir = BACKEND_DIR / "models"
    models_dir.mkdir(exist_ok=True)

    joblib.dump(pipeline, models_dir / "house_price_model.joblib")

    metadata = {
        "model_type": "XGBRegressor pipeline",
        "target": TRAINING_TARGET,
        "mae_lakhs": round(mae, 3),
        "r2_score": round(r2, 4),
        "training_rows": len(df),
        "training_source": training_source,
        "locations_seen_in_training": sorted(df["location"].dropna().unique().tolist()),
        "app_supported_locations": list(CITY_PROFILES.keys()),
    }

    with (models_dir / "model_metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    print("Model trained successfully.")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    arguments = parse_args()

    if arguments.csv:
        dataset = load_custom_dataset(arguments.csv, arguments.target_column, arguments.target_unit)
        source_label = f"custom_csv:{arguments.csv.resolve()}"
    else:
        dataset = generate_dataset(arguments.samples)
        source_label = f"synthetic:{arguments.samples}_rows"

    train_model(dataset, source_label)
