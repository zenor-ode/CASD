import csv
from ship import Ship
from app import session

# File path to the CSV file
# Replace with your actual CSV file path

csv_file_path = "ship_data.csv"
 
# Read CSV and add ship data to the database
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

# Commit all changes to the database
session.commit()
print("Ships data imported successfully!")
 
# Run push.py to import the CSV data into the database