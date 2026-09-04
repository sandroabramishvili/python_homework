from sqlalchemy import Date, create_engine, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from datetime import date

engine = create_engine('postgresql+psycopg2://postgres:madagascar@localhost:5432/hwk36',)

class Base(DeclarativeBase):
    pass

class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=False)

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="hotel", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Hotel id = {self.id} name = {self.name} country = {self.country} city = {self.city} stars = {self.stars}"


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_number: Mapped[str] = mapped_column(String(100), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)
    hotel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hotel.id", ondelete="CASCADE"), nullable=False
    )

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Room id = {self.id} room_number = {self.room_number} floor = {self.floor} price_per_night = {self.price_per_night} hotel_id = {self.hotel_id}"


class Guest(Base):
    __tablename__ = 'guest'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="guest", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Guest id = {self.id} first_name = {self.first_name} last_name = {self.last_name} email = {self.email} phone = {self.phone}"


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guest_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("guest.id", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False
    )
    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)

    guest: Mapped["Guest"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="bookings")

    def __repr__(self):
        return f"Booking id = {self.id} guest_id = {self.guest_id} room_id = {self.room_id} check_in = {self.check_in} check_out = {self.check_out}"


Base.metadata.create_all(engine)