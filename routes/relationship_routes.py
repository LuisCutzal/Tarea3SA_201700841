from flask import Blueprint, request, jsonify
from services.relationship_service import (
    get_relationship as get_relationship_by_id,
    delete_relationship as delete_relationship_by_id,
    create_relationship as create_relationship_entry,
    get_relationship as get_relationships_for_ci,
    update_relationship as update_relationship_entry
)

relationship_bp = Blueprint('relationship_bp', __name__)

@relationship_bp.route('/cis/<int:from_id>/relationships', methods=['POST'])
def create_relationship(from_id):
    data = request.json
    return create_relationship_entry(from_id, data)

@relationship_bp.route('/relationships/<int:relationship_id>', methods=['GET'])
def get_relationship(relationship_id):
    return get_relationship_by_id(relationship_id)

@relationship_bp.route('/relationships/<int:relationship_id>', methods=['DELETE'])
def delete_relationship(relationship_id):
    return delete_relationship_by_id(relationship_id)

@relationship_bp.route('/relationships/<int:relationship_id>', methods=['PUT'])
def update_relationship(relationship_id):
    data = request.json
    return update_relationship_entry(relationship_id, data)