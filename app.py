from flask import Flask, request, jsonify
import pandas as pd
import pickle
import os
from werkzeug.exceptions import BadRequest

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

# Initialize the Flask app
app = Flask(__name__)

# Define the input schema validation
valid_parts = ["EXTERIOR", "INTERIOR"]
valid_materials = [
    'cotton', 'viscose', 'fiber', 'elastane', 'polyester', 'linen',
    'lyocell', 'polyamide', 'nylon', 'wool', 'acrylic', 'camel',
    'cupro', 'modal'
]

@app.route('/')
def read_root():
    return {"message": "Welcome to the Reward Points Prediction API hosted on Flask!"}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from request
        input_data = request.get_json()

        # Validate input data
        part_name = input_data.get("part_name")
        material = input_data.get("material")
        eco_friendly = input_data.get("eco_friendly")
        item_price = input_data.get("item_price")

        if part_name not in valid_parts:
            raise BadRequest(f"Invalid part name! Must be 'EXTERIOR' or 'INTERIOR'.")
        if material not in valid_materials:
            raise BadRequest(f"Invalid material! Choose from: {', '.join(valid_materials)}.")

        # Prepare the input data for prediction
        input_df = pd.DataFrame([{
            "part_name": part_name,
            "eco_friendly": eco_friendly,
            "material": material,
            "item_price": item_price
        }])

        # Predict reward points
        try:
            reward_points = model.predict(input_df)[0]
            positive_reward_points = max(0, reward_points)
            return jsonify({"reward_points": positive_reward_points})
        except Exception as e:
            raise RuntimeError(f"Prediction error: {str(e)}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
