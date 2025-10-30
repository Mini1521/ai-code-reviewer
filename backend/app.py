from flask import Flask, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv  
from extension import db
import os

load_dotenv()                                           #load environment variables from .env file (API key) 

# Adjust static + template folders
# Assuming frontend files (index.html, style.css, script.js) are in ../frontend
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder='static', 
            template_folder='templates')                #instance for Flask app created, static file and HTML templates stored are defined.


#configure database to use SQLite and disable tracking modifications to save resources
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
db.init_app(app)                                        #initialzing the database (SQLAlchemy) object

limiter = Limiter(get_remote_address,                   #rate litmting
    app=app,
    default_limits=["10 per minute"] )                  # allow max of 10 request per min 

from routes.review_route import review_bp               #importing and registering the blueprint from review_routes.py
app.register_blueprint(review_bp)

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    """Serve index.html from frontend directory"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static_files(path):
    """Serve JS, CSS, and other assets"""
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == '__main__':                              #start Flask app
    print("Starting the Flask application...")
    with app.app_context():
        db.create_all()                                 #database and tables created if non-existent
    app.run(debug=True)                                 #Flask app run in debug mode

