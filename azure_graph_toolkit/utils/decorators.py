import requests
from functools import wraps
import logging

logging.basicConfig(level=logging.ERROR)

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
            #logging.error(http_err)
            raise Exception(f"""\nStatus: {http_err.response.status_code}    
Error : {http_err.response.json().get('error')}
Error description: "{http_err.response.json().get('error_description')}
            """)
        
        """
            return {
                'status_code': http_err.response.status_code,
                'error': http_err.response.json() if http_err.response.text else 'HTTP error'
            }

        except requests.exceptions.ConnectionError as conn_err:
            raise  conn_err
            return {
            'status_code': conn_err.response.status_code,
            'error':conn_err.response.text
            }
        
        except requests.exceptions.Timeout as timeout_err:
            raise timeout_err
            return {
            'status_code': timeout_err.response.status_code,
            'error': timeout_err.response.text
            }
        
        except requests.exceptions.TooManyRedirects as redirects_err:
            raise redirects_err
            return {
            'status_code': redirects_err.response.status_code,
            'error': redirects_err.response.text
            }
        
        except requests.exceptions.URLRequired as url_err:
            raise url_err
            return {
            'status_code': url_err.response.status_code,
            'error': url_err.response.text
            }
        
        except requests.exceptions.ChunkedEncodingError as chunked_err:
            raise chunked_err
            return {
            'status_code': chunked_err.response.status_code,
            'error': chunked_err.response.text
            }
"""
    return wrapper