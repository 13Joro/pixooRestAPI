from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from different origins (frontend)

@app.route('/')
def index():
    counts = 0  # Default value or fetch from a source
    return render_template('index.html', counts=counts)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print("Received data:", data)  # Debugging log
    return jsonify({"message": "API request received successfully!"})




@app.route('/post', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error_code": "Request data illegal json"}), 400
        
        command = data.get("Command")
        text_string = data.get("textString")

        if not command or not text_string:
            return jsonify({"error_code": "Missing required fields"}), 400

        # Example response
        return jsonify({
            "status": "success",
            "received_command": command,
            "received_text": text_string
        }), 200
    except Exception as e:
        return jsonify({"error_code": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
