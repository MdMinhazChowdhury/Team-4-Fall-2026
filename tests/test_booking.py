# tests/test_booking.py
import unittest
import sys
import os

# Add the parent directory's 'src' folder to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models import Movie, Showtime, Booking
from factories import BookingFactory

class TestBookingSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up a clean sample movie and showtime instance before each test."""
        self.movie = Movie(1, "Inception", "A mind-bending thriller", "PG-13", 148)
        self.showtime = Showtime(101, self.movie, "2026-11-01", "7:00 PM", 10) # Starts with 10 seats

    def test_sunny_day_booking(self):
        """Sunny Day Test: Successfully book a standard number of seats."""
        booking = BookingFactory.create_booking(1001, 501, self.showtime, 2)
        
        self.assertEqual(booking.ticket_count, 2)
        self.assertEqual(booking.total_cost, 25.0)
        self.assertEqual(self.showtime.get_availability(), 8) # 10 - 2 = 8 seats left
        self.assertEqual(booking.status, "Confirmed")

    def test_rainy_day_overbooking(self):
        """Rainy Day Test: Attempting to book more seats than available should raise an error."""
        with self.assertRaises(ValueError) as context:
            BookingFactory.create_booking(1002, 502, self.showtime, 15) # Requesting 15 when only 10 exist
        
        self.assertEqual(str(context.exception), "Not enough available seats for this showtime.")

    def test_boundary_condition_exact_seats(self):
        """Boundary Test: Book the exact number of all remaining available seats."""
        booking = BookingFactory.create_booking(1003, 503, self.showtime, 10) # Requesting all 10 seats
        
        self.assertEqual(booking.ticket_count, 10)
        self.assertEqual(self.showtime.get_availability(), 0) # Exactly 0 seats left


if __name__ == '__main__':
    unittest.main()