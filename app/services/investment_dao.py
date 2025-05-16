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
            raise QueryException(f'Portfolio ID must be an integer, received: {portfolioId}')
        
        investments = Investment.query.filter_by(portfolio_id=portfolioId).all()
        return investments
    except Exception as e:
        raise QueryException(f'Failed to get investments with portfolio ID {portfolioId}: {str(e)}', e)


def get_investments(investmentId: int) -> Investment:
    try:
        if not isinstance(investmentId, int):
            raise Exception(f'Investment ID must be a number, received: {investmentId}')
        return Investment.query.filter_by(id=investmentId).one()
    except NoResultFound as e:
        raise QueryException(f'Cannot find investment #{investmentId}. This investment may have been already sold completely.', e)
    except MultipleResultsFound as e:
        raise QueryException(f'System error: Multiple records found for investment #{investmentId}. Please contact support.', e)
    except Exception as e:
        raise QueryException(f'Failed to retrieve investment #{investmentId}. Please try again.', e)

def harvest_investment(investmentId: int) -> None:
    try:
        if not isinstance(investmentId, int):
            raise Exception(f'Investment ID must be a number, received: {investmentId}')
        investment = Investment.query.filter_by(id=investmentId).one()
        db.session.delete(investment)
        db.session.commit()
    except NoResultFound as e:
        raise QueryException(f'Cannot delete investment #{investmentId} as it no longer exists in your portfolio.', e)
    except MultipleResultsFound as e:
        raise QueryException(f'System error: Multiple records found for investment #{investmentId}. Please contact support.', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to remove investment #{investmentId} from your portfolio. Please try again.', e)

def update_qty(investmentId: int, qty: int) -> None:
    try:
        if not isinstance(investmentId, int) or not isinstance(qty, int):
            raise Exception(f'Investment ID and quantity must be numbers. Received: ID={investmentId}, quantity={qty}')
        investment = Investment.query.filter_by(id=investmentId).one()
        investment.quantity = qty
        db.session.commit()
    except NoResultFound as e:
        raise QueryException(f'Cannot update investment #{investmentId} as it no longer exists in your portfolio.', e)
    except MultipleResultsFound as e:
        raise QueryException(f'System error: Multiple records found for investment #{investmentId}. Please contact support.', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to update quantity for investment #{investmentId}. Please try again.', e)

def purchase(porftolio_id, ticker, price, quantity):
    try:
        userId: int = get_portfolio_by_id(porftolio_id).userId.value
        balance: float = get_balance(userId)
        investment_cost: float = price * quantity
        if balance < investment_cost:
            raise Exception('Insufficient funds to complete this purchase.')
        investment = Investment(portfolio_id=porftolio_id, ticker=ticker, price=price, quantity=quantity, date=date.today())
        db.session.add(investment)
        db.session.commit()
        update_balance(userId, balance - investment_cost)
    except Exception as e:
        db.session.rollback()
        raise QueryException('Unable to complete purchase. Please check your balance and try again.', e)

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
