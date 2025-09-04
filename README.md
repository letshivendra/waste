# 🌱 EcoTracker - Waste Management Web Application

A comprehensive full-stack web application for waste tracking, recycling center discovery, and environmental gamification.

## ✨ Features

### 👤 User Management
- **User Registration & Login** with secure session management
- **MongoDB Integration** for user data storage
- **Points System** for gamification

### 📸 Waste Reporting
- **Photo Upload** with drag-and-drop interface
- **Geolocation API** for automatic location detection
- **AI Object Detection** (simulated) for waste classification
- **Recycling Information** with step-by-step guides

### 🗺️ Interactive Map
- **Google Maps Integration** for recycling center discovery
- **Real-time Location** services
- **Distance Calculation** and sorting
- **Multiple Marker Types** (centers vs bins)

### 🏆 Gamification
- **Leaderboard System** with real-time updates
- **Achievement Badges** and progress tracking
- **Interactive Quiz** with environmental knowledge
- **Points Rewards** for various activities

### 🎮 Admin Panel
- **User Management** dashboard
- **Rewards System** for top performers
- **Analytics** and engagement metrics
- **System Administration** tools

### 📱 Progressive Web App (PWA)
- **Offline Support** with service workers
- **Installable** on mobile devices
- **Responsive Design** for all screen sizes
- **Push Notifications** (ready for implementation)

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database
- **Flask-PyMongo** - MongoDB integration
- **Werkzeug** - Security and utilities

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icon library

### APIs & Services
- **Google Maps JavaScript API** - Map functionality
- **Geolocation API** - Location services
- **File Upload API** - Image handling
- **RESTful APIs** - Backend communication

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- Node.js (for development tools)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd waste-management-app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MongoDB
```bash
# Start MongoDB service
sudo systemctl start mongod  # Linux
# or
brew services start mongodb-community  # macOS
```

### 5. Configure Environment
Create a `.env` file:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/waste_management
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
waste-management-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── report.html       # Waste reporting
│   ├── map.html          # Recycling centers map
│   ├── leaderboard.html  # User leaderboard
│   ├── quiz.html         # Environmental quiz
│   ├── admin_login.html  # Admin authentication
│   └── admin_dashboard.html # Admin panel
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   ├── main.js       # Main JavaScript
│   │   └── sw.js         # Service worker
│   ├── images/           # PWA icons and images
│   ├── uploads/          # User uploaded images
│   └── manifest.json     # PWA manifest
└── uploads/              # File upload directory
```

## 🔧 Configuration

### Google Maps API
1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Maps JavaScript API
3. Add your domain to API restrictions
4. Update `YOUR_API_KEY` in `templates/map.html`

### MongoDB Setup
```python
# Default connection string
MONGO_URI = 'mongodb://localhost:27017/waste_management'
```

### File Upload Configuration
```python
# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Upload directory
UPLOAD_FOLDER = 'static/uploads'
```

## 🎯 Usage

### For Users
1. **Register/Login** to create an account
2. **Report Waste** by uploading photos and getting location
3. **Find Centers** using the interactive map
4. **Take Quiz** to earn bonus points
5. **View Leaderboard** to see rankings
6. **Install PWA** for mobile access

### For Admins
1. **Login** with admin credentials (admin/admin123)
2. **Manage Users** and view analytics
3. **Award Rewards** to top performers
4. **Monitor System** performance

## 🚀 Deployment

### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Add environment variables

### Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 🔒 Security Features

- **Password Hashing** with Werkzeug
- **Session Management** with Flask sessions
- **File Upload Validation** with type checking
- **CSRF Protection** (ready for implementation)
- **Input Sanitization** for all user inputs

## 📊 Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "username": "string",
  "email": "string",
  "password": "hashed_string",
  "points": "number",
  "created_at": "datetime"
}
```

### Reports Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "image_url": "string",
  "location": {
    "lat": "number",
    "lng": "number"
  },
  "detected_object": "string",
  "timestamp": "datetime",
  "points_awarded": "number"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap for the UI framework
- Font Awesome for icons
- Google Maps for mapping services
- MongoDB for database services
- Flask community for excellent documentation

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@ecotracker.com
- Documentation: [Wiki](https://github.com/your-repo/wiki)

---

**Made with ❤️ for a cleaner planet! 🌍**
