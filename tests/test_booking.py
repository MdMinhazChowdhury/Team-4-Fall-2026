# tests/test_booking.py
import unittest
import sys
import os
from unittest import mock #(P:B) needs to restore the price registry

# Add the parent directory's 'src' folder to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models import Movie, Showtime, Booking
from factories import BookingFactory

#(P:B) Stub class to simulate a showtime with controlled seat availability
class StubShowtime:
    def __init__(self, seats):

        self.seats = seats

        self.deducted_seats = 0
        self.movie = Movie(1, "stub Movie", "d", "PG", 90)
        self.date, self.time = "2026-11-01", "7:00 PM"

    
    def get_availability(self):
        return self.seats   

    def update_seats(self, count):

        self.deducted_seats += count

        self.seats -= count

#(P:B) Testing the Movie by itself
class TestMovieUnit(unittest.TestCase):

    def test_sunny_movie_its_details(self):#(P:B) the constructor keeps every value it was given. checking if all 5 values are saved corectly
        
        m = Movie(7, "Arrival", "Sci-Fi", "PG-13", 116)
        
        self.assertEqual((m.movie_id, m.title, m.description, m.rating, m.runtime), (7, "Arrival", "Sci-Fi", "PG-13", 116))

    def test_sunny_movie_info_text(self):
        #(P:B) makes the text for the movie info
        
        m = Movie(7, "Arrival", "Sci-Fi", "PG-13", 116)

        self.assertEqual(m.get_movie_info(), "Arrival (PG-13) - 116 mins")

    def test_boundary_movie_info_shortest_runtime(self):
        #(P:B) text is still correct fot the shortest runtime
        self.assertEqual(Movie(2, "Short", "d", "G", 1).get_movie_info(), "Short (G) - 1 mins")

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

        #(P:B) adding test for sunny

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

    #(P:B) testing at the boundary of 0 seats left, and trying to book 1 more seat
class Testshowtime(unittest.TestCase):
        
    def setUp(self):
        self.showtime = Showtime(1,Movie(1, "Inception", "A mind-bending thriller", "PG-13", 148), "2026-11-01", "7:00 PM", 10)

    def test_sunny_update_seats_removes_seats(self):
        #(P:B) takes 3 seats away (10 ->7)
        self.showtime.update_seats(3)
        self.assertEqual(self.showtime.get_availability(), 7)

    def test_boundary_update_seats_to_zero(self):
        #(P:B) takes all seats away (10 ->0)
        self.showtime.update_seats(10)
        self.assertEqual(self.showtime.get_availability(), 0)

    #(P:B) Booking and booking 
class TestBookingUnitWithStub(unittest.TestCase):

    def test_sunny_booking_cost(self):
           #(P:B) cost = tickets * $12.50 (3 tickets = $37.50)
        self.assertEqual(Booking(1, 1, StubShowtime(10), 3).total_cost, 37.5)

    def test_boundary_booking_cost_one_ticket(self):
            #(P:B) the smallest booking cost is 1 ticket * $12.50 = $12.50
            self.assertEqual(Booking(1, 1, StubShowtime(10), 1).total_cost, 12.5)

    def test_sunny_factory_deducts_seats_once(self):
        #(P:B) the factory deducts seats from the showtime when a booking is created
        stub_showtime = StubShowtime(5)
        booking = BookingFactory.create_booking(1, 1, stub_showtime, 2)
        self.assertEqual(stub_showtime.deducted_seats, 2)
        self.assertEqual(booking.total_cost, 25.0)

    def test_rainy_factory_refuses_and_deducts_nothing(self):
        #(P:B) the factory refuses to create a booking if there are not enough seats, and does not deduct any seats
        stub_showtime = StubShowtime(3)
        with self.assertRaises(ValueError):
            BookingFactory.create_booking(1, 1, stub_showtime, 5) # Requesting 5 when only 3 exist
        self.assertEqual(stub_showtime.deducted_seats, 0) # No seats should be deducted

    def test_boundary_factory_exact_seats(self):
            #(P:B) the factory allows booking exactly the number of available seats, and deducts them
        stub_showtime = StubShowtime(4)
        BookingFactory.create_booking(1, 1, stub_showtime, 4) # Requesting all 4 seats
        self.assertEqual(stub_showtime.deducted_seats, 4)
        self.assertEqual(stub_showtime.get_availability(), 0) # All seats should be deducted

    #(P:B) the REAL Movie, Showtime, Booking and BookingFactory working together
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.movie = Movie(1, "Inception", "A mind-bending thriller", "PG-13", 148)
        self.showtime = Showtime(101, self.movie, "2026-11-01", "7:00 PM", 10)

    def test_sunny_full_booking_flow(self):
        b = BookingFactory.create_booking(1, 7, self.showtime, 3)
        self.assertEqual(b.get_confirmation(), "Booking #1: 3 ticket(s) for Inception on 2026-11-01 at 7:00 PM.")
        self.assertEqual((b.total_cost, self.showtime.get_availability()), (37.5, 7))

    def test_rainy_failed_booking_leaves_seats_unchanged(self):
        #(P:B) SHOWS: a refused booking (5 seats when 4 are left) changes nothing.
        BookingFactory.create_booking(2, 1, self.showtime, 6)
        with self.assertRaises(ValueError):
            BookingFactory.create_booking(3, 2, self.showtime, 5)
        self.assertEqual(self.showtime.get_availability(), 4)

    def test_boundary_last_seat_then_one_too_many(self):
        #(P:B) SHOWS: 9 seats, then the last seat works, then one more fails.
        BookingFactory.create_booking(4, 1, self.showtime, 9)
        BookingFactory.create_booking(5, 2, self.showtime, 1)
        self.assertEqual(self.showtime.get_availability(), 0)
        with self.assertRaises(ValueError):
            BookingFactory.create_booking(6, 3, self.showtime, 1)

if __name__ == '__main__':
    unittest.main()
