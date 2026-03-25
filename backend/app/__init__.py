from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager 

load_dotenv()

# Inicializamos la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY') 
    jwt = JWTManager(app)

    # Configuramos la URI de la base de datos usando variables de entorno
    # mysql+pymysql://usuario:password@host/nombre_db
    user = 'root'
    password = os.getenv('DB_ROOT_PASSWORD')
    host = 'db'
    dbname = os.getenv('DB_NAME')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Iniciamos la base de datos con la app que configuramos
    db.init_app(app)

    # Importamos los modelos para que SQLAlchemy los conozca
    from app import models

    # Creamos las tablas si no existen
    with app.app_context():
        db.create_all()


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

    return app

