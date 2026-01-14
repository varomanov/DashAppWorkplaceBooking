from sqlalchemy.orm import Session
from models.models import Person, Place, Booking, engine

with Session(engine) as session:
    pass