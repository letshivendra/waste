#!/usr/bin/env python3
"""
EcoTracker Demo Data Script
Populate the database with sample data for testing
"""

from app import app, mongo
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_demo_users():
    """Create demo users with different point levels"""
    demo_users = [
        {
            'username': 'eco_warrior_2024',
            'email': 'warrior@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 1250,
            'created_at': datetime.utcnow() - timedelta(days=30)
        },
        {
            'username': 'green_champion',
            'email': 'champion@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 890,
            'created_at': datetime.utcnow() - timedelta(days=25)
        },
        {
            'username': 'planet_saver',
            'email': 'saver@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 650,
            'created_at': datetime.utcnow() - timedelta(days=20)
        },
        {
            'username': 'recycle_master',
            'email': 'master@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 420,
            'created_at': datetime.utcnow() - timedelta(days=15)
        },
        {
            'username': 'waste_hunter',
            'email': 'hunter@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 280,
            'created_at': datetime.utcnow() - timedelta(days=10)
        },
        {
            'username': 'eco_beginner',
            'email': 'beginner@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 150,
            'created_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'username': 'new_user',
            'email': 'new@ecotracker.com',
            'password': generate_password_hash('demo123'),
            'points': 50,
            'created_at': datetime.utcnow() - timedelta(days=2)
        }
    ]
    
    print("🔄 Creating demo users...")
    for user in demo_users:
        existing_user = mongo.db.users.find_one({'username': user['username']})
        if not existing_user:
            mongo.db.users.insert_one(user)
            print(f"✅ Created user: {user['username']} ({user['points']} points)")
        else:
            print(f"⚠️  User already exists: {user['username']}")

def create_demo_reports():
    """Create demo waste reports"""
    users = list(mongo.db.users.find())
    if not users:
        print("❌ No users found. Please create users first.")
        return
    
    waste_types = ['plastic bottle', 'paper', 'glass', 'metal can', 'cardboard', 'aluminum can']
    locations = [
        {'lat': 40.7128, 'lng': -74.0060, 'name': 'New York City'},
        {'lat': 40.7589, 'lng': -73.9851, 'name': 'Times Square'},
        {'lat': 40.7505, 'lng': -73.9934, 'name': 'Central Park'},
        {'lat': 40.7614, 'lng': -73.9776, 'name': 'Brooklyn Bridge'},
        {'lat': 40.7282, 'lng': -73.7949, 'name': 'Queens'},
    ]
    
    print("🔄 Creating demo reports...")
    
    for i in range(50):  # Create 50 demo reports
        user = random.choice(users)
        location = random.choice(locations)
        waste_type = random.choice(waste_types)
        
        # Add some random variation to coordinates
        lat = location['lat'] + random.uniform(-0.01, 0.01)
        lng = location['lng'] + random.uniform(-0.01, 0.01)
        
        report = {
            'user_id': user['_id'],
            'image_url': f'/static/uploads/demo_image_{i+1}.jpg',
            'location': {
                'lat': lat,
                'lng': lng
            },
            'detected_object': waste_type,
            'timestamp': datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            'points_awarded': 10
        }
        
        mongo.db.reports.insert_one(report)
    
    print("✅ Created 50 demo reports")

def create_demo_recycling_centers():
    """Create demo recycling centers data"""
    centers = [
        {
            'name': 'Green Earth Recycling Center',
            'lat': 40.7128,
            'lng': -74.0060,
            'type': 'center',
            'address': '123 Green Street, New York, NY',
            'hours': 'Mon-Fri: 8AM-6PM, Sat-Sun: 9AM-5PM',
            'services': ['Plastic', 'Paper', 'Glass', 'Metal']
        },
        {
            'name': 'Eco Bin #1',
            'lat': 40.7589,
            'lng': -73.9851,
            'type': 'bin',
            'address': 'Times Square, New York, NY',
            'hours': '24/7',
            'services': ['General Waste', 'Recyclables']
        },
        {
            'name': 'Waste Management Hub',
            'lat': 40.7505,
            'lng': -73.9934,
            'type': 'center',
            'address': '456 Central Park West, New York, NY',
            'hours': 'Mon-Sat: 7AM-7PM',
            'services': ['All Materials', 'Electronics', 'Hazardous Waste']
        },
        {
            'name': 'Recycle Point',
            'lat': 40.7614,
            'lng': -73.9776,
            'type': 'bin',
            'address': 'Brooklyn Bridge Park, New York, NY',
            'hours': '24/7',
            'services': ['Plastic', 'Paper']
        },
        {
            'name': 'Green Valley Center',
            'lat': 40.7282,
            'lng': -73.7949,
            'type': 'center',
            'address': '789 Queens Blvd, Queens, NY',
            'hours': 'Mon-Fri: 9AM-5PM',
            'services': ['Glass', 'Metal', 'Cardboard']
        }
    ]
    
    print("🔄 Creating demo recycling centers...")
    for center in centers:
        existing_center = mongo.db.recycling_centers.find_one({'name': center['name']})
        if not existing_center:
            mongo.db.recycling_centers.insert_one(center)
            print(f"✅ Created center: {center['name']}")
        else:
            print(f"⚠️  Center already exists: {center['name']}")

def main():
    """Main function to populate demo data"""
    print("🌱 EcoTracker Demo Data Generator")
    print("=" * 40)
    
    with app.app_context():
        # Create demo users
        create_demo_users()
        print()
        
        # Create demo reports
        create_demo_reports()
        print()
        
        # Create demo recycling centers
        create_demo_recycling_centers()
        print()
        
        # Display statistics
        user_count = mongo.db.users.count_documents({})
        report_count = mongo.db.reports.count_documents({})
        center_count = mongo.db.recycling_centers.count_documents({})
        
        print("📊 Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Reports: {report_count}")
        print(f"   Recycling Centers: {center_count}")
        
        print("\n🎉 Demo data created successfully!")
        print("\n📝 Demo Login Credentials:")
        print("   Username: eco_warrior_2024")
        print("   Password: demo123")
        print("   Points: 1250")
        
        print("\n   Username: green_champion")
        print("   Password: demo123")
        print("   Points: 890")

if __name__ == '__main__':
    main()
