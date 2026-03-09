class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement.db"
    # which database to Use
    # database location
    # database file name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # disable the feature to track object changes
# to set configuration for the flask application, specifically for SQLAlchemy database connection and tracking modifications.