# ดึงค่าจาก Environment
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        # 1. แก้เรื่องชื่อโปรโตคอล (postgres -> postgresql)
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        # 2. แก้เรื่อง SSL (เติมต่อท้าย URL)
        # ตัวนี้จะแก้ปัญหา "SSL connection has been closed" ใน Log ของคุณครับ
        if "sslmode" not in db_url:
            db_url += "?sslmode=require" if "?" not in db_url else "&sslmode=require"
            
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoe_store.db'

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')
