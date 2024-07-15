#!/usr/bin/python3
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City  # Import the City model


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # Define the relationship with City
    cities = relationship("City", backref="state")

    @property
    def cities(self):
        """ Gets the list of City instances linked to the current State """
        city_list = []
        for city in models.storage.all(City).values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
