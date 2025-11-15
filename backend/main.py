from fastapi import FastAPI # type: ignore
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# Load model
model = joblib.load('housing_model.pkl')

# Define input schema
class HouseFeatures(BaseModel):
    longitude: float = Field(..., ge=-125, le=-114, description="Between -125 and -114")
    latitude: float = Field(..., ge=32, le=42, description="Between 32 and 42")
    housing_median_age: float = Field(..., ge=1, le=52, description="1 to 52 years")
    total_rooms: float = Field(..., ge=1, le=40000, description="Total rooms in district")
    total_bedrooms: float = Field(..., ge=1, le=6000, description="Total bedrooms")
    population: float = Field(..., ge=1, le=35000, description="District population")
    households: float = Field(..., ge=1, le=6000, description="Number of households")
    median_income: float = Field(..., ge=0.5, le=15.0, description="Median income (in $10k)")
    ocean_proximity: str = Field(..., pattern="^(NEAR BAY|NEAR OCEAN|INLAND|ISLAND)$")

app = FastAPI(
    title="California House Price Predictor API",
    description="Predict median house value in California districts",
    version="1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the California House Price Prediction API! Go to /docs for docs."}

# Output schema for Swagger UI
class PredictionResponse(BaseModel):
    predicted_median_house_value: float
    currency: str

@app.post("/predict", response_model=PredictionResponse) 
def predict(data: HouseFeatures): 
    

    # Convert input data to DataFrame 
    df = pd.DataFrame([data.dict()])

     # Make prediction 
    prediction = model.predict(df)[0]

# If your model outputs in $100k, multiply by 100_000; otherwise remove multiplication
    # Return in dollars (model outputs in $100k)  
    return {
        "predicted_median_house_value": round(prediction * 1, 2),
        "currency": "USD"
    }
