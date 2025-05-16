from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from app.models.exceptions.QueryException import QueryException
from typing import List
from app.extensions import db
from app.models.user import User

def create_user(username:str, password:str, balance:float)-> None:
    try:
        balance = float(balance)
        if not isinstance(balance, float):
            raise ValueError(f'The balance must be a decimal, found {balance}')
        if username is None or password is None:
            raise ValueError('The username and password are both required fields')
        user= User(username=username, password=password, balance=balance)
        # with get_session() as session:
        #     session.add(user)
        #     session.commit()
        db.session.add(user)
        db.session.commit()
    except ValueError as e:
        raise QueryException('Invalid input provided for creating a new user', e)
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of failure
        raise QueryException('Failed to create a new user', e)

def password_matches(username:str, password:str)->bool:
    try:
        # session = db.session
        # users = session.query(User).filter(User.username == username).one()
        user = User.query.filter_by(username=username).one()
        if password == user.password:
            return user
    except NoResultFound as e:
        raise QueryException(f'No user found with username: {username}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'Unexpected state - multiple users found with the same username: {username}', e)
    except Exception as e:
        raise QueryException('An unexpected error occurred while checking username and password', e)
    
        
def get_all() -> List[User]:
    try: 
       return User.query.all()
    except Exception as e:
        raise QueryException('Failed to get all users', e)
     

def get_active() -> List[User]:
    try:
        return User.query.filter_by(is_active=True).all()
    except Exception as e:
        raise QueryException('Failed to get active users', e)

def get_balance(userId: int) -> float:
    try:
        if not isinstance(userId, int): #isinstance helps with type checking
            raise ValueError('userId must be an integer')
        user = User.query.filter_by(id=userId).one()
        return user.balance
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {userId}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exist with ID {userId}')
    except Exception as e:
        raise QueryException(f'Failed to get user balance for user with ID {userId}', e)

    

def delete_user(userId: int) -> None:
    try:
        user = User.query.filter_by(id=userId).one()
        db.session.delete(user)
        db.session.commit()
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {userId}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exists with ID {userId}', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to delete user with ID {userId}', e)

def update_balance(userId: int, updated_balance: float) -> None:
    try:
        user = User.query.filter_by(id=userId).one()
        user.balance = updated_balance
        db.session.commit()
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {userId}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exists with ID {userId}', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to update balance for user with ID {userId}', e)