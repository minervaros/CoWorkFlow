from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='client') # 'admin' o 'client'
    esta_verificado = db.Column(db.Boolean, default=False, nullable=False)
    token_verificacion = db.Column(db.String(100), nullable=True)

    # Método para cifrar la contraseña (Seguridad Nivel 4)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar la contraseña al hacer login
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    equipamiento = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Room {self.name}>'

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed') # confirmed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # paid, pending, reception
    payment_method = db.Column(db.String(20), default='reception')  # platform, reception

    # Opcional: Relaciones para acceder fácil desde el objeto
    user = db.relationship('User', backref='bookings')
    room = db.relationship('Room', backref='bookings')

    def __repr__(self):
        return f'<Booking User:{self.user_id} Room:{self.room_id}>'


class TourBooking(db.Model):
    __tablename__ = 'tour_bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sede_slug = db.Column(db.String(50), nullable=False, index=True)
    sede_name = db.Column(db.String(120), nullable=False)

    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    people_count = db.Column(db.Integer, nullable=False, default=1)
    company_name = db.Column(db.String(160), nullable=False)

    status = db.Column(db.String(20), default='requested')  # requested, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='tour_bookings')

    def __repr__(self):
        return f'<TourBooking User:{self.user_id} Sede:{self.sede_slug}>'