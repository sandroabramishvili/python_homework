from sqlalchemy import Date, create_engine, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship, sessionmaker
from models import Hotel, Room, Guest, Booking, engine
from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

# CRUD ოპერაციები

# ახალი სასტუმროს დამატება
# ახალი ოთახის დამატება
# ახალი სტუმრის დამატება
# ახალი Booking-ის შექმნა

def add_hotel(name: str, country: str, city: str, stars: int):
    hotel = Hotel(name=name, country=country, city=city, stars=stars)
    session.add(hotel)
    session.commit()
    return hotel

def add_room(room_number: str, floor: int, price_per_night: float, hotel_id: int):
    room = Room(room_number=room_number, floor=floor, price_per_night=price_per_night, hotel_id=hotel_id)
    session.add(room)
    session.commit()
    return room

def add_guest(first_name: str, last_name: str, email: str, phone: str):
    guest = Guest(first_name=first_name, last_name=last_name, email=email, phone=phone)
    session.add(guest)
    session.commit()
    return guest

def add_booking(guest_id: int, room_id: int, check_in: date, check_out: date):
    booking = Booking(guest_id=guest_id, room_id=room_id, check_in=check_in, check_out=check_out)
    session.add(booking)
    session.commit()
    return booking

# ყველა სასტუმროს მიღება
# კონკრეტული სასტუმროს მიღება `id`-ით
# ყველა ოთახის მიღება
# კონკრეტული სტუმრის მიღება `email`-ით

def get_all_hotels():
    return session.query(Hotel).all()

def get_hotel_by_id(hotel_id: int):
    return session.query(Hotel).filter(Hotel.id == hotel_id).first()

def get_all_rooms():
    return session.query(Room).all()

def get_guest_by_email(email: str):
    return session.query(Guest).filter(Guest.email == email).first()

# შექმენით ფუნქცია, რომელიც ოთახის ფასს შეცვლის.

def update_room_price(room_id: int, new_price: float):
    room = session.query(Room).filter(Room.id == room_id).first()
    if room:
        room.price_per_night = new_price
        session.commit()
        return room
    return None

# სტუმრის წაშლა
# ოთახის წაშლა

def delete_guest(guest_id: int):
    guest = session.query(Guest).filter(Guest.id == guest_id).first()
    if guest:
        session.delete(guest)
        session.commit()
        return True
    return False

def delete_room(room_id: int):
    room = session.query(Room).filter(Room.id == room_id).first()
    if room:
        session.delete(room)
        session.commit()
        return True
    return False