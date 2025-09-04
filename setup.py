#!/usr/bin/env python3
"""
EcoTracker Setup Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists('venv'):
        return run_command('python -m venv venv', 'Creating virtual environment')
    else:
        print("✅ Virtual environment already exists")
        return True

def install_dependencies():
    """Install Python dependencies"""
    if os.name == 'nt':  # Windows
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        pip_cmd = 'venv/bin/pip'
    
    return run_command(f'{pip_cmd} install -r requirements.txt', 'Installing dependencies')

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/uploads',
        'static/images',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✅ Created .env file from template")
            print("📝 Please update .env with your actual configuration values")
        else:
            print("⚠️  env.example not found, please create .env manually")
    else:
        print("✅ .env file already exists")
    
    return True

def check_mongodb():
    """Check if MongoDB is available"""
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB not available: {e}")
        print("📝 Please install and start MongoDB before running the application")
        return False

def main():
    """Main setup function"""
    print("🌱 EcoTracker Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create environment file
    create_env_file()
    
    # Check MongoDB
    check_mongodb()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Update .env file with your configuration")
    print("2. Get a Google Maps API key for map functionality")
    print("3. Start MongoDB service")
    print("4. Run the application:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python run.py")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
        print("   python run.py")
    
    print("\n🌍 Happy coding for a cleaner planet!")

if __name__ == '__main__':
    main()
