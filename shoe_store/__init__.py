# ดึงค่า DATABASE_URL มาจาก Render Environment
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        # 1. เปลี่ยน postgres:// เป็น postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        # 2. บังคับใช้ SSL (แก้ปัญหา SSL connection closed ที่เจอใน Log)
        if "sslmode" not in db_url:
            db_url += "?sslmode=require" if "?" not in db_url else "&sslmode=require"
            
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoe_store.db'
