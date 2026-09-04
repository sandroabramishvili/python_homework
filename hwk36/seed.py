from models import Hotel, Room, Guest, Booking, engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

hotels = [
    Hotel(name='Grand Hotel', country='Georgia', city='Tbilisi', stars=5),
    Hotel(name='Tbilisi Palace', country='Georgia', city='Tbilisi', stars=4),
    Hotel(name='Rotel', country='Georgia', city='Kutaisi', stars=3),
]
session.add_all(hotels)
session.commit()

rooms = [
    Room(room_number='101', floor=1, price_per_night=150.0, hotel_id=1),
    Room(room_number='102', floor=1, price_per_night=200.0, hotel_id=1),
    Room(room_number='201', floor=2, price_per_night=250.0, hotel_id=1),
    Room(room_number='202', floor=2, price_per_night=300.0, hotel_id=2),
    Room(room_number='301', floor=3, price_per_night=350.0, hotel_id=2),
    Room(room_number='302', floor=3, price_per_night=400.0, hotel_id=2),
    Room(room_number='101', floor=1, price_per_night=80.0, hotel_id=3),
    Room(room_number='102', floor=1, price_per_night=100.0, hotel_id=3),
    Room(room_number='201', floor=2, price_per_night=120.0, hotel_id=3),
]
session.add_all(rooms)
session.commit()

guests = [
    Guest(first_name='Lasha', last_name='Gelashvili', email='lg@gmail.com', phone='555-0101'),
    Guest(first_name='Nino', last_name='Gelashvili', email='ng@gmail.com', phone='555-0102'),
    Guest(first_name='Giorgi', last_name='Khmaladze', email='gk@gmail.com', phone='555-0103'),
    Guest(first_name='Mariam', last_name='Japaridze', email='mj@gmail.com', phone='555-0104'),
    Guest(first_name='Saba', last_name='Svanidze', email='ss@gmail.com', phone='555-0105'),
]
session.add_all(guests)
session.commit()

from datetime import date

bookings = [
    Booking(guest_id=1, room_id=1, check_in=date(2026, 6, 1), check_out=date(2026, 6, 5)),
    Booking(guest_id=2, room_id=2, check_in=date(2026, 6, 2), check_out=date(2026, 6, 6)),
    Booking(guest_id=3, room_id=3, check_in=date(2026, 6, 3), check_out=date(2026, 6, 7)),
    Booking(guest_id=4, room_id=4, check_in=date(2026, 6, 4), check_out=date(2026, 6, 8)),
    Booking(guest_id=5, room_id=5, check_in=date(2026, 6, 5), check_out=date(2026, 6, 9)),
    Booking(guest_id=1, room_id=6, check_in=date(2026, 6, 10), check_out=date(2026, 6, 15)),
    Booking(guest_id=2, room_id=7, check_in=date(2026, 6, 11), check_out=date(2026, 6, 16)),
]

session.add_all(bookings)
session.commit()