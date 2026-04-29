from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager 
from flask_cors import CORS
from datetime import timedelta
import json


load_dotenv()

# Inicializamos la instancia de SQLAlchemy
db = SQLAlchemy()


def seed_sample_rooms():
    from app.models import Room

    salas_muestra = [
        {
            "name": "Sala Ágora",
            "location": "Sede Ruzafa",
            "equipamiento": ["Pantalla 4K", "Pizarra", "Videollamada", "Café incluido"],
            "description": "Sala luminosa para workshops creativos, sesiones de estrategia y dinámicas de equipo.",
            "capacity": 8,
            "price_per_hour": 24,
            "image_url": "https://images.unsplash.com/photo-1497366412874-3415097a27e7?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Turia",
            "location": "Sede Ruzafa",
            "equipamiento": ["Monitor ultrapanorámico", "Wifi premium", "Apple TV"],
            "description": "Espacio ágil para reuniones de producto, entrevistas y trabajo híbrido con clientes.",
            "capacity": 4,
            "price_per_hour": 18,
            "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Mercado",
            "location": "Sede Ruzafa",
            "equipamiento": ["Pizarra", "Videollamada", "Altavoz"],
            "description": "Ideal para reuniones comerciales y revisiones de pipeline con equipos híbridos.",
            "capacity": 6,
            "price_per_hour": 22,
            "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Russafa Hub",
            "location": "Sede Ruzafa",
            "equipamiento": ["Pantalla 4K", "Wifi premium", "Apple TV"],
            "description": "Espacio versátil para demos, reuniones de seguimiento y presentaciones breves.",
            "capacity": 7,
            "price_per_hour": 23,
            "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Creativa",
            "location": "Sede Ruzafa",
            "equipamiento": ["Pizarra", "Mesa modular", "Café incluido"],
            "description": "Diseñada para sesiones de ideación, retrospectivas y talleres colaborativos.",
            "capacity": 9,
            "price_per_hour": 25,
            "image_url": "https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Ruzafa Pro",
            "location": "Sede Ruzafa",
            "equipamiento": ["Proyector", "Videollamada", "Iluminación regulable"],
            "description": "Entorno profesional para reuniones con cliente y toma de decisiones estratégicas.",
            "capacity": 10,
            "price_per_hour": 27,
            "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Muralla",
            "location": "Sede El Carmen",
            "equipamiento": ["Proyector", "Pizarra", "Altavoz"],
            "description": "Ambiente sereno para reuniones ejecutivas, revisiones de negocio y sesiones de planificación.",
            "capacity": 10,
            "price_per_hour": 28,
            "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Lonja",
            "location": "Sede El Carmen",
            "equipamiento": ["Pantalla 4K", "Videollamada", "Iluminación regulable"],
            "description": "Sala elegante para presentaciones con clientes, comités y reuniones de alto impacto.",
            "capacity": 12,
            "price_per_hour": 32,
            "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Quart",
            "location": "Sede El Carmen",
            "equipamiento": ["Pantalla 4K", "Pizarra", "Wifi premium"],
            "description": "Perfecta para reuniones de dirección y coordinación entre departamentos.",
            "capacity": 8,
            "price_per_hour": 26,
            "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Serranos",
            "location": "Sede El Carmen",
            "equipamiento": ["Monitor ultrapanorámico", "Videollamada", "Altavoz"],
            "description": "Sala dinámica para sincronizaciones de producto y revisiones técnicas.",
            "capacity": 6,
            "price_per_hour": 24,
            "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Carme",
            "location": "Sede El Carmen",
            "equipamiento": ["Proyector", "Mesa modular", "Café incluido"],
            "description": "Espacio cómodo para formación interna, entrevistas y reuniones operativas.",
            "capacity": 9,
            "price_per_hour": 27,
            "image_url": "https://images.unsplash.com/photo-1497215842964-222b430dc094?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Plaza Redonda",
            "location": "Sede El Carmen",
            "equipamiento": ["Pantalla táctil", "Videollamada", "Iluminación regulable"],
            "description": "Preparada para presentaciones comerciales y sesiones de validación con clientes.",
            "capacity": 11,
            "price_per_hour": 31,
            "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Eixample One",
            "location": "Sede Eixample",
            "equipamiento": ["Proyector", "Pizarra", "Mesa modular", "Wifi premium"],
            "description": "Configuración flexible para formación interna, workshops y sesiones de sprint planning.",
            "capacity": 14,
            "price_per_hour": 30,
            "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Alameda",
            "location": "Sede Eixample",
            "equipamiento": ["Pantalla táctil", "Sonido envolvente", "Videollamada"],
            "description": "Perfecta para demos, reuniones de ventas y sesiones con soporte audiovisual avanzado.",
            "capacity": 6,
            "price_per_hour": 26,
            "image_url": "https://images.unsplash.com/photo-1517502884422-41eaead166d4?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Colón",
            "location": "Sede Eixample",
            "equipamiento": ["Pantalla 4K", "Videollamada", "Pizarra"],
            "description": "Excelente para demos de producto, kick-offs y sesiones de seguimiento semanal.",
            "capacity": 8,
            "price_per_hour": 27,
            "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Reino",
            "location": "Sede Eixample",
            "equipamiento": ["Monitor 32\"", "Wifi premium", "Apple TV"],
            "description": "Sala compacta para reuniones de análisis, entrevistas y coordinación rápida.",
            "capacity": 5,
            "price_per_hour": 21,
            "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Cánovas",
            "location": "Sede Eixample",
            "equipamiento": ["Proyector", "Altavoz", "Café incluido"],
            "description": "Entorno tranquilo para planificación trimestral y reuniones de liderazgo.",
            "capacity": 10,
            "price_per_hour": 29,
            "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Gran Vía",
            "location": "Sede Eixample",
            "equipamiento": ["Pantalla táctil", "Videollamada", "Sonido envolvente"],
            "description": "Pensada para presentaciones de alto impacto y sesiones con stakeholders.",
            "capacity": 12,
            "price_per_hour": 33,
            "image_url": "https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Mediterráneo",
            "location": "Sede Cabanyal",
            "equipamiento": ["Luz natural", "Pizarra", "Café incluido"],
            "description": "Espacio relajado e inspirador para sesiones creativas, mentoring y trabajo profundo.",
            "capacity": 5,
            "price_per_hour": 20,
            "image_url": "https://images.unsplash.com/photo-1497215842964-222b430dc094?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Brisa",
            "location": "Sede Cabanyal",
            "equipamiento": ["Monitor 32\"", "Videollamada", "Cabina acústica cercana"],
            "description": "Sala compacta para reuniones uno a uno, coaching y trabajo enfocado cerca del mar.",
            "capacity": 3,
            "price_per_hour": 16,
            "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Marina",
            "location": "Sede Cabanyal",
            "equipamiento": ["Pantalla 4K", "Videollamada", "Wifi premium"],
            "description": "Ideal para reuniones de planificación de campañas y coordinación de equipos distribuidos.",
            "capacity": 7,
            "price_per_hour": 22,
            "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Atarazanas",
            "location": "Sede Cabanyal",
            "equipamiento": ["Proyector", "Pizarra", "Altavoz"],
            "description": "Para workshops prácticos, formación interna y reuniones de ejecución.",
            "capacity": 9,
            "price_per_hour": 24,
            "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Levante",
            "location": "Sede Cabanyal",
            "equipamiento": ["Monitor ultrapanorámico", "Apple TV", "Iluminación regulable"],
            "description": "Sala moderna para revisión de métricas, producto y decisiones de roadmap.",
            "capacity": 6,
            "price_per_hour": 23,
            "image_url": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sala Arenas",
            "location": "Sede Cabanyal",
            "equipamiento": ["Pantalla táctil", "Sonido envolvente", "Café incluido"],
            "description": "Excelente para sesiones con clientes, demos y cierre de propuestas.",
            "capacity": 10,
            "price_per_hour": 28,
            "image_url": "https://images.unsplash.com/photo-1517502884422-41eaead166d4?q=80&w=1200&auto=format&fit=crop"
        }
    ]

    nombres_existentes = {nombre for (nombre,) in db.session.query(Room.name).all()}
    nuevas_salas = []

    for sala in salas_muestra:
        if sala["name"] in nombres_existentes:
            continue

        nuevas_salas.append(
            Room(
                name=sala["name"],
                location=sala["location"],
                equipamiento=json.dumps(sala["equipamiento"], ensure_ascii=False),
                description=sala["description"],
                capacity=sala["capacity"],
                price_per_hour=sala["price_per_hour"],
                is_active=True,
                image_url=sala["image_url"]
            )
        )

    if nuevas_salas:
        db.session.add_all(nuevas_salas)
        db.session.commit()

    sedes_objetivo = {sala["location"] for sala in salas_muestra}
    nombres_objetivo = {sala["name"] for sala in salas_muestra}

    for sede in sedes_objetivo:
        salas_activas = (
            db.session.query(Room)
            .filter(Room.location == sede, Room.is_deleted == False)
            .order_by(Room.id.asc())
            .all()
        )

        excedente = len(salas_activas) - 6
        if excedente <= 0:
            continue

        salas_no_semilla = [sala for sala in salas_activas if sala.name not in nombres_objetivo]
        salas_semilla = [sala for sala in salas_activas if sala.name in nombres_objetivo]

        a_desactivar = salas_no_semilla[:excedente]
        faltan = excedente - len(a_desactivar)

        if faltan > 0:
            a_desactivar.extend(salas_semilla[:faltan])

        for sala in a_desactivar:
            sala.is_deleted = True

    db.session.commit()

def create_app():

    app = Flask(__name__)
    CORS(app)

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY') 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt = JWTManager(app)

    # Configuramos la URI de la base de datos usando variables de entorno (soporta Clever Cloud y local)
    # mysql+pymysql://usuario:password@host:port/nombre_db
    import urllib.parse
    user = os.getenv('MYSQL_ADDON_USER', 'root')
    password = os.getenv('MYSQL_ADDON_PASSWORD', os.getenv('DB_ROOT_PASSWORD', ''))
    host = os.getenv('MYSQL_ADDON_HOST', 'db')
    port = os.getenv('MYSQL_ADDON_PORT', '3306')
    dbname = os.getenv('MYSQL_ADDON_DB', os.getenv('DB_NAME'))
    
    safe_password = urllib.parse.quote_plus(password) if password else ''
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{dbname}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Iniciamos la base de datos con la app que configuramos
    db.init_app(app)

    # Importamos los modelos para que SQLAlchemy los conozca
    from app import models

    # Creamos las tablas si no existen
    with app.app_context():
        db.create_all()
        columns_result = db.session.execute(db.text("SHOW COLUMNS FROM rooms"))
        room_columns = [row[0] for row in columns_result]
        if 'location' not in room_columns:
            db.session.execute(db.text('ALTER TABLE rooms ADD COLUMN location VARCHAR(255) NULL'))
            db.session.commit()
        if 'equipamiento' not in room_columns:
            db.session.execute(db.text('ALTER TABLE rooms ADD COLUMN equipamiento TEXT NULL'))
            db.session.commit()
        if 'is_deleted' not in room_columns:
            db.session.execute(db.text('ALTER TABLE rooms ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE'))
            db.session.commit()

        booking_columns_result = db.session.execute(db.text("SHOW COLUMNS FROM bookings"))
        booking_columns = [row[0] for row in booking_columns_result]
        if 'payment_status' not in booking_columns:
            db.session.execute(db.text("ALTER TABLE bookings ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending'"))
            db.session.commit()
        if 'payment_method' not in booking_columns:
            db.session.execute(db.text("ALTER TABLE bookings ADD COLUMN payment_method VARCHAR(20) DEFAULT 'reception'"))
            db.session.commit()

        seed_sample_rooms()


    @app.route('/')
    def index():
        return "<h1>¡CoWorkFlow Vivo!</h1><p>Arquitectura profesional con <b>SQLAlchemy ORM</b>.</p>"

    @app.route('/api/health')
    def health_check():
        try:
            # Comprobación de salud usando el ORM
            db.session.execute(db.text('SELECT 1'))
            return {"status": "success", "message": "Conexión MySQL OK (SQLAlchemy)"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    # Registramos el Blueprint de autenticación
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Registramos el Blueprint de salas
    from app.rooms import rooms_bp
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')

    # Registramos el Blueprint de reservas
    from app.bookings import bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')

    # Registramos el Blueprint de contacto (formulario + envío SMTP)
    from app.contact import contact_bp
    app.register_blueprint(contact_bp, url_prefix='/api/contact')

    return app

