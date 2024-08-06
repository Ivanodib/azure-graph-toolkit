import requests
from functools import wraps

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
            return {
            'status_code': http_err.response.status_code,
            'error':http_err.response.text
            }

        except requests.exceptions.ConnectionError as conn_err:
            return {
            'status_code': conn_err.response.status_code,
            'error':conn_err.response.text
            }
        
        except requests.exceptions.Timeout as timeout_err:
            return {
            'status_code': timeout_err.response.status_code,
            'error': timeout_err.response.text
            }
        
        except requests.exceptions.TooManyRedirects as redirects_err:
            return {
            'status_code': redirects_err.response.status_code,
            'error': redirects_err.response.text
            }
        
        except requests.exceptions.URLRequired as url_err:
            return {
            'status_code': url_err.response.status_code,
            'error': url_err.response.text
            }
        
        except requests.exceptions.ChunkedEncodingError as chunked_err:
            return {
            'status_code': chunked_err.response.status_code,
            'error': chunked_err.response.text
            }
        
        except requests.exceptions.RequestException as req_err:
            return {
            'status_code': req_err.response.status_code,
            'error': req_err.response.text
            }

    return wrapper