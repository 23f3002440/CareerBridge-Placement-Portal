# delete the existing database and create a new one with the updated schema.
# This is useful during development when you make changes to the database models 
# and want to start fresh without any old data.
# Note that this will permanently delete all existing data in the database, so use it with caution.
"""Reset database with new schema"""
from app import db, app

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("✓ Database reinitialized with new schema")
