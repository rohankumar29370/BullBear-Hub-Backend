from flask import Blueprint, jsonify, request
from app.services.investment_dao import get_investments_by_portfolio, sell, purchase, get_investments
from app.models.portfolio import Portfolio
from app.models.investment import Investment
from app.models.exceptions.QueryException import QueryException
from app.extensions import db
import logging

investment_bp = Blueprint('investment', __name__)

@investment_bp.route('/get-all/<int:portfolioId>')
def get_all_investments_by_portId(portfolioId):
    try:
        # First check if portfolio exists
        portfolio = Portfolio.query.get(portfolioId)
        if not portfolio:
            return jsonify({"message": f"Portfolio with ID {portfolioId} not found"}), 404
            
        investments = get_investments_by_portfolio(portfolioId)
        investments_dict = [investment.to_dict() for investment in investments]
        return jsonify(investments_dict), 200
    except QueryException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Failed to get investments of portfolio with ID {portfolioId}. Details: {str(e)}"}), 500

@investment_bp.route('/purchase', methods=['POST'])
def purchase_investment():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['portfolioId', 'ticker', 'price', 'quantity']):
            return jsonify({"message": "Missing required fields"}), 400
            
        investment = purchase(
            portfolio_id=data['portfolioId'],
            ticker=data['ticker'],
            price=float(data['price']),
            quantity=int(data['quantity'])
        )
        return jsonify({
            "message": "Investment purchased successfully",
            "investment": investment.to_dict()
        }), 201
    except QueryException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Failed to purchase investment: {str(e)}"}), 500

@investment_bp.route('/sell', methods=['POST'])
def sell_investment():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['investmentId', 'qty', 'price']):
            return jsonify({"message": "Missing required fields"}), 400
            
        sell(
            investmentId=int(data['investmentId']),
            qty=int(data['qty']),
            sale_price=float(data['price'])
        )
        return jsonify({"message": "Investment sold successfully"}), 200
    except QueryException as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Failed to sell investment: {str(e)}"}), 500