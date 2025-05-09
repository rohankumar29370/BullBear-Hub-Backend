from flask import Blueprint, jsonify, request

from app.services.user_dao import create_user, get_all, password_matches

user_bp = Blueprint('user', __name__)

@user_bp.route('/get-all')
def get_all_users():
    try:
        users = get_all()
        users_dicts = [user.to_dict() for user in users]
        return jsonify(users_dicts), 200 #Basically retruning a tuple of the response and the status code.
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/add-user', methods = ['POST'])
def add_user():
    try:
        data = request.get_json()
        create_user(data.get('username'), data.get('password'), data.get('balance'))
        return jsonify('OK'), 200
    except Exception as e:
        return jsonify({"message": f"Failed to create a new user {str(e)}"}), 500
    