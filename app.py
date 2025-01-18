from fastapi import FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os

# Define the model file path dynamically
model_file_path = os.path.join(os.getcwd(), 'model.pkl')
if not os.path.exists(model_file_path):
    raise FileNotFoundError('Model file not found! Ensure model.pkl is uploaded correctly.')

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Reward Points Prediction API hosted on Render!"}

@app.post("/predict")
def predict(input_data: InputData):
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

    input_df = pd.DataFrame([{
        "part_name": input_data.part_name,
        "eco_friendly": input_data.eco_friendly,
        "material": input_data.material,
        "item_price": input_data.item_price
    }])

    try:
        reward_points = model.predict(input_df)[0]
        positive_reward_points = max(0, reward_points)
        return {"reward_points": positive_reward_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Wrap the FastAPI app as WSGI
from wsgiref.simple_server import make_server

def app_wsgi(environ, start_response):
    return WSGIMiddleware(app)(environ, start_response)
