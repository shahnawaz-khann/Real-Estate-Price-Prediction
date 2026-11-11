from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import util

app = Flask(__name__)
CLIENT_DIR = Path(__file__).resolve().parent.parent / 'client'


@app.route('/', methods=['GET'])
def home():
    return send_from_directory(CLIENT_DIR, 'app.html')


@app.route('/<path:filename>', methods=['GET'])
def client_asset(filename):
    if filename not in {'app.css', 'app.js'}:
        return jsonify({'error': 'Not found.'}), 404
    return send_from_directory(CLIENT_DIR, filename)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/get_location_names', methods=['GET'])
@app.route('/api/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
@app.route('/api/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    payload = request.get_json(silent=True) or request.form or {}

    try:
        total_sqft = float(payload.get('total_sqft'))
        location = str(payload.get('location', '')).strip()
        bhk = int(payload.get('bhk'))
        bath = int(payload.get('bath'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input. Please provide total_sqft, location, bhk, and bath.'}), 400

    if total_sqft <= 0:
        return jsonify({'error': 'total_sqft must be greater than zero.'}), 400
    if bhk <= 0 or bath <= 0:
        return jsonify({'error': 'bhk and bath must be positive integers.'}), 400
    if not location:
        return jsonify({'error': 'location is required.'}), 400

    try:
        price = util.get_estimated_price(location, total_sqft, bhk, bath)
    except ValueError:
        return jsonify({'error': f"Location '{location}' is not supported."}), 400

    response = jsonify({'estimated_price': price})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=False)