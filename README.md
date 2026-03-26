# Kerala House Price Prediction System

Kerala House Price Prediction System is a full-stack web application that predicts residential property prices in Kerala and augments the result with practical local intelligence such as weather, nearby schools and hospitals, city-level price comparisons, investment scoring, and property portal suggestions.

## Highlights

- FastAPI backend with modular routes, services, SQLite persistence, and simple JWT authentication.
- XGBoost training pipeline for house price regression using realistic synthetic Kerala housing data.
- React + Vite frontend with a responsive multi-page experience for home, prediction, results, login, and signup flows.
- Graceful fallback behavior when Google Maps or OpenWeather API keys are missing or external requests fail.
- Docker support for containerized frontend and backend startup.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, XGBoost, Pandas, NumPy, Scikit-learn
- Frontend: React, React Router, Vite, CSS
- Database: SQLite
- Optional APIs: Google Maps API, OpenWeather API, Unsplash-compatible image URLs

## Project Structure

```text
house-price-prediction/
|-- backend/
|   |-- app.py
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- models/
|   |   |-- .gitkeep
|   |-- scripts/
|   |   |-- train_model.py
|   |-- app/
|   |   |-- main.py
|   |   |-- api/
|   |   |   |-- routes/
|   |   |   |   |-- auth.py
|   |   |   |   |-- health.py
|   |   |   |   |-- prediction.py
|   |   |-- core/
|   |   |   |-- config.py
|   |   |   |-- database.py
|   |   |   |-- security.py
|   |   |-- db/
|   |   |   |-- models.py
|   |   |   |-- schemas.py
|   |   |-- data/
|   |   |   |-- city_profiles.py
|   |   |-- ml/
|   |   |   |-- predictor.py
|   |   |-- services/
|   |   |   |-- insight_service.py
|   |   |   |-- location_service.py
|   |   |   |-- recommendation_service.py
|-- frontend/
|   |-- package.json
|   |-- vite.config.js
|   |-- Dockerfile
|   |-- nginx.conf
|   |-- src/
|   |   |-- api/
|   |   |-- assets/
|   |   |-- components/
|   |   |-- context/
|   |   |-- pages/
|   |   |-- styles/
|   |   |-- utils/
|-- docker-compose.yml
|-- README.md
```

## Core Features

- Property input form with Kerala city dropdown, BHK, area, bathrooms, age, floor details, parking, furnishing, facing, and property type.
- `POST /predict` endpoint for price prediction and market insights.
- `GET /location-info` endpoint for weather and nearby facilities.
- `GET /recommendations` endpoint for property portal suggestions and locality tips.
- Investment score, area popularity, confidence range, and average city price comparison.
- Login and signup support with JWT-based authentication.

## Backend Setup

1. Open a terminal in [backend](/C:/Projects/house-price-prediction/backend).
2. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Copy the environment template:

```powershell
Copy-Item .env.example .env
```

5. Train and save the XGBoost model artifact:

```powershell
python scripts/train_model.py
```

You can also train with your own CSV:

```powershell
python scripts/train_model.py --csv C:\path\to\kerala_houses.csv
```

If your target price column uses a different name or stores values in rupees instead of lakhs:

```powershell
python scripts/train_model.py --csv C:\path\to\kerala_houses.csv --target-column price_inr --target-unit inr
```

6. Start the backend:

```powershell
uvicorn app.main:app --reload
```

The backend runs at [http://localhost:8000](http://localhost:8000) and Swagger docs are available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Frontend Setup

1. Open a terminal in [frontend](/C:/Projects/house-price-prediction/frontend).
2. Install dependencies:

```powershell
npm install
```

3. Copy the frontend environment template:

```powershell
Copy-Item .env.example .env
```

4. Start the development server:

```powershell
npm run dev
```

The frontend runs at [http://localhost:5173](http://localhost:5173).

## Docker Setup

1. Copy [backend/.env.example](/C:/Projects/house-price-prediction/backend/.env.example) to `backend/.env`.
2. From the project root [house-price-prediction](/C:/Projects/house-price-prediction), run:

```powershell
docker compose up --build
```

3. Access the services:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

## API Endpoints

- `POST /predict`
- `GET /location-info?location=Kochi&property_type=Apartment`
- `GET /recommendations?location=Kochi&property_type=Apartment&budget_lakhs=90`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `GET /health`

## Example Prediction Payload

```json
{
  "location": "Kochi",
  "bhk": 3,
  "area_sqft": 1500,
  "bathrooms": 3,
  "age_of_property": 5,
  "floor": 4,
  "total_floors": 12,
  "parking": true,
  "furnishing": "Semi",
  "facing": "East",
  "property_type": "Apartment"
}
```

## Environment Variables

Backend variables in [backend/.env.example](/C:/Projects/house-price-prediction/backend/.env.example):

- `SECRET_KEY`
- `DATABASE_URL`
- `ALLOWED_ORIGINS`
- `GOOGLE_MAPS_API_KEY`
- `OPENWEATHER_API_KEY`
- `UNSPLASH_ACCESS_KEY`
- `MODEL_PATH`
- `METADATA_PATH`

Frontend variables in [frontend/.env.example](/C:/Projects/house-price-prediction/frontend/.env.example):

- `VITE_API_BASE_URL`

## Notes

- The backend automatically uses fallback city profiles if external APIs are unavailable.
- If the trained model artifact does not exist yet, the API falls back to a deterministic rule-based estimator so the application still works during first-time setup.
- For best reproducibility, generate the model by running [train_model.py](/C:/Projects/house-price-prediction/backend/scripts/train_model.py) after installing dependencies.
- The custom CSV trainer supports common aliases for columns like `city`, `bedrooms`, `area`, `bathroom`, `parking`, and `price`.
- If your CSV introduces new locations that are not already defined in [city_profiles.py](/C:/Projects/house-price-prediction/backend/app/data/city_profiles.py), also extend that file so the app dropdown, insights, and fallback enrichment remain consistent.
