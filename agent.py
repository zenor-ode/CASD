import os

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import ship
from ship import Ship

from db_functions import init_db

def main():
    session = init_db()
    #ships = session.query(Ship).all()
    # ships =
    # ship_data = [
    #     {
    #         "id": ship.id,
    #         "Ship Name": ship.name,
    #         "Capacity": ship.capacity,
    #         "Speed": ship.speed_knots,
    #         "Length": ship.length_m,
    #         "Beam": ship.beam_m,
    #         "Draft": ship.draft_m,
    #         "Displacement": ship.displacement_tons,
    #         "Block Coefficient": ship.block_coefficient,
    #     }
    #     for ship in ships
    # ]
    # df = pd.DataFrame(ship_data)
    df = pd.read_csv("synthetic_ships.csv")
    df = df.rename(
        columns={
            "Capacity (TEU)": "Capacity",
            "Speed (knots)": "Speed",
            "Length (m)": "Length",
            "Beam (m)": "Beam",
            "Draft (m)": "Draft",
            "Displacement (tons)": "Displacement",
            "Block Coefficient": "Block Coefficient",
        }
    )


    X = df[['Capacity', 'Speed']]  # Input features (Capacity and Speed)
    y = df[['Length', 'Beam', 'Draft', 'Displacement', 'Block Coefficient']]  # Target variables

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #train & test split

    # Step 4: Feature Scaling (standardize the data)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Step 5: Train a model for each target feature (using Random Forest Regressor as an example)
    models = {}
    for feature in y.columns:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train[feature])
        models[feature] = model

    # Step 6: Predictions for all target features
    y_pred = {}
    for feature in y.columns:
        y_pred[feature] = models[feature].predict(X_test_scaled)

    # Step 7: Evaluate the models using Mean Absolute Error (MAE)
    for feature in y.columns:
        mae = mean_absolute_error(y_test[feature], y_pred[feature])
        print(f'Mean Absolute Error for {feature} Prediction: {mae}')

    # # Example of predicting for a new ship
    # new_ship_data = np.array([[1200, 23]])  # Example new ship data (Capacity, Speed)
    # new_ship_data_scaled = scaler.transform(new_ship_data)
    #
    # new_ship_predictions = {}
    # for feature in y.columns:
    #     new_ship_predictions[feature] = models[feature].predict(new_ship_data_scaled)[0]
    #
    # print("\nPredicted values for the new ship:")
    # print(new_ship_predictions)


    #os.makedirs("models", exist_ok=True)
    for feature, model in models.items():
        filename = os.path.join(f"{feature}_predictor_model.pkl")
        joblib.dump(model, filename)
        print(f"Model for {feature} saved as {filename}.")
    joblib.dump(scaler, "scaler.pkl")

def load_scaler_from_path(name):
    # Load the scaler
    scaler = joblib.load(name)
    print(f"Scaler loaded from {name}.")
    return  scaler

def load_models():
    loaded_models = {}
    for feature in ['Length', 'Beam', 'Draft', 'Displacement', 'Block Coefficient']:
        filename = f"{feature}_predictor_model.pkl"
        loaded_models[feature] = joblib.load(filename)
        print(f"Loaded model for {feature} from {filename}.")
    return loaded_models

def predict_features(capacity, speed, loaded_models, scaler):
    new_ship_data = np.array([[capacity, speed]])  # Example new ship data (Capacity, Speed)
    new_ship_data_scaled = scaler.transform(new_ship_data)  # Use the same scaler from training

    new_ship_predictions = {}
    for feature, model in loaded_models.items():
        new_ship_predictions[feature] = model.predict(new_ship_data_scaled)[0]

    print("Predicted values for the new ship using loaded models:")
    print(new_ship_predictions)


if __name__ == "__main__":
    main()