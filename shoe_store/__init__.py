import os
from flask import Flask
from shoe_store.extensions import db, login_manager, bcrypt
from shoe_store.models import User, Category, Shoe
from shoe_store.core.routes import core_bp
from shoe_store.users.routes import user_bp
from shoe_store.shoes.routes import shoe_bp

def create_app():
    app = Flask(__name__)

    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        if "sslmode" not in db_url:
            db_url += "?sslmode=require" if "?" not in db_url else "&sslmode=require"
            
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
    
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoe_store.db'
        
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-123')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'warning'
    login_manager.login_message = 'Please log in to access this page.'
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(shoe_bp, url_prefix='/shoe')

    with app.app_context():
        db.create_all()

    return app
