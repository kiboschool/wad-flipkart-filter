from app import app, db

with app.app_context():
    print("creating database")
    db.create_all()
