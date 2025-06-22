from flask import Blueprint, jsonify, request
from connection import get_db_connection

ci_bp = Blueprint('ci_bp', __name__)

# Obtener todos los CIs
def get_all_cis():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    query = """
        SELECT CI.Id, CI.Name, CI.Description, CI.CurrentStatus, CIType.Name AS TypeName, CI.Environment
        FROM CI
        JOIN CIType ON CI.TypeId = CIType.Id
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        cis = []
        for row in rows:
            cis.append({
                'id': row.Id,
                'name': row.Name,
                'description': row.Description,
                'type': row.TypeName,
                'status': row.CurrentStatus,
                'environment': row.Environment
            })
        return jsonify(cis)
    except Exception as e:
        print("Error al obtener CIs:", e)
        return jsonify({'error': 'Error al consultar los CIs'}), 500
    finally:
        cursor.close()
        conn.close()

def get_especific_ci(ci_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    query = """
        SELECT CI.Id, CI.Name, CI.Description, CIType.Name AS TypeName, CI.Environment
        FROM CI
        JOIN CIType ON CI.TypeId = CIType.Id
        WHERE CI.Id = ?
    """
    try:
        cursor.execute(query, (ci_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'CI no encontrado'}), 404
        ci = {
            'id': row.Id,
            'name': row.Name,
            'description': row.Description,
            'type': row.TypeName,
            'environment': row.Environment
        }
    except Exception as e:
        print("Error al obtener CI:", e)
        return jsonify({'error': 'Error al consultar el CI'}), 500
    finally:
        cursor.close()
        conn.close()
    return jsonify(ci)

# Crear un nuevo CI
def create_ci_():
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    type_name = data.get('type', '').lower()
    environment = data.get('environment')
    if environment not in ['DEV', 'QA', 'PROD']:
        return jsonify({'error': 'El campo "environment" debe ser DEV, QA o PROD'}), 400
    if not name or not type_name:
        return jsonify({'error': 'Faltan campos obligatorios: name y type'}), 400
    # Validaciones por tipo de CI
    required_fields_by_type = {
        'servidor': ['serial_number', 'acquisition_date', 'owner'],
        'base de datos': ['version', 'owner'],
        'aplicación': ['version', 'config_status']
    }
    missing_fields = []
    required = required_fields_by_type.get(type_name, [])
    for field in required:
        if not data.get(field):
            missing_fields.append(field)
    if missing_fields:
        return jsonify({'error': f'Faltan campos para tipo "{type_name}": {", ".join(missing_fields)}'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Verificar o insertar el tipo
    cursor.execute("SELECT Id FROM CIType WHERE Name = ?", type_name)
    row = cursor.fetchone()
    if row:
        type_id = row.Id
    else:
        cursor.execute("INSERT INTO CIType (Name) VALUES (?)", type_name)
        cursor.execute("SELECT SCOPE_IDENTITY()")
        type_id = cursor.fetchone()[0]
    # Insertar el CI
    cursor.execute("""
        INSERT INTO CI (
            Name, Description, SerialNumber, Version, AcquisitionDate,
            CurrentStatus, PhysicalLocation, Owner, SecurityLevel,
            Compliance, ConfigStatus, LicenseNumber, ExpirationDate, TypeId,Environment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """, (
        name,
        description,
        data.get('serial_number'),
        data.get('version'),
        data.get('acquisition_date'),
        data.get('current_status'),
        data.get('physical_location'),
        data.get('owner'),
        data.get('security_level'),
        data.get('compliance'),
        data.get('config_status'),
        data.get('license_number'),
        data.get('expiration_date'),
        type_id,
        environment
    ))
    cursor.execute("SELECT SCOPE_IDENTITY()")
    ci_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': ci_id, 'message': 'CI creado'}), 201

# Obtener relaciones de un CI (salientes y entrantes)
def get_relationships(ci_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    try:
        # Relación saliente
        cursor.execute("""
            SELECT R.Id, R.RelationshipType, CI.Id, CI.Name
            FROM CIRelationship R
            JOIN CI ON R.ToCIId = CI.Id
            WHERE R.FromCIId = ?
        """, ci_id)
        salientes = [{
            'relationship_id': row.Id,
            'type': row.RelationshipType,
            'direction': 'outgoing',
            'target_ci': {
                'id': row.Id,
                'name': row.Name
            }
        } for row in cursor.fetchall()]
        # Relación entrante
        cursor.execute("""
            SELECT R.Id, R.RelationshipType, CI.Id, CI.Name
            FROM CIRelationship R
            JOIN CI ON R.FromCIId = CI.Id
            WHERE R.ToCIId = ?
        """, ci_id)
        entrantes = [{
            'relationship_id': row.Id,
            'type': row.RelationshipType,
            'direction': 'incoming',
            'source_ci': {
                'id': row.Id,
                'name': row.Name
            }
        } for row in cursor.fetchall()]

        return jsonify({
            'relationships': salientes + entrantes
        })
    except Exception as e:
        print("Error al obtener relaciones:", e)
        return jsonify({'error': 'Error al consultar las relaciones'}), 500
    finally:
        cursor.close()
        conn.close()

def update_ci(ci_id, data):
    name = data.get('name')
    description = data.get('description')
    status = data.get('status')
    changed_by = data.get('changed_by')  # puede ser un nombre o ID de usuario

    if not changed_by:
        return jsonify({'error': 'El campo "changed_by" es obligatorio'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar que el CI existe
        cursor.execute("SELECT * FROM CI WHERE Id = ?", ci_id)
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'CI no encontrado'}), 404

        # Construir descripción del cambio
        cambios = []
        if name and name != row.Name:
            cambios.append(f'Nombre: {row.Name} → {name}')
        if description and description != row.Description:
            cambios.append(f'Descripción: {row.Description} → {description}')
        if status and status != row.CurrentStatus:
            cambios.append(f'Estado: {row.CurrentStatus} → {status}')

        if not cambios:
            return jsonify({'message': 'No hay cambios para registrar'}), 200

        # Actualizar el CI
        cursor.execute("""
            UPDATE CI SET Name = ?, Description = ?, CurrentStatus = ?, UpdatedAt = GETDATE()
            WHERE Id = ?
        """, name, description, status, ci_id)

        # Insertar en CIChangeLog
        cursor.execute("""
            INSERT INTO CIChangeLog (CIId, ChangeDescription, ChangedBy)
            VALUES (?, ?, ?)
        """, ci_id, "; ".join(cambios), changed_by)

        conn.commit()
        return jsonify({'message': 'CI actualizado y cambio registrado'}), 200

    except Exception as e:
        print("Error al actualizar CI:", e)
        return jsonify({'error': 'Error interno'}), 500

    finally:
        cursor.close()
        conn.close()

def get_ci_change_log(ci_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ChangeDescription, ChangedBy, ChangeDate
            FROM CIChangeLog
            WHERE CIId = ?
            ORDER BY ChangeDate DESC
        """, ci_id)

        rows = cursor.fetchall()
        changes = [{
            'description': row.ChangeDescription,
            'changed_by': row.ChangedBy,
            'change_date': row.ChangeDate.strftime('%Y-%m-%d %H:%M:%S')
        } for row in rows]

        return jsonify(changes), 200

    except Exception as e:
        print("❌ Error al obtener el historial:", e)
        return jsonify({'error': 'Error al obtener historial'}), 500

    finally:
        cursor.close()
        conn.close()