from app import app, db, User

with app.app_context():
    admin = User.query.filter_by(name="admin").first()
    if admin:
        print(f"Admin exists: {admin.name}")
        print(f"Role: {admin.role}")
        print(f"Active: {admin.is_active}")
        print(f"Approved: {admin.is_approved}")
    else:
        print("Admin user not found")