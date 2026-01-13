from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargamos variables de entorno del archivo .env
load_dotenv()

# Inicializamos MySQL
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    app.config['MYSQL_HOST'] = 'db'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_ROOT_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Inicializamos la base de datos con la configuración de esta app
    mysql.init_app(app)

    # Una ruta de prueba para verificar la conexión
    @app.route('/api/health')
    def health_check():
        try:
            # Intentamos una consulta simple a MySQL
            cur = mysql.connection.cursor()
            cur.execute('SELECT 1')
            cur.close()
            return {"status": "success", "message": "Conexión con MySQL establecida correctamente"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    return app
