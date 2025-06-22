from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/fs', methods=['GET', 'POST'])
def home():
    print(request.method)
    if request.method == 'GET':
        file = request.args.get('file')
        if not file:
            return jsonify(statuscode=400, error="File name is required")
        file += ".json"
        cwd = Path.cwd()
        file_path = Path(cwd, "data", file)
        if not file_path.exists():
            return jsonify(statuscode=404, error="File not found")
        df = pd.read_json(file_path)
        json_data = df.to_dict(orient="records")
        if not json_data:
            # If the file is empty, return an empty list
            return jsonify(statuscode=200, data=[])
        return jsonify(statuscode=200, data=json_data)
    else:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        file, json_data = data.values()

        cwd = Path.cwd()
        file_path = Path(cwd, "data")
        if not file_path.exists():
            Path.mkdir(file_path)
        df = pd.DataFrame(json_data)
        json_file = Path(file_path, file + ".json")
        df.to_json(json_file, orient="records", indent=2)

        return jsonify(statuscode=200, message="Data saved successfully")


if __name__ == '__main__':
    app.run(debug=True)
