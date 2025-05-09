from typing import List
from app.extensions import db
from app.models.exceptions.QueryException import QueryException
from app.models.portfolio import Portfolio
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

def create_new(name: str, strategy: str, userId: int) -> None:
    try:
        if not isinstance(name, str) or not isinstance(strategy, str) or not isinstance(userId, int):
            raise Exception('Expected input data types: name|str, strategy|str, userId|int')
        portfolio = Portfolio(name=name, strategy=strategy, userId=userId)
        db.session.add(portfolio)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise QueryException('Failed to create a new portfolio', e)

def get_portfolios_by_user(userId: int) -> List[Portfolio]:
    try:
        if not isinstance(userId, int):
            raise Exception(f'User ID must be an integer received: {userId}')
        portfolios = Portfolio.query.filter_by(userId=userId).all()
        return portfolios
    except Exception as e:
        raise QueryException(f'Failed to get portfolios of user with ID {userId}')

def get_portfolio_by_id(id: int) -> Portfolio:
    try:
        if not isinstance(id, int):
            raise Exception(f'User ID must be an integer received: {userId}')
        return Portfolio.query.filter_by(id=id).one()
    except NoResultFound:
        raise QueryException(f'No portfolios exist with ID {id}')
    except MultipleResultsFound:
        raise QueryException(f'Found multiple portfolios with the same ID')
    except Exception as e:
        raise QueryException(f'Failed to query portfolio with ID {id}: {str(e)}')