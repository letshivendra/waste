#!/usr/bin/env python3
"""
EcoTracker - Simplified Version
Works without external dependencies for testing
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Simple in-memory storage (replace with MongoDB later)
users_db = {}
reports_db = []
recycling_centers = [
    {'name': 'Green Recycling Center', 'lat': 40.7128, 'lng': -74.0060, 'type': 'center'},
    {'name': 'Eco Bin #1', 'lat': 40.7589, 'lng': -73.9851, 'type': 'bin'},
    {'name': 'Waste Management Hub', 'lat': 40.7505, 'lng': -73.9934, 'type': 'center'},
    {'name': 'Recycle Point', 'lat': 40.7614, 'lng': -73.9776, 'type': 'bin'},
    {'name': 'Green Earth Center', 'lat': 40.7282, 'lng': -73.7949, 'type': 'center'}
]

# Routes
@app.route('/')
def index():
    user = None
    if 'user_id' in session and session['user_id'] in users_db:
        user = users_db[session['user_id']]
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists
        for user_id, user in users_db.items():
            if user['username'] == username or user['email'] == email:
                return jsonify({'success': False, 'message': 'User already exists'})
        
        # Create new user
        user_id = str(uuid.uuid4())
        users_db[user_id] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password': password,  # In real app, hash this
            'points': 0,
            'created_at': datetime.utcnow().isoformat()
        }
        
        session['user_id'] = user_id
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Find user
        for user_id, user in users_db.items():
            if user['username'] == username and user['password'] == password:
                session['user_id'] = user_id
                return jsonify({'success': True, 'message': 'Login successful'})
        
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
        
        # Simulate AI detection
        detected_objects = ['plastic bottle', 'paper', 'glass', 'metal can']
        detected_object = detected_objects[hash(data.get('image_url', '')) % len(detected_objects)]
        
        # Create report
        report_id = str(uuid.uuid4())
        report = {
            'id': report_id,
            'user_id': session['user_id'],
            'image_url': data.get('image_url'),
            'location': {
                'lat': data.get('lat'),
                'lng': data.get('lng')
            },
            'detected_object': detected_object,
            'timestamp': datetime.utcnow().isoformat(),
            'points_awarded': 10
        }
        reports_db.append(report)
        
        # Update user points
        if session['user_id'] in users_db:
            users_db[session['user_id']]['points'] += 10
        
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
    top_users = sorted(users_db.values(), key=lambda x: x['points'], reverse=True)[:10]
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
    points = score * 2
    
    # Update user points
    if session['user_id'] in users_db:
        users_db[session['user_id']]['points'] += points
    
    return jsonify({'success': True, 'points_awarded': points})

@app.route('/admin')
def admin():
    if 'admin_id' not in session:
        return render_template('admin_login.html')
    
    users = sorted(users_db.values(), key=lambda x: x['points'], reverse=True)
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
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
    return jsonify(recycling_centers)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    # Create upload directory
    os.makedirs('static/uploads', exist_ok=True)
    
    # Save file
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join('static/uploads', filename)
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'filename': filename,
        'url': f'/static/uploads/{filename}'
    })

# Add some demo users
def add_demo_users():
    demo_users = [
        {'username': 'eco_warrior', 'email': 'warrior@test.com', 'password': 'demo123', 'points': 250},
        {'username': 'green_champion', 'email': 'champion@test.com', 'password': 'demo123', 'points': 180},
        {'username': 'planet_saver', 'email': 'saver@test.com', 'password': 'demo123', 'points': 120},
    ]
    
    for user_data in demo_users:
        user_id = str(uuid.uuid4())
        users_db[user_id] = {
            'id': user_id,
            'username': user_data['username'],
            'email': user_data['email'],
            'password': user_data['password'],
            'points': user_data['points'],
            'created_at': datetime.utcnow().isoformat()
        }

if __name__ == '__main__':
    # Add demo users
    add_demo_users()
    
    print("🌱 EcoTracker - Simplified Version")
    print("=" * 40)
    print("✅ No external dependencies required!")
    print("📍 Server: http://localhost:5000")
    print("👤 Demo users: eco_warrior, green_champion, planet_saver")
    print("🔑 Demo password: demo123")
    print("🔧 Admin: admin / admin123")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

