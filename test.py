import requests

url = "https://repurpose-model-git-main-sanjib-shahs-projects.vercel.app/predict"
payload = {
    "part_name": "EXTERIOR",
    "eco_friendly": True,
    "material": "cotton",
    "item_price": 150.0
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Reward Points:", response.json())
else:
    print("Error:", response.status_code, response.text)
