from flask import Blueprint, request
from services.ci_service import (
    get_all_cis,get_especific_ci,create_ci_,get_relationships,update_ci,get_ci_change_log
    )

ci_bp = Blueprint('ci_bp', __name__)

@ci_bp.route('/cis', methods=['GET'])
def get_cis():
    return get_all_cis()

@ci_bp.route('/cis/<int:ci_id>', methods=['GET'])
def get_ci(ci_id):
    return get_especific_ci(ci_id)

@ci_bp.route('/cis', methods=['POST'])
def create_ci():
    data = request.json
    return create_ci_(data)

@ci_bp.route('/cis/<int:ci_id>/relationships', methods=['GET'])
def get_ci_relationships(ci_id):
    return get_relationships(ci_id)

@ci_bp.route('/cis/<int:ci_id>', methods=['PUT'])
def update_ci_route(ci_id):
    data = request.json
    return update_ci(ci_id, data)


@ci_bp.route('/cis/<int:ci_id>/changes', methods=['GET'])
def get_ci_changes(ci_id):
    return get_ci_change_log(ci_id)