from flask import Blueprint, jsonify, request
from app.services.portfolio_dao import get_portfolios_by_user, create_new

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/get-all/<int:userId>')
def get_portfolios_for_user(userId):
    try:
        portfolios = get_portfolios_by_user(userId)
        ports_dict = [port.to_dict() for port in portfolios]
        return jsonify(ports_dict), 200
    except Exception as e:
        return jsonify({"message": f"Failed to get portfolios for user with ID: {userId}. Details: {str(e)}"})
    
@portfolio_bp.route('/create-new', methods = ['POST'])
def create_new_portfolio():
    try:
        port_json = request.get_json()
        create_new(port_json.get('name'), port_json.get('strategy'), port_json.get('userId'))
        return '', 201
    except Exception as e:
        return jsonify({"message": f"Failed to create a new portfolio: {str(e)}"})