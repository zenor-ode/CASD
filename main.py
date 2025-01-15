from db_functions import init_db, display_ships, import_ships_from_csv
from sqlalchemy import MetaData, create_engine
from synthetic_ship import SyntheticShip, generate_synthetic_ships, write_to_csv
from ship import Ship
from agent import load_models, predict_features, load_scaler_from_path


def main():
    session = init_db()
    # display_ships(session,Ship)
    # display_ships(session,SyntheticShip)
    # real_ships = session.query(Ship).all()
    # generated_ships = generate_synthetic_ships(real_ships, 5000) # synthetic data generation
    # write_to_csv(generated_ships, "generated_ships_alot.csv")
    # import_ships_from_csv("generated_ships_alot.csv",session)
    #
    #
    # display_ships(session,SyntheticShip)
    print("Start")
    models = load_models()
    scaler = load_scaler_from_path("scaler.pkl")
    predict_features(50000, 10, models, scaler)
    print("End")



if __name__ == "__main__":
    main()
