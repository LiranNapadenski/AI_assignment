from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow front-end to call back-end

@app.route('/data', methods=['POST'])
def handle_data():
    data = request.json
    return jsonify({'response': f'Backend received: {data["message"]}'})

if __name__ == '__main__':
    app.run(debug=True)
