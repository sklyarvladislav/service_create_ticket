from typing import List, Callable, Type
from functools import wraps


class CustomException(Exception):
    pass


def handle_exceptions(exc: List[Type[Exception]], result_exc: Type[Exception] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except tuple(exc) as e:
                raise result_exc(f"An error occurred: {str(e)}") from e

        return wrapper

    return decorator
