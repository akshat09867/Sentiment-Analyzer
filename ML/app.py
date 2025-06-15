from flask import Flask, request, jsonify
import pickle
import re # Import re for your clean_text function
import pandas as pd # Import pandas if your preprocessing uses it
from flask_cors import CORS
# Import other necessary libraries you used in your notebook
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.preprocessing import LabelEncoder # We'll need this to inverse transform predictions

app = Flask(__name__)
CORS(app) # Enable CORS to allow requests from your Node.js backend

MODEL_PATH = 'sentiment_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'
LABEL_ENCODER_PATH = 'label_encoder.pkl' # We need to save and load the LabelEncoder too!

sentiment_model = None
vectorizer = None
label_encoder = None # Variable to hold the loaded LabelEncoder

# --- Define the clean_text function from your notebook ---
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)  # Remove URLs, mentions, hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters/numbers
    return text.strip().lower()

# --- Load the trained model, vectorizer, and label encoder when the app starts ---
def load_resources():
    global sentiment_model, vectorizer, label_encoder
    try:
        with open(MODEL_PATH, 'rb') as model_file:
            sentiment_model = pickle.load(model_file)
        print(f"Model loaded from {MODEL_PATH}")

        with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        print(f"Vectorizer loaded from {VECTORIZER_PATH}")

        # --- Load the LabelEncoder ---
        # You need to save your LabelEncoder from your notebook as well!
        with open(LABEL_ENCODER_PATH, 'rb') as le_file:
             label_encoder = pickle.load(le_file)
        print(f"Label Encoder loaded from {LABEL_ENCODER_PATH}")


    except Exception as e:
        print(f"Error loading resources: {e}")
        sentiment_model = None
        vectorizer = None
        label_encoder = None
        # In a production app, you'd want better error handling and logging here

# --- Define the prediction endpoint ---
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    # Check if resources are loaded
    if sentiment_model is None or vectorizer is None or label_encoder is None:
        return jsonify({'error': 'ML resources not loaded'}), 500

    data = request.get_json(force=True)

    # Get the text from the incoming JSON request
    text_to_analyze = data.get('text', '')

    if not text_to_analyze or not isinstance(text_to_analyze, str):
        return jsonify({'error': 'Valid text string not provided'}), 400

    try:
        # --- Preprocess the input text using the loaded clean_text function and vectorizer ---
        cleaned_text = clean_text(text_to_analyze)
        # Vectorizers typically expect input as a list
        processed_text_list = [cleaned_text]
        text_vectorized = vectorizer.transform(processed_text_list)


        # --- Make prediction using the loaded model ---
        numerical_prediction = sentiment_model.predict(text_vectorized)

        # --- Convert numerical prediction back to sentiment label ---
        # Use the loaded LabelEncoder to inverse transform the prediction
        predicted_sentiment = str(label_encoder.inverse_transform(numerical_prediction)[0])


        return jsonify({'sentiment': predicted_sentiment})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Error predicting sentiment'}), 500

# --- Basic health check or root endpoint ---
@app.route('/')
def status():
    return jsonify({
        'status': 'Python ML service is running',
        'model_loaded': sentiment_model is not None,
        'vectorizer_loaded': vectorizer is not None,
        'label_encoder_loaded': label_encoder is not None
    })

# --- Run the Flask app ---
if __name__ == '__main__':
    load_resources() # Load the model, vectorizer, and label encoder when the script is run
    # Run the Flask development server on a port (e.g., 5001)
    # Use a different port than your Node.js backend (e.g., 5000)
    app.run(debug=True, port=5001)
    # For production, use gunicorn: gunicorn -w 4 -b 0.0.0.0:5001 app:app