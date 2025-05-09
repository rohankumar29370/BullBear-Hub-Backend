from flask import Blueprint,jsonify, request
from app.services.db.investment_dao import get_investments_by_portfolio, sell

investment_bp = Blueprint('investment', __name__)

@investment_bp.route('/get-all/<int:portfolioId>')
def get_all_investments_by_portId(portfolioId):
    try:
        investments = get_investments_by_portfolio(portfolioId)
        investments_dict = [investment.to_dict() for investment in investments]
        return jsonify(investments_dict), 200
    except Exception as e:
        return jsonify({"message": f"Failed to get investments of portfolio with ID {portfolioId}"})
    
@investment_bp.route('/sell', methods = ['POST'])
def sell_investment():
    try:
        sell_json = request.get_json()
        sell(sell_json.get('investmentId'),sell_json.get('qty'), sell_json.get('price'))
        return '', 200
    except Exception as e:
        return jsonify({"message": f"Failed to sell investment {str(e)}"}), 500