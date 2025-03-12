import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize counters
counts = {"count1": 0, "count2": 0, "count3": 0}

# Divoom Pixoo64 API URL
DIVOOM_IP = "10.108.32.244"
DIVOOM_URL = f"http://{DIVOOM_IP}/post"

def send_to_divoom(message):
    """Send updated text to Divoom Pixoo64"""
    payload = {
        "Command": "Draw/SendHttpText",
        "TextId": 1,
        "x": 5,
        "y": 5,
        "dir": 0,
        "font": 10,
        "color": 16777215,  # White color
        "textString": message
    }
    try:
        response = requests.post(DIVOOM_URL, json=payload)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@app.route('/')
def index():
    return render_template('index.html', counts=counts)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    counter = data.get("counter")
    action = data.get("action")

    if counter in counts:
        if action == "increase":
            counts[counter] += 1
        elif action == "decrease" and counts[counter] > 0:
            counts[counter] -= 1

    return jsonify(counts)

@app.route('/submit', methods=['POST'])
def submit():
    message = f"Count 1: {counts['count1']} | Count 2: {counts['count2']} | Count 3: {counts['count3']}"
    success = send_to_divoom(message)
    return jsonify({"success": success, "message": message})

if __name__ == '__main__':
    app.run(debug=True)
