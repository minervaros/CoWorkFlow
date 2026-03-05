from app import create_app

# Aquí llamamos a la función que configuramos en tu __init__.py
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
