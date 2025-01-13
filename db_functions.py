import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ship import Base, Ship


# Initialize the database connection
# Replacement for app.py
def init_db():
    engine = create_engine("sqlite:///shipDB.sqlite3", echo=True)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    session = sessionmaker(bind=engine)
    return session()


# Function to import ships data from a CSV file
# Replacement for push.py
def import_ships_from_csv(csv_file_path, session):
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ship = Ship(
                name=row["Ship Name"],
                capacity=int(row["Capacity (TEU)"]),
                speed_knots=float(row["Speed (knots)"]),
                length_m=float(row["Length (m)"]),
                beam_m=float(row["Beam (m)"]),
                draft_m=float(row["Draft (m)"]),
                displacement_tons=float(row["Displacement (tons)"]),
                block_coefficient=float(row["Block Coefficient"]),
            )
            session.add(ship)
    session.commit()
    print("Ships data imported successfully!")


# Function to query and display ships data
# Replacement for query.py
def display_ships(session, table_class):
    ships = session.query(table_class).all()
    print("Ships in the database:")
    for ship in ships:
        print(
            f"Name: {ship.name}, Capacity: {ship.capacity} TEU, "
            f"Speed: {ship.speed_knots} knots, Length: {ship.length_m} m, "
            f"Beam: {ship.beam_m} m, Draft: {ship.draft_m} m, "
            f"Displacement: {ship.displacement_tons} tons, "
            f"Block Coefficient: {ship.block_coefficient}"
        )



