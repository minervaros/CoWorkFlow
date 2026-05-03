from flask import Blueprint, request, jsonify
from app import db
from app.models import Review

resenas_bp = Blueprint('resenas', __name__)

@resenas_bp.route('/', methods=['GET'])
def obtener_resenas():
    try:
        # Recuperamos todas las reseñas ordenadas por id de forma ascendente
        resenas = Review.query.order_by(Review.id.asc()).all()
        resultado = []
        for r in resenas:
            resultado.append({
                "id": r.id,
                "autor": r.author,
                "puesto": r.position,
                "texto": r.text,
                "estrellas": r.rating
            })
        return jsonify(resultado), 200
    except Exception as e:
        # TODO(security): Log de error detallado en servidor
        print(f"Error al obtener reseñas: {str(e)}")
        return jsonify({"message": "Error al recuperar las reseñas"}), 500

@resenas_bp.route('/', methods=['POST'])
def publicar_resena():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"message": "Faltan datos de la reseña"}), 400

        # Validación estricta de campos (variables en español)
        autor = datos.get('autor')
        puesto = datos.get('puesto')
        texto = datos.get('texto')
        estrellas = datos.get('estrellas')

        if not autor or not isinstance(autor, str) or not autor.strip():
            return jsonify({"message": "El campo 'autor' es obligatorio y no puede estar vacío"}), 400
        if not puesto or not isinstance(puesto, str) or not puesto.strip():
            return jsonify({"message": "El campo 'puesto' es obligatorio y no puede estar vacío"}), 400
        if not texto or not isinstance(texto, str) or not texto.strip():
            return jsonify({"message": "El campo 'texto' es obligatorio y no puede estar vacío"}), 400

        try:
            estrellas_int = int(estrellas)
        except (ValueError, TypeError):
            return jsonify({"message": "El campo 'estrellas' debe ser un número entero válido"}), 400

        if estrellas_int < 1 or estrellas_int > 5:
            return jsonify({"message": "Las estrellas deben ser un número entre 1 y 5"}), 400

        # Uso de ORM para prevenir inyección SQL. Campos en inglés: author, position, text, rating.
        nueva_resena = Review(
            author=autor.strip(),
            position=puesto.strip(),
            text=texto.strip(),
            rating=estrellas_int
        )

        db.session.add(nueva_resena)
        db.session.commit()

        return jsonify({
            "message": "Reseña publicada con éxito",
            "resena": {
                "id": nueva_resena.id,
                "autor": nueva_resena.author,
                "puesto": nueva_resena.position,
                "texto": nueva_resena.text,
                "estrellas": nueva_resena.rating
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        # TODO(security): Log de error detallado en servidor
        print(f"Error al publicar reseña: {str(e)}")
        return jsonify({"message": "Error interno al guardar la reseña"}), 500
