from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

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
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            "message": "Bienvenido a CoWorkFlow",
            "access_token": token,
            "refresh_token": refresh_token,
            "user": {
                "full_name": user.full_name,
                "role": user.role
            }
        }), 200

    # 4. Si algo falla, error genérico
    return jsonify({"message": "Credenciales incorrectas"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required() # <--- Esta es la "aduana". Si no hay token, devuelve 401.
def get_profile():
    # Recuperamos el ID que guardamos dentro del token
    current_user_id = get_jwt_identity()
    
    # Buscamos al usuario en la base de datos
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
        
    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "message": "Acceso concedido al perfil protegido"
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_access_token():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    role = user.role if user else 'client'
    new_access_token = create_access_token(
        identity=str(current_user_id),
        additional_claims={"role": role}
    )

    return jsonify({"access_token": new_access_token}), 200

@auth_bp.route('/admin/users/', methods=['GET'])
@jwt_required()
def get_all_users():
    # 1. Extraemos los "claims" adicionales que metimos en el token al hacer login
    claims = get_jwt()
    
    # 2. Verificamos si el rol es 'admin'
    if claims.get("role") != "admin":
        return jsonify({"message": "Acceso denegado: Se requieren permisos de administrador"}), 403

    # 3. Si es admin, listamos todos los usuarios
    users = User.query.all()
    users_list = []
    for u in users:
        users_list.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role
        })
    
    return jsonify(users_list), 200