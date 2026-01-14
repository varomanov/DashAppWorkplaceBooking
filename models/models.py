from sqlalchemy import create_engine, Date, Integer, String, ForeignKey, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import date, timedelta
from typing import List

engine = create_engine('sqlite:///booking.db')


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'persons'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50))
    
    bookings: Mapped[List['Booking']] = relationship(back_populates='person', cascade='all, delete-orphan')


class Place(Base):
    __tablename__ = 'places'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    placename: Mapped[str] = mapped_column(String(20))

    bookings: Mapped[List['Booking']] = relationship(back_populates='place', cascade='all, delete-orphan')


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    place_id: Mapped[int] = mapped_column(ForeignKey('places.id', ondelete='CASCADE', onupdate='CASCADE'))
    booked_at: Mapped[date] = mapped_column(Date)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)

    person: Mapped['Person'] = relationship(back_populates='bookings')
    place: Mapped['Place'] = relationship(back_populates='bookings')


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def get_persons():
    with Session(engine) as session:
        result = session.scalars(select(Person).order_by(Person.fullname))
        return [{'name': x.fullname, 'id': x.id} for x in result]

def get_dates():
    with Session(engine) as session:
        result = session.scalars(
            select(Booking.booked_at)
            .order_by(Booking.booked_at)
            .distinct()
        )
        return list(result)

def get_places():
    with Session(engine) as session:
        result = session.scalars(select(Place).order_by(Place.placename))
        return [{'name': x.placename, 'id': x.id} for x in result]

def book_place(date, user_id: int, place_id: int):
    with Session(engine) as session:
        result = session.scalar(
            select(Booking).where(
                Booking.place_id==place_id,
                Booking.booked_at==date,
                Booking.is_booked==False
            )
        )
        if result is None:
            return False
        
        result.person_id = user_id
        session.commit()
        return True

def remove_place(row_id: int):
    with Session(engine) as session:
        # Сначала получаем объект
        booking = session.scalar(
            select(Booking).where(
                Booking.id == row_id  # если нужен конкретный ID
            )
        )
        
        if booking is None:
            return False
        
        # Удаляем объект
        session.delete(booking)
        session.commit()
        return True


def get_user_places(user_id):
    with Session(engine) as session:
        result = session.scalars(select(Booking).where(Booking.person_id == user_id))
        data = [{'name': x.person.fullname, 'dept': x.person.department, 'dt': x.booked_at, 'place': x.place.placename, 'row_id': x.id} for x in result]
        if data:
            return data
        return False

def get_all_booked_places():
    with Session(engine) as session:
        result = session.scalars(select(Booking).where(Booking.person_id > 0))
        data = [{'name': x.person.fullname, 'dept': x.person.department, 'dt': x.booked_at, 'place': x.place.placename, 'row_id': x.id, 'user_id': x.person_id} for x in result]
        if data:
            return data
        return False


if __name__ == '__main__':
    
    def add_person():
        persons = [
            {'name': 'Игорь Серов', 'dept': 'Финансы'},
            {'name': 'Василий Огурцов', 'dept': 'Маркетинг'},
            {'name': 'Егор Бордов', 'dept': 'Кадры'},
            {'name': 'Виктор Бубнов', 'dept': 'Аналитика'},
        ]
        with Session(engine) as session:
            for person in persons:
                session.add(Person(fullname=person['name'], department=person['dept']))
                session.commit()
    
    
    def add_places():
        with Session(engine) as session:
            for i in range(10, 25):
                session.add(Place(placename=f'934/{i}'))
                session.commit()


    def add_slots():
        with Session(engine) as session:
            for i in range(1, 11):
                dt = date.today() + timedelta(days=i)
                for j in range(1, 16):
                    session.add(Booking(place_id=j, booked_at=dt))
                    session.commit()

    # add_person()
    # add_places()
    # add_slots()