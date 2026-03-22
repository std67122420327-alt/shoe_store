import os
from flask import Flask
from shoe_store.extensions import db, login_manager, bcrypt
from shoe_store.models import User, Category, Shoe
from shoe_store.shoe_categories import CATEGORY_NAMES
from shoe_store.core.routes import core_bp
from shoe_store.users.routes import user_bp
from shoe_store.shoes.routes import shoe_bp

def create_app():
    app = Flask(__name__)

    # --- เริ่มส่วนจัดการฐานข้อมูล (DATABASE CONFIG) ---
    db_url = os.environ.get('DATABASE_URL')

    if db_url:
        # 1. แก้ไขจาก postgres:// เป็น postgresql:// (สำคัญมากสำหรับ SQLAlchemy 1.4+)
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        # 2. เพิ่ม sslmode เพื่อให้เชื่อมต่อกับ Render Database ได้
        if "sslmode" not in db_url:
            db_url += "?sslmode=require" if "?" not in db_url else "&sslmode=require"

        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # 3. ถ้าไม่เจอ DATABASE_URL ให้ใช้ SQLite (สำหรับรันในคอมตัวเอง)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoe_store.db'
    # --- จบส่วนจัดการฐานข้อมูล ---

    # อย่าลืมตั้งค่า SECRET_KEY (ถ้าไม่มี หน้าเว็บจะล่มเวลาใช้ Flash Message)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

    # ... (ส่วนอื่นของโปรแกรม เช่น db.init_app(app), register_blueprint)
    # db.init_app(app)
    # bcrypt.init_app(app)
    # login_manager.init_app(app)

    return app
