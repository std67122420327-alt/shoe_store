import os
from flask import Flask
from shoe_store.extensions import db, login_manager, bcrypt
from shoe_store.models import User, Category, Shoe
from shoe_store.core.routes import core_bp
from shoe_store.users.routes import user_bp
from shoe_store.shoes.routes import shoe_bp

# Load environment variables from .env file (for local development only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, using system environment variables (production)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'warning'
    login_manager.login_message = 'Please log in to access this page.'
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(shoe_bp, url_prefix='/shoe')

    return app