from flask import Blueprint, jsonify, request
from app.services.portfolio_dao import get_portfolios_by_user, create_new, delete_portfolio, get_portfolio_by_id
from app.models.user import User

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/get-all/<int:userId>')
def get_portfolios_for_user(userId):
    try:
        # First check if user exists
        user = User.query.get(userId)
        if not user:
            return jsonify({"message": f"User with ID {userId} not found"}), 404
            
        portfolios = get_portfolios_by_user(userId)
        ports_dict = [port.to_dict() for port in portfolios]
        return jsonify(ports_dict), 200
    except Exception as e:
        return jsonify({"message": f"Failed to get portfolios for user with ID: {userId}. Details: {str(e)}"}), 500
    
@portfolio_bp.route('/create-new', methods = ['POST'])
def create_new_portfolio():
    try:
        port_json = request.get_json()
        create_new(port_json.get('name'), port_json.get('strategy'), port_json.get('userId'))
        return '', 201
    except Exception as e:
        return jsonify({"message": f"Failed to create a new portfolio: {str(e)}"})

@portfolio_bp.route('/delete/<int:portfolioId>', methods=['DELETE'])
def delete_portfolio_route(portfolioId):
    try:
        print(f"Attempting to delete portfolio with ID: {portfolioId}")
        delete_portfolio(portfolioId)
        print(f"Successfully deleted portfolio with ID: {portfolioId}")
        return jsonify({"message": "Portfolio deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting portfolio: {str(e)}")
        return jsonify({"message": f"Failed to delete portfolio: {str(e)}"}), 500