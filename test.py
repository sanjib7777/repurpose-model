# Updated test.py
import requests

# Replace with your Vercel URL
url = "https://repurpose-model-q0uaf6n0o-sanjib-shahs-projects.vercel.app/predict"

# Sample payload
payload = {
    "part_name": "EXTERIOR",
    "eco_friendly": True,
    "material": "cotton",
    "item_price": 120
}

try:
    # Send POST request
    response = requests.post(url, json=payload)

    # Print response
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Error connecting to {url}: {e}")
