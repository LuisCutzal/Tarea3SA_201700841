from flask import Blueprint, jsonify, request
from connection import get_db_connection

ci_bp = Blueprint('ci_bp', __name__)

# Obtener una relación específica por ID
def get_relationship(relationship_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT R.Id, R.RelationshipType,
                   FromCI.Id AS FromId, FromCI.Name AS FromName,
                   ToCI.Id AS ToId, ToCI.Name AS ToName
            FROM CIRelationship R
            JOIN CI AS FromCI ON R.FromCIId = FromCI.Id
            JOIN CI AS ToCI ON R.ToCIId = ToCI.Id
            WHERE R.Id = ?
        """, relationship_id)

        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Relación no encontrada'}), 404

        return jsonify({
            'relationship_id': row.Id,
            'type': row.RelationshipType,
            'from_ci': {
                'id': row.FromId,
                'name': row.FromName
            },
            'to_ci': {
                'id': row.ToId,
                'name': row.ToName
            }
        })
    except Exception as e:
        print("Error al obtener relación:", e)
        return jsonify({'error': 'Error al consultar la relación'}), 500
    finally:
        cursor.close()
        conn.close()

# Crear una nueva relación
def create_relationship(from_id):
    data = request.json
    to_id = data.get('to_id')
    relationship_type = data.get('type', '')
    if not to_id:
        return jsonify({'error': 'Falta el campo to_id'}), 400
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    try:
        # Validar que ambos CIs existan
        cursor.execute("SELECT Id FROM CI WHERE Id = ?", from_id)
        if not cursor.fetchone():
            return jsonify({'error': f'CI origen (ID {from_id}) no encontrado'}), 404

        cursor.execute("SELECT Id FROM CI WHERE Id = ?", to_id)
        if not cursor.fetchone():
            return jsonify({'error': f'CI destino (ID {to_id}) no encontrado'}), 404
        # Insertar relación
        cursor.execute("""
            INSERT INTO CIRelationship (FromCIId, ToCIId, RelationshipType)
            VALUES (?, ?, ?)
        """, (from_id, to_id, relationship_type))
        conn.commit()
        return jsonify({'message': 'Relación creada correctamente'}), 201
    except Exception as e:
        print("Error al crear relación:", e)
        return jsonify({'error': 'Error al crear la relación'}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar una relación por ID
def delete_relationship(relationship_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    try:
        # Verificar si existe
        cursor.execute("SELECT Id FROM CIRelationship WHERE Id = ?", relationship_id)
        if not cursor.fetchone():
            return jsonify({'error': 'Relación no encontrada'}), 404
        # Eliminar
        cursor.execute("DELETE FROM CIRelationship WHERE Id = ?", relationship_id)
        conn.commit()
        return jsonify({'message': f'Relación {relationship_id} eliminada correctamente'})
    except Exception as e:
        print("Error al eliminar relación:", e)
        return jsonify({'error': 'Error al eliminar la relación'}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar una relación (solo tipo de relación)
def update_relationship(relationship_id, data):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    new_type = data.get('type')
    if not new_type:
        return jsonify({'error': 'El campo "type" es obligatorio'}), 400
    try:
        cursor.execute("SELECT Id FROM CIRelationship WHERE Id = ?", relationship_id)
        if not cursor.fetchone():
            return jsonify({'error': 'Relación no encontrada'}), 404
        cursor.execute("""
            UPDATE CIRelationship
            SET RelationshipType = ?
            WHERE Id = ?
        """, new_type, relationship_id)
        conn.commit()
        return jsonify({'message': f'Tipo de relación actualizado a "{new_type}"'})
    except Exception as e:
        print("Error al actualizar relación:", e)
        return jsonify({'error': 'Error al actualizar la relación'}), 500
    finally:
        cursor.close()
        conn.close()