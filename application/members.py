# from flask import Blueprint, jsonify, request, abort
# from typing import Dict, Any
# import uuid
#
# members_bp = Blueprint('members', __name__)
#
# members: Dict[str, Dict[str, Any]] = {}
#
# @members_bp.route('/', methods=['POST'])
# def create_member():
#     data = request.json
#     if not data or 'name' not in data:
#         abort(400, 'Invalid member data.')
#
#     member_id = str(uuid.uuid4())
#     members[member_id] = {
#         'id': member_id,
#         'name': data['name'],
#     }
#     return jsonify(members[member_id]), 201
#
# @members_bp.route('/<member_id>', methods=['GET'])
# def get_member(member_id):
#     if member_id not in members:
#         abort(404, 'Member not found.')
#     return jsonify(members[member_id])





from flask import Blueprint, jsonify, request, abort
from .models import Member
from . import db
import uuid

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['POST'])
def create_member():
    data = request.json
    if not data or 'name' not in data:
        abort(400, 'Invalid member data.')

    member_id = str(uuid.uuid4())
    new_member = Member(id=member_id, name=data['name'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'id': new_member.id, 'name': new_member.name}), 201

@members_bp.route('/<member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        abort(404, 'Member not found.')
    return jsonify({'id': member.id, 'name': member.name})
