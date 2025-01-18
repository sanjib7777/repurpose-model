
# 1. Library imports
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
try:
    with open(model_file_path, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

# Initialize the FastAPI app
app = FastAPI()

# Define the input schema
class InputData(BaseModel):
    part_name: str
    eco_friendly: bool
    material: str
    item_price: float

# Define the predict endpoint
@app.post("/predict")
def predict(input_data: InputData):
    # Validate input fields
    valid_parts = ["EXTERIOR", "INTERIOR"]
    valid_materials = [
        'cotton', 'viscose', 'fiber', 'elastane', 'polyester', 'linen', 
        'lyocell', 'polyamide', 'nylon', 'wool', 'acrylic', 'camel', 
        'cupro', 'modal'
    ]
    
    if input_data.part_name not in valid_parts:
        raise HTTPException(status_code=400, detail="Invalid part name! Must be 'EXTERIOR' or 'INTERIOR'.")
    if input_data.material not in valid_materials:
        raise HTTPException(status_code=400, detail=f"Invalid material! Choose from: {', '.join(valid_materials)}.")

    # Prepare data for prediction
    input_df = pd.DataFrame([{
        "part_name": input_data.part_name,
        "eco_friendly": input_data.eco_friendly,
        "material": input_data.material,
        "item_price": input_data.item_price
    }])

    # Predict reward points
    try:
        reward_points = model.predict(input_df)[0]
        positive_reward_points = abs(reward_points)  # Ensure reward points are positive
        return {"reward_points": positive_reward_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Add a main block for local testing
if __name__ == "__main__":
    # Test data
    test_input = InputData(
        part_name="EXTERIOR",
        eco_friendly=True,
        material="cotton",
        item_price=120.50
    )
    
    # Print test prediction
    try:
        prediction_result = predict(test_input)
        print(f"Test Prediction Result: {prediction_result}")
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
