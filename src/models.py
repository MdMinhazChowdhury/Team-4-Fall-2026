# src/models.py

class Movie:
    def __init__(self, movie_id: int, title: str, description: str, rating: str, runtime: int):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.rating = rating
        self.runtime = runtime

    def get_movie_info(self) -> str:
        return f"{self.title} ({self.rating}) - {self.runtime} mins"


class Showtime:
    def __init__(self, showtime_id: int, movie: Movie, date: str, time: str, available_seats: int):
        self.showtime_id = showtime_id
        self.movie = movie
        self.date = date
        self.time = time
        self.available_seats = available_seats

    def get_availability(self) -> int:
        return self.available_seats

    def update_seats(self, count: int):
        self.available_seats -= count


class Booking:
    def __init__(self, booking_id: int, customer_id: int, showtime: Showtime, ticket_count: int):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.showtime = showtime
        self.ticket_count = ticket_count
        self.total_cost = self.calculate_cost()
        self.status = "Confirmed"

    def calculate_cost(self) -> float:
        # Example pricing logic: $12.50 per ticket
        return self.ticket_count * 12.50

    def get_confirmation(self) -> str:
        return f"Booking #{self.booking_id}: {self.ticket_count} ticket(s) for {self.showtime.movie.title} on {self.showtime.date} at {self.showtime.time}."