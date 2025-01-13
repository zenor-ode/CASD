from ship import Ship
from app import session

# Print the database for csv file
ships = session.query(Ship).all()
print("Ships in the database:")
for ship in ships:
    print(
        f"Name: {ship.name}, Capacity: {ship.capacity} TEU, "
        f"Speed: {ship.speed_knots} knots, Length: {ship.length_m} m, "
        f"Beam: {ship.beam_m} m, Draft: {ship.draft_m} m, "
        f"Displacement: {ship.displacement_tons} tons, "
        f"Block Coefficient: {ship.block_coefficient}"
    )

# Run query.py to verify and display the imported data.