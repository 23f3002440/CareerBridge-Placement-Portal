from flask import Flask
from models import db
# we have created database in models.py hence importing database from it
app = Flask(__name__)
#create main Flask app object
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///placement.db"
# database is created 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# disables the feature that tracks every object change
# saves memory
db.init_app(app)
# app interact  with the database using the app context
with app.app_context():
    db.create_all()
# create all the tables that are defined in models.py

# Test route
@app.route("/")
def home():
    return "Placement Portal Running"

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes