from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ship import Base

# Ship database
engine = create_engine("sqlite:///shipDB.sqlite3", echo=True)

# Creating table for database
Base.metadata.create_all(engine)

# Initialize sessios
Session = sessionmaker(bind=engine)
session = Session()

# Run app.py to initialize (Update) the database.