from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv  
from extension import db
from flask_cors import CORS
import os

load_dotenv()               #load environment variables from .env file  

#app = Flask(__name__)       #creating Flask app instance

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # <-- allow frontend requests

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)        #initialzing the database object
db.init_app(app)

limiter = Limiter(get_remote_address,       #rate litmting, allow max of 10 request per min 
    app=app,
    default_limits=["10 per minute"] )

from routes.review_route import review_bp
app.register_blueprint(review_bp)

if __name__ == '__main__':
    print("Starting the Flask application...")
    with app.app_context():
        db.create_all()
    app.run(debug=True)

