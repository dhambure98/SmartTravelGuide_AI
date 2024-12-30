from flask import Flask, request, jsonify

app = Flask(__name__)

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
            print(f"No destinations found matching preferences '{preferences}' within budget {budget_range}")
            return jsonify({"error": "No destinations found within your budget and age range"}), 404

        recommendations = filtered_df.to_dict(orient='records')
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
