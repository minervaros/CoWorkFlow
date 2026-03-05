from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializamos la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

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

    return app




# from flask import Flask
# from flask_mysqldb import MySQL
# import os
# from dotenv import load_dotenv

# # Cargamos variables de entorno del archivo .env
# load_dotenv()

# # Inicializamos MySQL
# mysql = MySQL()

# def create_app():
#     app = Flask(__name__)

#     # Configuración desde variables de entorno
#     app.config['MYSQL_HOST'] = 'db'
#     app.config['MYSQL_USER'] = 'root'
#     app.config['MYSQL_PASSWORD'] = os.getenv('DB_ROOT_PASSWORD')
#     app.config['MYSQL_DB'] = os.getenv('DB_NAME')
#     app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

#     # Inicializamos la base de datos con la configuración de esta app
#     mysql.init_app(app)

#     @app.route('/')
#     def index():
#         return "<h1>¡CoWorkFlow Vivo!</h1><p>Estás en la raíz de la API.</p>"

#     # Una ruta de prueba para verificar la conexión
#     @app.route('/api/health')
#     def health_check():
#         try:
#             # Intentamos una consulta simple a MySQL
#             cur = mysql.connection.cursor()
#             cur.execute('SELECT 1')
#             cur.close()
#             return {"status": "success", "message": "Conexión con MySQL establecida correctamente"}, 200
#         except Exception as e:
#             return {"status": "error", "message": str(e)}, 500

#     return app
