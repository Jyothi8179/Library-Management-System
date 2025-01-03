

from flask import Blueprint, jsonify, request, abort
from typing import Dict
import uuid

auth_bp = Blueprint('auth', __name__)

sessions: Dict[str, str] = {}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'member_id' not in data:
        abort(400, 'Invalid login credentials.')

    token = str(uuid.uuid4())
    sessions[token] = data['member_id']
    return jsonify({'token': token})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if token in sessions:
        del sessions[token]
    return '', 204