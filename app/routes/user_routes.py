from flask import Blueprint, jsonify, request
from app.services.user_dao import (
    create_user, get_all, get_user_by_username,
    update_balance, get_balance, delete_user, password_matches
)
from app.models.exceptions.QueryException import QueryException
from app.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/get-all')
def get_all_users():
    try:
        users = get_all()
        users_dicts = [user.to_dict() for user in users]
        return jsonify(users_dicts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/create-user', methods=['POST'])
def create_new_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data or 'balance' not in data:
            return jsonify({'message': 'Missing required fields'}), 400
        
        username = data['username']
        password = data['password']
        balance = float(data['balance'])

        if balance < 0:
            return jsonify({'message': 'Initial balance cannot be negative'}), 400

        try:
            user = create_user(username, password, balance)
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'balance': user.balance
                }
            }), 201
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@user_bp.route('/authenticate-user/<username>/<password>', methods=['GET'])
def authenticate_user(username, password):
    try:
        user = password_matches(username, password)
        return jsonify({
            'message': 'Authentication successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'balance': user.balance
            }
        }), 200
    except QueryException as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@user_bp.route('/update-balance/<int:user_id>', methods=['PUT'])
def update_user_balance(user_id):
    try:
        data = request.get_json()
        new_balance = data.get('balance')
        if new_balance is None:
            return jsonify({"message": "Balance is required"}), 400
        user = update_balance(user_id, float(new_balance))
        return jsonify({
            "message": "Balance updated successfully",
            "new_balance": user.balance
        }), 200
    except QueryException as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@user_bp.route('/get-balance/<int:user_id>', methods=['GET'])
def get_user_balance(user_id):
    try:
        balance = get_balance(user_id)
        return jsonify({'balance': balance}), 200
    except QueryException as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
    