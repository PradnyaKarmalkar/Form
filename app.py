from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration - update these values with your actual database info
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Route to save form data
@app.route('/api/saveFormData', methods=['POST'])
def save_form_data():
    # Get data from request
    data = request.json
    
    # Validate input
    if not all(k in data for k in ['name', 'email', 'gender', 'city']):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Execute query
        query = "INSERT INTO user_data (name, email, gender, city) VALUES (%s, %s, %s, %s)"
        values = (data['name'], data['email'], data['gender'], data['city'])
        cursor.execute(query, values)
        
        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Data saved successfully'}), 200
    
    except Error as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Basic route for testing
@app.route('/')
def home():
    return "Flask server is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)