import random
import csv
import numpy as np
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from  sklearn.cluster import KMeans


# Define the base and synthetic ships model
Base = declarative_base()


class SyntheticShip(Base):
    __tablename__ = "synthetic_ships"

    id = Column("id", Integer, primary_key=True)
    name = Column("Ship Name", String, nullable=False)
    capacity = Column("Capacity (TEU)", Integer, nullable=False)
    speed_knots = Column("Speed (knots)", Float, nullable=False)
    length_m = Column("Length (m)", Float, nullable=False)
    beam_m = Column("Beam (m)", Float, nullable=False)
    draft_m = Column("Draft (m)", Float, nullable=False)
    displacement_tons = Column("Displacement (tons)", Float, nullable=False)
    block_coefficient = Column("Block Coefficient", Float, nullable=False)

    # Initializing Ship Attributes via initializing Method
    def __init__(self, name, capacity, speed_knots, length_m, beam_m, draft_m, displacement_tons, block_coefficient):
        self.name = name
        self.capacity = capacity
        self.speed_knots = speed_knots
        self.length_m = length_m
        self.beam_m = beam_m
        self.draft_m = draft_m
        self.displacement_tons = displacement_tons
        self.block_coefficient = block_coefficient


# Generate synthetic ships data
def generate_synthetic_ships(real_ships, num_synthetic_ships, n_clusters=7):
    synthetic_ships = []

    # Prepare real ship data for clustering
    ship_data = np.array([
        [
            ship.capacity,
            ship.speed_knots,
            ship.length_m,
            ship.beam_m,
            ship.draft_m,
            ship.displacement_tons,
            ship.block_coefficient,
        ]
        for ship in real_ships
    ])

    # K-Means clustering on real ship data
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(ship_data)

    cluster_centers = kmeans.cluster_centers_

    for _ in range(num_synthetic_ships):
        # Randomly select a cluster
        cluster_idx = random.randint(0, n_clusters - 1)
        cluster_center = cluster_centers[cluster_idx]

        # Add random noise to the cluster center for variability
        noise = np.random.normal(0, 0.05, cluster_center.shape)  # Small noise
        synthetic_attributes = cluster_center + noise

        # Create a new synthetic ship dictionary
        new_ship = {
            "Ship Name": f"Synthetic_{random.randint(1000, 9999)}", # this needs to be changed, should not be random
            "Capacity (TEU)": int(max(1, synthetic_attributes[0])),  # Ensure positive capacity
            "Speed (knots)": max(0, synthetic_attributes[1]),        # Ensure non-negative speed
            "Length (m)": max(0, synthetic_attributes[2]),
            "Beam (m)": max(0, synthetic_attributes[3]),
            "Draft (m)": max(0, synthetic_attributes[4]),
            "Displacement (tons)": max(0, synthetic_attributes[5]),
            "Block Coefficient": min(max(0, synthetic_attributes[6]), 1),  # Block coefficient in [0, 1]
        }

        synthetic_ships.append(new_ship)

    return synthetic_ships


# Write synthetic ships to a new CSV file
def write_to_csv(synthetic_ships, output_csv_path):
    with open(output_csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Ship Name",
            "Capacity (TEU)",
            "Speed (knots)",
            "Length (m)",
            "Beam (m)",
            "Draft (m)",
            "Displacement (tons)",
            "Block Coefficient",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(synthetic_ships)
    print(f"Synthetic ship data written to {output_csv_path}")
