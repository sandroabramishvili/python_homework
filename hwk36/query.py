from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import Hotel, Room, Guest, Booking, engine
from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

def formatter():
    print("-" * 100)

# 5-ვარსკვლავიანი სასტუმროები
five_star = session.query(Hotel).filter(Hotel.stars == 5).all()
print("5-star hotels:", five_star)
formatter()

# თბილისის სასტუმროები
tbilisi_hotels = session.query(Hotel).filter(Hotel.city == 'Tbilisi').all()
print("Tbilisi hotels:", tbilisi_hotels)
formatter()

# 100-ზე იაფი ოთახები
cheap_rooms = session.query(Room).filter(Room.price_per_night < 100).all()
print("Rooms under 100:", cheap_rooms)
formatter()

# კონკრეტული სასტუმროს ოთახები
hotel_rooms = session.query(Room).filter(Room.hotel_id == 1).all()
print("Hotel 1 rooms:", hotel_rooms)
formatter()

# კონკრეტული სტუმრის Booking-ები
guest_bookings = session.query(Booking).filter(Booking.guest_id == 1).all()
print("Guest 1 bookings:", guest_bookings)
formatter()

# მომავალი check_out-ის Booking-ები
future_bookings = session.query(Booking).filter(Booking.check_out > date.today()).all()
print("Future bookings:", future_bookings)
formatter()

# ყველაზე ძვირი ოთახი
priciest_room = session.query(Room).order_by(Room.price_per_night.desc()).first()
print("Most expensive room:", priciest_room)
formatter()

# ოთახების რაოდენობა თითოეულ სასტუმროში
room_counts = session.query(Hotel.name, func.count(Room.id)).join(Room).group_by(Hotel.id).all()
for name, count in room_counts:
    print(f"{name:<20} {count} rooms")
formatter()

# მინიმუმ 3 ოთახის მქონე სასტუმროები
hotels_with_3plus_rooms = session.query(Hotel).join(Room).group_by(Hotel.id).having(func.count(Room.id) >= 3).all()
print("Hotels with 3+ rooms:", hotels_with_3plus_rooms)
formatter()

# ერთზე მეტი Booking-ის მქონე სტუმრები
repeat_guests = session.query(Guest).join(Booking).group_by(Guest.id).having(func.count(Booking.id) > 1).all()
print("Repeat guests:", repeat_guests)
formatter()

# Relationship-ების გამოყენება
hotel = session.query(Hotel).filter(Hotel.name == 'Grand Hotel').first()
print(f"{hotel.name} rooms via relationship:", hotel.rooms)
formatter()

guest = session.query(Guest).filter(Guest.id == 1).first()
print(f"Guest {guest.first_name}'s bookings via relationship:", guest.bookings)
formatter()

booking = session.query(Booking).first()
print(f"Booking {booking.id} guest:", booking.guest)
print(f"Booking {booking.id} room:", booking.room)
formatter()

session.close()