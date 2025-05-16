from typing import List
from app.extensions import db
from app.models.exceptions.QueryException import QueryException
from app.models.portfolio import Portfolio
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

def create_new(name: str, strategy: str, userId: int) -> None:
    try:
        if not isinstance(name, str) or not isinstance(strategy, str) or not isinstance(userId, int):
            raise Exception('Invalid input: Portfolio name and strategy must be text, user ID must be a number')
        portfolio = Portfolio(name=name, strategy=strategy, userId=userId)
        db.session.add(portfolio)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise QueryException('Unable to create new portfolio. Please try again.', e)

def get_portfolios_by_user(userId: int) -> List[Portfolio]:
    try:
        if not isinstance(userId, int):
            raise QueryException(f'User ID must be a number, received: {userId}')
        
        portfolios = Portfolio.query.filter_by(userId=userId).all()
        return portfolios
    except Exception as e:
        raise QueryException(f'Failed to retrieve portfolios for user #{userId}. Please try again.', e)

def get_portfolio_by_id(id: int) -> Portfolio:
    try:
        if not isinstance(id, int):
            raise Exception(f'Portfolio ID must be a number, received: {id}')
        return Portfolio.query.filter_by(id=id).one()
    except NoResultFound as e:
        raise QueryException(f'Cannot find portfolio #{id}. This portfolio may have been deleted.', e)
    except MultipleResultsFound as e:
        raise QueryException(f'System error: Multiple records found for portfolio #{id}. Please contact support.', e)
    except Exception as e:
        raise QueryException(f'Failed to retrieve portfolio #{id}. Please try again.', e)