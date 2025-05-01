# 🧾 Reward Points Prediction API

This is a Flask-based REST API that predicts reward points for clothing items based on attributes like part name, material, eco-friendliness, and item price. The machine learning model is pre-trained and loaded using `pickle`.

---

## 🚀 Features

- Predicts **reward points** for clothing items
- Accepts JSON POST requests
- Includes input validation for part name and material
- Handles errors gracefully
- Deployed locally using Flask

---


---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt

```
## Clone the repo
```
git clone https://github.com/your-username/reward-points-api.git
cd reward-points-api
```

## Start the Flask server
```
python app.py
http://127.0.0.1:5000
```
## 🔍 API Endpoints - POST /predict
Request Body (JSON)
```
{
  "part_name": "EXTERIOR",
  "material": "cotton",
  "eco_friendly": true,
  "item_price": 49.99
}
```
📤 Response
```
{
  "reward_points": 120
}




