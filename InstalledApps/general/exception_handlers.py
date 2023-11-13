from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import send_mail
from InstalledApps.general.logs import handle_log_exception
from InstalledApps.general.constants import Constants
from requests.exceptions import ConnectionError, Timeout, RequestException, HTTPError

class ExceptionHandler:
    def __init__(self, exception):
        self.exception = exception

    def handle(self):
        try:
            if type(self.exception).__name__ == 'ValidationError':
                print(f'HDL {Constants.ERROR_VALIDATION}: {self.exception}')
            elif isinstance(self.exception, ValueError):
                print(f'{Constants.VALUE_ERROR}: {self.exception}')
            elif isinstance(self.exception, (
                TypeError,
                IndexError,
                NameError,
                KeyError,
                ImportError,
                IntegrityError,
                )):
                print(f'HDL {Constants.ERROR_NOT_CONTROLLED}: {self.exception}')
            # REST
            elif isinstance(self, ConnectionError):
                print(f'HDL {Constants.ERROR_CONNECTION}: {self.exception}')
            elif isinstance(self, Timeout):
                print(f'HDL {Constants.ERROR_TIMEOUT}: {self.exception}')
            elif isinstance(self, HTTPError):
                print(f'HDL {Constants.ERROR_HTTP_REST}: {self.exception}')
            elif isinstance(self, RequestException):
                print(f'HDL {Constants.ERROR_REQUEST_EXCEPTION}: {self.exception}')
            
        except Exception as e:
            print(f'HDL {Constants.ERROR_EXCEPTION} {e}')
        finally:
            print('develop the handle_log_exception(self)')
            # __DEVELOPMENT__ test in task/5
            # handle_log_exception(self)

    