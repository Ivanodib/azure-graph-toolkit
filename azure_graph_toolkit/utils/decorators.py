import requests
from functools import wraps
import logging

logging.basicConfig(level=logging.ERROR)

class GraphHTTPError(Exception):
    pass


def handle_http_exceptions(func):
    """
    Decorator to handle HTTP exceptions in all functions.

    Args:
        function (func): The function to handle HTTP exceptions. 

    Returns:
        dict: A dictionary containings status code and error raised."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except requests.exceptions.HTTPError as http_err:

            response_json = http_err.response.json()
            message = response_json.get('error', {}).get('message')

            error_response = {
            "status_code": http_err.response.status_code,
            "message": message
            }
            
            return error_response
            #raise GraphHTTPError(error_response) from None

    return wrapper