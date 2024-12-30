from flask import Flask, request, jsonify
from flask_cors import CORS  
import pandas as pd

app = Flask(__name__)
CORS(app)  

# Load the dataset
try:
    df = pd.read_csv("data/travel.csv")
    print("Columns in CSV:", df.columns)
    print("Unique preferences in the dataset:", df['user_preferences'].unique())
except FileNotFoundError:
    print("Error: 'travel.csv' not found. Please ensure it is in the same directory.")
    df = pd.DataFrame() 

# Example of a GET route
@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    try:
        destinations = df.head().to_dict(orient='records')
        return jsonify({"destinations": destinations}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# POST route for recommendations
@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        preferences = data.get("preferences", "").lower()
        age = data.get("age")
        budget_range = data.get("budget_range", [0, float("inf")])

        print(f"Received preferences: {preferences}")
        print(f"Age: {age}, Budget Range: {budget_range}")

        if not preferences or age is None or not budget_range:
            return jsonify({"error": "Invalid input. Please provide preferences, age, and budget range."}), 400

        print("Original DataFrame:")
        print(df.head())

        filtered_df = df[
            df['user_preferences'].str.contains(preferences, case=False, na=False) &
            (df['budget'] >= budget_range[0]) &
            (df['budget'] <= budget_range[1])
        ]

        print("Filtered DataFrame:")
        print(filtered_df)

        if filtered_df.empty:
            return jsonify({"error": "No destinations found within your budget and age range"}), 404

        recommendations = filtered_df.to_dict(orient='records')
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
