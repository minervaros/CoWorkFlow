from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token

# Creamos el Blueprint para autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validamos que vengan los datos básicos
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    # Comprobamos si el usuario ya existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "El usuario ya está registrado"}), 400

    # Creamos el nuevo usuario usando el modelo que configuramos
    new_user = User(
        full_name=data.get('full_name', 'Usuario CoWork'),
        email=data['email'],
        role=data.get('role', 'client')
    )
    # Ciframos la contraseña (Seguridad Nivel 4)
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al guardar: {str(e)}"}), 500
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Buscamos al usuario
    user = User.query.filter_by(email=email).first()

    # 2. Comprobamos si existe y si la contraseña es correcta
    if user and user.check_password(password):
        # 3. Creamos la "llave" (Token)
        # Guardamos el ID del usuario y su rol dentro del token
        token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role}
        )
        
        return jsonify({
            "message": "Bienvenido a CoWorkFlow",
            "access_token": token,
            "user": {
                "full_name": user.full_name,
                "role": user.role
            }
        }), 200

    # 4. Si algo falla, error genérico
    return jsonify({"message": "Credenciales incorrectas"}), 401