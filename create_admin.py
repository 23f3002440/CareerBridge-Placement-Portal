#!/usr/bin/env python
"""Create admin user"""
from app import db, app, User

with app.app_context():
    # List all users
    users = User.query.all()
    # retrieve all users from the database and print their details
    print("Existing users:")
    for user in users:
        print(f"  {user.role}: {user.name} ({user.email}) - Active: {user.is_active}, Approved: {user.is_approved}")
    
    # Check if admin exists
    admin = User.query.filter_by(role='admin').first()
    if admin:
        print(f"\nAdmin user already exists: {admin.name} ({admin.email})")
        print("Login credentials:")
        print(f"  Username: {admin.name}")
        print(f"  Email: {admin.email}")
        # Reset admin password
        admin.password = 'admin123'
        db.session.commit()
        print("  Password reset to: admin123")
    else:
        # Create admin user
        admin_user = User(
            name='admin',
            email='admin@careerbridge.com',
            password='admin123',  # Change this in production
            role='admin',
            is_active=True,
            is_approved=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("\n✓ Admin user created:")
        print("  Username: admin")
        print("  Email: admin@careerbridge.com")
        print("  Password: admin123")
        print("  Login at: http://localhost:5000/login")
        
        
        # create if admin is missing
        # reset admin password
        # check if admin exists
        # show existing users