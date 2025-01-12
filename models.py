from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()


class Ship(Base):
    __tablename__ = "ships"

    id = Column("id", Integer, primary_key=True)
    name = Column("Ship Name", String, nullable=False)
    capacity = Column("Capacity (TEU)", Integer, nullable=False)
    speed_knots = Column("Speed (knots)", Float, nullable=False)
    length_m = Column("Length (m)", Float, nullable=False)
    beam_m = Column("Beam (m)", Float, nullable=False)
    draft_m = Column("Draft (m)", Float, nullable=False)
    displacement_tons = Column("Displacement (tons)", Float, nullable=False)
    block_coefficient = Column("Block Coefficient", Float, nullable=False)

    # Initialzing Ship Attributes via initializing Mehthod
    def __init__(self, name, capacity, speed_knots, length_m, beam_m, draft_m, displacement_tons, block_coefficient):
        self.name = name
        self.capacity = capacity
        self.speed_knots = speed_knots
        self.length_m = length_m
        self.beam_m = beam_m
        self.draft_m = draft_m
        self.displacement_tons = displacement_tons
        self.block_coefficient = block_coefficient
