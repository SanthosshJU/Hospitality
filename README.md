# Hospitality
Overview  This is a simple hotel management system built using Flask and SQLite. It provides RESTful API endpoints for managing guests, room bookings, check-ins, and checkouts.

Hotel Management System (Flask + SQLite)

Overview

This is a simple hotel management system built using Flask and SQLite. It provides RESTful API endpoints for managing guests, room bookings, check-ins, and checkouts.

Features

Guest Registration: Register new guests with unique emails and phone numbers.

Room Booking: Book available rooms for registered guests.

Check-in and Check-out: Manage guest check-ins and checkouts.

View Bookings: Retrieve a list of all bookings with relevant details.

Technologies Used

Python

Flask

Flask-SQLAlchemy

SQLite

Installation

Clone the repository:

git clone <repository_url>
cd <project_directory>

Install dependencies:

pip install flask flask-sqlalchemy

Run the application:

python app.py

API Endpoints

Register Guest: POST /register_guest

Request Body:

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}

Book Room: POST /book_room

Request Body:

{
  "guest_id": 1,
  "room_number": "101",
  "check_in": "2025-03-25"
}

Check Out: PUT /checkout/<booking_id>

View Bookings: GET /view_bookings

License

This project is open-source and free to use.
