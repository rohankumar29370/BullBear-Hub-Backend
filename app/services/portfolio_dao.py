from typing import List
from app.extensions import db
from app.models.exceptions.QueryException import QueryException
from app.models.portfolio import Portfolio
from app.models.investment import Investment
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

def delete_portfolio(portfolio_id: int) -> None:
    """Delete a portfolio by ID."""
    print(f"Starting deletion process for portfolio #{portfolio_id}")
    try:
        # First check if portfolio exists
        portfolio = get_portfolio_by_id(portfolio_id)
        if not portfolio:
            print(f"Portfolio #{portfolio_id} not found")
            raise QueryException(f"Portfolio #{portfolio_id} not found", Exception("Portfolio not found"))
        
        # Check if portfolio has any investments
        investments = Investment.query.filter_by(portfolio_id=portfolio_id).all()
        if investments:
            print(f"Portfolio #{portfolio_id} has {len(investments)} investments")
            raise QueryException("Please sell all investments in this portfolio before deleting it.", Exception("Portfolio has investments"))
        
        print(f"Deleting portfolio #{portfolio_id}")
        db.session.delete(portfolio)
        db.session.commit()
        
        # Verify deletion
        try:
            db.session.refresh(portfolio)
            print(f"Warning: Portfolio #{portfolio_id} still exists after deletion")
        except:
            print(f"Successfully deleted portfolio #{portfolio_id}")
            return
        
    except QueryException as e:
        print(f"QueryException during portfolio deletion: {str(e)}")
        db.session.rollback()
        raise e
    except Exception as e:
        print(f"Unexpected error during portfolio deletion: {str(e)}")
        db.session.rollback()
        raise QueryException("Unable to delete portfolio. Please try again.", e)