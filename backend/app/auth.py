from flask import Blueprint, request, jsonify
from app import db
from app.models import User

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