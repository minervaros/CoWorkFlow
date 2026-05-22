import os
import secrets
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app.mailer import send_email

# Creamos el Blueprint para autenticación
auth_bp = Blueprint('auth', __name__)

def enviar_correo_verificacion(destinatario, nombre_completo, token):
    url_frontal = os.getenv('FRONTEND_URL', 'http://localhost:8080').rstrip('/')
    enlace = f"{url_frontal}/verificar-cuenta?token={token}"

    cuerpo = (
        f"Hola {nombre_completo},\n\n"
        "¡Gracias por registrarte en CoWorkFlow!\n\n"
        "Para activar tu cuenta y poder iniciar sesión, por favor haz clic en el siguiente enlace:\n"
        f"{enlace}\n\n"
        "Si no has creado esta cuenta, puedes ignorar este mensaje.\n\n"
        "Un saludo,\n"
        "El equipo de CoWorkFlow"
    )

    return send_email(
        to_email=destinatario,
        to_name=nombre_completo,
        subject="Verifica tu cuenta en CoWorkFlow",
        body=cuerpo,
        sender_name="CoWorkFlow"
    )

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validamos que vengan los datos básicos
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    email = data['email'].strip().lower()

    # Comprobamos si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "El usuario ya está registrado"}), 400

    token = secrets.token_urlsafe(32)

    # Creamos el nuevo usuario usando el modelo que configuramos
    new_user = User(
        full_name=data.get('full_name', 'Usuario CoWork'),
        email=email,
        role=data.get('role', 'client'),
        esta_verificado=False,
        token_verificacion=token
    )
    # Ciframos la contraseña (Seguridad Nivel 4)
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al guardar: {str(e)}"}), 500

    # Enviamos el correo de verificación
    enviado, error_correo = enviar_correo_verificacion(email, new_user.full_name, token)
    if not enviado:
        # Registramos pero avisamos del problema de envío de correo en modo desarrollo
        print(f"Error al enviar correo de verificación: {error_correo}")
        return jsonify({
            "message": "Usuario registrado, pero no se pudo enviar el correo de verificación. Contacta con soporte.",
            "error_correo": error_correo
        }), 201

    return jsonify({"message": "Usuario creado con éxito. Revisa tu correo para verificar tu cuenta."}), 201
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Buscamos al usuario
    user = User.query.filter_by(email=email).first()

    # 2. Comprobamos si existe y si la contraseña es correcta
    if user and user.check_password(password):
        # Verificar si la cuenta está verificada
        if not user.esta_verificado:
            return jsonify({"message": "Por favor, verifica tu cuenta de correo electrónico antes de iniciar sesión. Revisa tu bandeja de entrada."}), 403

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


@auth_bp.route('/verificar-cuenta', methods=['GET'])
def verificar_cuenta():
    token = request.args.get('token')
    if not token:
        return jsonify({"message": "El token de verificación es obligatorio"}), 400

    usuario = User.query.filter_by(token_verificacion=token).first()
    if not usuario:
        return jsonify({"message": "El token de verificación es inválido o ha expirado"}), 400

    usuario.esta_verificado = True
    usuario.token_verificacion = None

    try:
        db.session.commit()
        return jsonify({"message": "Cuenta verificada con éxito. Ya puedes iniciar sesión."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al verificar la cuenta: {str(e)}"}), 500

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

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    if not user.check_password(data['current_password']):
        return jsonify({"message": "La contraseña actual es incorrecta"}), 400

    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify({"message": "Contraseña actualizada con éxito"}), 200

@auth_bp.route('/delete-account', methods=['POST'])
@jwt_required()
def delete_account():
    data = request.get_json()
    if not data or not data.get('password'):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    if not user.check_password(data['password']):
        return jsonify({"message": "La contraseña es incorrecta"}), 400

    from app.models import Booking, TourBooking
    
    try:
        # Borramos las dependencias de este usuario primero
        Booking.query.filter_by(user_id=current_user_id).delete()
        TourBooking.query.filter_by(user_id=current_user_id).delete()
        
        # Borramos al usuario
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Cuenta eliminada con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al eliminar la cuenta: {str(e)}"}), 500