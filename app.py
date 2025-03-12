import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize counters
counts = {"count1": 0, "count2": 0, "count3": 0}

# Divoom Pixoo64 API URL
DIVOOM_IP = "10.108.32.244"
DIVOOM_URL = f"http://{DIVOOM_IP}/post"

def send_to_divoom(message):
    """Send updated text to Divoom Pixoo64 with better formatting"""
    payload = {
        "Command": "Draw/SendHttpText",
        "TextId": 1,
        "x": 0,  # Align text to start
        "y": 16,  # Lowered text position for visibility
        "dir": 0,
        "font": 10,  # Adjust font size
        "color": 16777215,  # White color
        "textString": message
    }
    try:
        response = requests.post(DIVOOM_URL, json=payload)
        print(f"Sent to Divoom: {message}")  # Debugging message
        print("Divoom Response:", response.text)  # Debugging response
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print("Error sending to Divoom:", e)
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
    message = f"Rooms: {counts['count1']} | Inv: {counts['count2']} | PCs: {counts['count3']}"
    success = send_to_divoom(message)
    return jsonify({"success": success, "message": message})

if __name__ == '__main__':
    app.run(debug=True)
