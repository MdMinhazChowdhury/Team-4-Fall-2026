# src/factories.py
from models import Booking, Showtime

class BookingFactory:
    @staticmethod
    def create_booking(booking_id: int, customer_id: int, showtime: Showtime, ticket_count: int) -> Booking:
        """
        Factory method to instantiate a Booking object after verifying seat availability.
        """
        if showtime.get_availability() < ticket_count:
            raise ValueError("Not enough available seats for this showtime.")
        
        # Deduct seats upon successful creation
        showtime.update_seats(ticket_count)
        
        # Return the newly instantiated Booking object
        return Booking(booking_id, customer_id, showtime, ticket_count)