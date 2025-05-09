from datetime import date
from typing import List
from app.models.exceptions.QueryException import QueryException
from app.models.investment import Investment
from app.services.portfolio_dao import get_portfolio_by_id
from app.services.user_dao import get_balance, update_balance
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from app.extensions import db

def get_investments_by_portfolio(portfolioId: int) -> List[Investment]:
    try:
        if not isinstance(portfolioId, int):
            raise Exception(f'Porftolio ID must be an int found {portfolioId}')
        return Investment.query.filter_by(portfolio_id=portfolioId).all()
    except Exception as e:
        raise QueryException(f'Failed to get investments with portfolio ID {portfolioId}')


def get_investments(investmentId: int) -> Investment:
    try:
        if not isinstance(investmentId, int):
            raise Exception(f'Investment ID must be an int found {investmentId}')
        return Investment.query.filter_by(id=investmentId).one()
    except NoResultFound:
        raise QueryException(f'No Investments exist with ID {investmentId}')
    except MultipleResultsFound:
        raise QueryException(f'Found multiple investments with the same ID {investmentId}')
    except Exception as e:
        raise QueryException(f'Failed to get investment with ID {investmentId}: {str(e)}')

def harvest_investment(investmentId: int) -> None:
    try:
        if not isinstance(investmentId, int):
            raise Exception(f'Investment ID must be an int found {investmentId}')
        investment = Investment.query.filter_by(id=investmentId).one()
        db.session.delete(investment)
        db.session.commit()
    except NoResultFound:
        raise QueryException(f'No Investments exist with ID {investmentId}')
    except MultipleResultsFound:
        raise QueryException(f'Found multiple investments with the same ID {investmentId}')
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to harvest investment with ID {investmentId}: {str(e)}')

def update_qty(investmentId: int, qty: int) -> None:
    try:
        if not isinstance(investmentId, int) or not isinstance(qty, int):
            raise Exception(f'Investment ID and Qty must be an int found investment ID={investmentId}, qty={qty}')
        investment = Investment.query.filter_by(id=investmentId).one()
        investment.quantity = qty
        db.session.commit()
    except NoResultFound:
        raise QueryException(f'No Investments exist with ID {investmentId}')
    except MultipleResultsFound:
        raise QueryException(f'Found multiple investments with the same ID {investmentId}')
    except Exception as e:
        db.session.rollbal()
        raise QueryException(f'Failed to update investment quantity [Investment Id: {investmentId}]: {str(e)}')

def purchase(porftolio_id, ticker, price, quantity):
    try:
        userId: int = get_portfolio_by_id(porftolio_id).userId.value
        balance: float = get_balance(userId)
        investment_cost: float = price * quantity
        if balance < investment_cost:
            raise Exception('No sufficient funds')
        investment = Investment(portfolio_id=porftolio_id, ticker=ticker, price=price, quantity=quantity, date=date.today())
        db.session.add(investment)
        db.session.commit()
        update_balance(userId, balance - investment_cost)
    except Exception as e:
        db.session.rollback()
        raise QueryException('Failed to place purchase order', e)

def sell(investmentId, qty, sale_price):
    investment: Investment = get_investments(investmentId)
    available_qty: int = investment.quantity
    if qty > available_qty:
        raise Exception(f'Quantity provided on sale order ({qty}) exceeds user available quantity ({available_qty})')
    if qty == available_qty:
        harvest_investment(investmentId)
    else:
        updated_qty = available_qty - qty
        update_qty(investmentId, updated_qty)
    proceeds: float = qty * sale_price
    portfolio = get_portfolio_by_id(investment.portfolio_id)
    userId: int = portfolio.userId
    old_balance = get_balance(userId)
    update_balance(userId, old_balance + proceeds)
