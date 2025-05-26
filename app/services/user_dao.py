from sqlalchemy.exc import MultipleResultsFound, NoResultFound, IntegrityError
from app.models.exceptions.QueryException import QueryException
from typing import List
from app.extensions import db
from app.models.user import User
from app.config import Config

def get_user_by_username(username: str) -> User:
    try:
        return User.query.filter_by(username=username).one()
    except NoResultFound:
        return None
    except MultipleResultsFound as e:
        raise QueryException(f'Multiple users found with username: {username}', e)

def create_user(username: str, password: str, balance: float) -> User:
    try:
        if get_user_by_username(username):
            raise ValueError("Username already exists")
        
        user = User(username=username, password=password, balance=balance)
        db.session.add(user)
        db.session.commit()
        return user
    except IntegrityError as e:
        db.session.rollback()
        raise QueryException('Username already exists', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException('Failed to create user', e)

def update_balance(user_id: int, new_balance: float) -> User:
    try:
        user = User.query.filter_by(id=user_id).one()
        user.balance = new_balance
        db.session.commit()
        return user
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {user_id}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exists with ID {user_id}', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to update balance for user with ID {user_id}', e)

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

def get_balance(user_id: int) -> float:
    try:
        if not isinstance(user_id, int):
            raise ValueError('userId must be an integer')
        user = User.query.filter_by(id=user_id).one()
        return user.balance
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {user_id}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exists with ID {user_id}')
    except Exception as e:
        raise QueryException(f'Failed to get user balance for user with ID {user_id}', e)

def delete_user(user_id: int) -> None:
    try:
        user = User.query.filter_by(id=user_id).one()
        db.session.delete(user)
        db.session.commit()
    except NoResultFound as e:
        raise QueryException(f'No user exists with ID {user_id}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'More than one user exists with ID {user_id}', e)
    except Exception as e:
        db.session.rollback()
        raise QueryException(f'Failed to delete user with ID {user_id}', e)

def password_matches(username: str, password: str) -> User:
    try:
        user = User.query.filter_by(username=username).one()
        if password == user.password:
            return user
        raise QueryException('Invalid password', None)
    except NoResultFound as e:
        raise QueryException(f'No user found with username: {username}', e)
    except MultipleResultsFound as e:
        raise QueryException(f'Unexpected state - multiple users found with the same username: {username}', e)
    except Exception as e:
        raise QueryException('An unexpected error occurred while checking username and password', e)