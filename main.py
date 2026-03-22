import os
from shoe_store import create_app

app = create_app()

db_url = os.getenv("DATABASE_URL")

if db_url:
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    if "sslmode" not in db_url:
        if "?" in db_url:
            db_url += "&sslmode=require"
        else:
            db_url += "?sslmode=require"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'รหัสลับสำรองกรณีลืมตั้งในRender')

if __name__ == "__main__":
    app.run()
