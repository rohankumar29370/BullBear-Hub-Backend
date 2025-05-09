

class QueryException(Exception):
    def __init__(self, message,e):
        super().__init__(f'[QUERY EXCEPTION] {message}. Details: {str(e)}')