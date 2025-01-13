from db_functions import init_db, display_ships, import_ships_from_csv
from sqlalchemy import MetaData, create_engine
from synthetic_ship import SyntheticShip, generate_synthetic_ships, write_to_csv
from ship import Ship

def main():
    session = init_db()
    display_ships(session,Ship)
    display_ships(session,SyntheticShip)
    # real_ships = session.query(Ship).all()
    # generated_ships = generate_synthetic_ships(real_ships, 5) # synthetic data generation
    # write_to_csv(generated_ships, "generated_ships.csv")
    # import_ships_from_csv("generated_ships.csv",session)


    display_ships(session,SyntheticShip)


if __name__ == "__main__":
    main()
