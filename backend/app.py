import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from rabbitmq_client import publish_to_rabbitmq

load_dotenv()

app = Flask(__name__)

CORS(app)

# Sundesi me mongodb
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_default_database()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Flask API is running!"}), 200

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.json
    if not data or not data.get('email') or not data.get('message'):
        return jsonify({"error": "Missing required fields"}), 400
    
    contact_doc = {
        "name": data.get('name', 'Anonymous'),
        "email": data.get('email'),
        "message": data.get('message'),
    }
    result = db.contacts.insert_one(contact_doc)
    
    #Kanoyme serialize to _id gia na mporoyme na to apothikeusoyme sto rabbitmq
    contact_doc['_id'] = str(result.inserted_id)
    
    # Apostoloi toy mhnumatow sto rabbitmq
    publish_to_rabbitmq(contact_doc)
    
    return jsonify({"success": True, "message": "Contact saved successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)