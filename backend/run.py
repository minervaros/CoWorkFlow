from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuramos MySQL
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('DB_ROOT_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql = MySQL(app)

# Definimos una ruta simple para probar
@app.route('/')
def hello():
    try:
        # Intentamos una conexión simple
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return "<h1>¡CoWorkFlow Vivo!</h1><p>Conexión a MySQL: <b>EXITOSA</b></p>"
    except Exception as e:
        return f"<h1>Error</h1><p>No se pudo conectar a la base de datos: {str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)