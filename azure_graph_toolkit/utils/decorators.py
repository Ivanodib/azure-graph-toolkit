import requests
from functools import wraps
import logging
import json

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

            error_response = {
            "status": http_err.response.status_code,
            "error": http_err.response.json().get('error'),
            "error_description": http_err.response.json().get('error_description')
            }
            raise GraphHTTPError(error_response) from None
    return wrapper