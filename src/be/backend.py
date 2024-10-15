from flask import Flask, jsonify, session, request
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'



# Define a route for the root URL
@app.route('/')
def home():
    return "Backend is running!"

# Define a route for an API endpoint
@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({"board": np.ones((8, 8)).tolist()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)


