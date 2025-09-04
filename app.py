from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json
from bson import ObjectId
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/waste_management'
mongo = PyMongo(app)

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Custom JSON encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

app.json_encoder = JSONEncoder

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        return render_template('index.html', user=user)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists
        if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return jsonify({'success': False, 'message': 'User already exists'})
        
        # Create new user
        user_id = mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'points': 0,
            'created_at': datetime.utcnow()
        }).inserted_id
        
        session['user_id'] = str(user_id)
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Simulate AI detection (placeholder)
        detected_objects = ['plastic bottle', 'paper', 'glass', 'metal can']
        detected_object = detected_objects[hash(data.get('image_url', '')) % len(detected_objects)]
        
        # Create report
        report_id = mongo.db.reports.insert_one({
            'user_id': ObjectId(session['user_id']),
            'image_url': data.get('image_url'),
            'location': {
                'lat': data.get('lat'),
                'lng': data.get('lng')
            },
            'detected_object': detected_object,
            'timestamp': datetime.utcnow(),
            'points_awarded': 10
        }).inserted_id
        
        # Update user points
        mongo.db.users.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$inc': {'points': 10}}
        )
        
        return jsonify({
            'success': True, 
            'message': 'Report submitted successfully',
            'detected_object': detected_object,
            'points_awarded': 10
        })
    
    return render_template('report.html')

@app.route('/map')
def map_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('map.html')

@app.route('/leaderboard')
def leaderboard():
    # Get top 10 users by points
    top_users = list(mongo.db.users.find().sort('points', -1).limit(10))
    return render_template('leaderboard.html', users=top_users)

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    score = data.get('score', 0)
    
    # Award points based on score
    points = score * 2  # 2 points per correct answer
    
    # Update user points
    mongo.db.users.update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$inc': {'points': points}}
    )
    
    return jsonify({'success': True, 'points_awarded': points})

@app.route('/admin')
def admin():
    if 'admin_id' not in session:
        return render_template('admin_login.html')
    
    # Get all users sorted by points
    users = list(mongo.db.users.find().sort('points', -1))
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple admin check (in production, use proper admin authentication)
    if username == 'admin' and password == 'admin123':
        session['admin_id'] = 'admin'
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid admin credentials'})

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin'))

@app.route('/api/recycling_centers')
def get_recycling_centers():
    # Sample recycling centers data
    centers = [
        {'name': 'Green Recycling Center', 'lat': 40.7128, 'lng': -74.0060, 'type': 'center'},
        {'name': 'Eco Bin #1', 'lat': 40.7589, 'lng': -73.9851, 'type': 'bin'},
        {'name': 'Waste Management Hub', 'lat': 40.7505, 'lng': -73.9934, 'type': 'center'},
        {'name': 'Recycle Point', 'lat': 40.7614, 'lng': -73.9776, 'type': 'bin'},
        {'name': 'Green Earth Center', 'lat': 40.7282, 'lng': -73.7949, 'type': 'center'}
    ]
    return jsonify(centers)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'url': f'/static/uploads/{unique_filename}'
        })
    
    return jsonify({'success': False, 'message': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
