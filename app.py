from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# Load your trained model
model_path = os.path.join("model", "model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

# Root route → redirect to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple check (replace with DB check if needed)
        if username == 'admin' and password == '1234':
            return redirect(url_for('predict'))  # Success → prediction page
        else:
            flash("Invalid username or password")  # show error message

    return render_template('login.html')

# Prediction route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Default values for all fields
    data = {
        "bedrooms": "",
        "bathrooms": "",
        "area": "",
        "floors": "",
        "yearbuilt": "",
        "parking": "",
        "lotsize": "",
        "distance": "",
        "location": "",
        "nearby": "",
        "housetype": "",
        "condition": "",
        "amenity": "",
    }
    display_price = None  # Price variable

    if request.method == 'POST':
        # Collect values from form
        for key in data.keys():
            data[key] = request.form.get(key, '')

        # Prepare numeric input for prediction
        try:
            input_values = [
                float(data["bedrooms"] or 0),
                float(data["bathrooms"] or 0),
                float(data["area"] or 0),
                float(data["floors"] or 0),
                float(data["yearbuilt"] or 0),
                float(data["parking"] or 0),
                float(data["lotsize"] or 0),
                float(data["distance"] or 0),
                # categorical placeholders
                0, 0, 0, 0, 0
            ]

            if model is None:
                display_price = "Model not loaded"
            else:
                prediction = model.predict([input_values])[0]

                # ✅ Convert prediction to readable format (Lakhs / Crores)
                if prediction >= 100:  # more than 100 Lakhs (1 Cr)
                    display_price = f"₹ {prediction/100:.2f} Cr"
                else:
                    display_price = f"₹ {prediction:.2f} Lakhs"

        except Exception as e:
            display_price = f"Error: {e}"

    return render_template('predict.html', price=display_price, **data)


if __name__ == '__main__':
    app.run(debug=True)
