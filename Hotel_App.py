from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Available')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=True)
    total_amount = db.Column(db.Float, default=0.0)

# Routes
@app.route('/register_guest', methods=['POST'])
def register_guest():
    data = request.json
    new_guest = Guest(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_guest)
    db.session.commit()
    return jsonify({'message': 'Guest registered successfully!'})

@app.route('/book_room', methods=['POST'])
def book_room():
    data = request.json
    room = Room.query.filter_by(room_number=data['room_number'], status='Available').first()
    if not room:
        return jsonify({'message': 'Room not available!'}), 400
    new_booking = Booking(
        guest_id=data['guest_id'],
        room_id=room.id,
        check_in=datetime.strptime(data['check_in'], '%Y-%m-%d')
    )
    room.status = 'Booked'
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': f'Room {room.room_number} booked successfully!'})

@app.route('/checkout/<int:booking_id>', methods=['PUT'])
def checkout(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking or booking.check_out:
        return jsonify({'message': 'Invalid or already checked-out booking!'}), 400
    booking.check_out = datetime.now()
    room = Room.query.get(booking.room_id)
    room.status = 'Available'
    db.session.commit()
    return jsonify({'message': f'Guest checked out successfully from Room {room.room_number}!'})

@app.route('/view_bookings', methods=['GET'])
def view_bookings():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        output.append({
            'booking_id': booking.id,
            'guest_id': booking.guest_id,
            'room_id': booking.room_id,
            'check_in': booking.check_in.strftime('%Y-%m-%d %H:%M:%S'),
            'check_out': booking.check_out.strftime('%Y-%m-%d %H:%M:%S') if booking.check_out else None
        })
    return jsonify(output)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
