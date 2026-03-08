#!/usr/bin/env python
"""Reset database with new schema"""
from app import db, app

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("✓ Database reinitialized with new schema")
