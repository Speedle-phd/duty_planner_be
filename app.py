import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
load_dotenv()  # take environment variables

app = Flask(__name__)
CORS(app, origins=["*"])  # Enable CORS for all origins
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")] # type: ignore
duties = db.duties

@app.route('/api/v1/fs', methods=['GET', 'PATCH'])
def home():
    print(request.method)
    if request.method == 'GET':
        try:
            mongo_data = duties.find()
            filtered_data = []
            for item in mongo_data:
                dict_item = {
                    "id": item["id"],
                    "duty": item["duty"],
                }
                filtered_data.append(dict_item)
            return jsonify(statuscode=200, data=filtered_data)
        except Exception as e:
            print(f"Error fetching data: {e}")
            return jsonify(statuscode=500, message="Internal Server Error"), 500
    else:
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            duties.find_one_and_update(
                {"id": data["id"]},
                {"$set": {"duty": data["duty"]}},
            )
            return jsonify(statuscode=200, message="Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
            return jsonify(statuscode=500, message="Internal Server Error"), 500


if __name__ == '__main__':
    app.run(debug=True)
