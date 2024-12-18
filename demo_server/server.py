from flask import Flask, jsonify, request

from demo_server.controller import Controller
from ds import DS
# Create a Flask app instance
app = Flask(__name__)

# Define a GET endpoint
@app.route("/api/fetch_receipts", methods=["GET"])
def fetch_receipts():
    if not data_storage.is_ready():
        return jsonify({"error": "Data storage is empty"}), 200
    return jsonify(data_storage.curr_storage)

# Run the server
if __name__ == "__main__":
    data_storage = DS()
    controller = Controller()
    controller.start_scheduling(data_storage)
    app.run(host="0.0.0.0", port=8000, debug=True)