from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os

# Check if the model exists
model_file_path = 'model.pkl'
if not os.path.exists(model_file_path):
    raise FileNotFoundError('Model file not found! Please ensure model.pkl is present.')

# Load the model
with open(model_file_path, 'rb') as file:
    model = pickle.load(file)

# Define the FastAPI app
app = FastAPI()

# Define the request schema
class InputData(BaseModel):
    part_name: str
    eco_friendly: bool
    material: str
    item_price: float

# Define the predict endpoint
@app.post("/predict")
def predict(input_data: InputData):
    # Convert input to DataFrame
    input_df = pd.DataFrame([{
        "part_name": input_data.part_name,
        "eco_friendly": input_data.eco_friendly,
        "material": input_data.material,
        "item_price": input_data.item_price
    }])
    
    # Validate input if necessary
    valid_parts = ["EXTERIOR", "INTERIOR"]
    valid_materials = [
        'cotton', 'viscose', 'fiber', 'elastane', 'polyester', 'linen', 
        'lyocell', 'polyamide', 'nylon', 'wool', 'acrylic', 'camel', 
        'cupro', 'modal'
    ]
    
    if input_data.part_name not in valid_parts:
        raise HTTPException(status_code=400, detail="Invalid part name!")
    if input_data.material not in valid_materials:
        raise HTTPException(status_code=400, detail="Invalid material!")
    
    # Predict reward points
    try:
        reward_points = model.predict(input_df)[0]
        positive_reward_points = abs(reward_points)  # Ensure reward points are positive
        return {"reward_points": positive_reward_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
