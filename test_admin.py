from app import app, db, User
# import app database and user model
with app.app_context():
    # create flask app context to access database
    admin = User.query.filter_by(name="admin").first()
    # query the data base - matches the first matching record
    if admin:
        # if admin exist in database
        print(f"Admin exists: {admin.name}")
        print(f"Role: {admin.role}")
        print(f"Active: {admin.is_active}")
        print(f"Approved: {admin.is_approved}")
    else:
        print("Admin user not found")
        
        
# to check whether admin account exists in the database and print its details.