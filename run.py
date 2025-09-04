#!/usr/bin/env python3
"""
EcoTracker - Waste Management Web Application
Startup script for development and production
"""

import os
import sys
from app import app

def main():
    """Main entry point for the application"""
    
    # Check if MongoDB is available
    try:
        from flask_pymongo import PyMongo
        mongo = PyMongo(app)
        # Test connection
        mongo.db.command('ping')
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Please ensure MongoDB is running on localhost:27017")
        sys.exit(1)
    
    # Create upload directory if it doesn't exist
    upload_dir = app.config.get('UPLOAD_FOLDER', 'static/uploads')
    os.makedirs(upload_dir, exist_ok=True)
    print(f"✅ Upload directory ready: {upload_dir}")
    
    # Get configuration
    debug = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting EcoTracker server...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌱 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    if debug:
        print("\n📝 Development Notes:")
        print("- Admin login: admin / admin123")
        print("- MongoDB: mongodb://localhost:27017/waste_management")
        print("- Upload folder: static/uploads/")
        print("- Google Maps API key needed for map functionality")
    
    print("\n" + "="*50)
    
    # Start the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    main()
