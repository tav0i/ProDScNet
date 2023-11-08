from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import send_mail
from InstalledApps.general.logs import handle_log_exception
from requests.exceptions import HTTPError

class ExceptionHandler:
    def __init__(self, exception):
        self.exception = exception

    def handle(self):
        try:
            if type(self.exception).__name__ == 'ValidationError':
                print(f'HDL validation error: {self.exception}')
            elif isinstance(self.exception, ValueError):
                print(f'HDL ValueError en handle: {self.exception}')
            elif isinstance(self.exception, (
                TypeError,
                IndexError,
                NameError,
                KeyError,
                ImportError,
                IntegrityError,
                )):
                print(f'HDL ingresa a errores no controlados: {self.exception}')
            elif isinstance(self.exception, HTTPError):
                print(f'HDL ingresa a HTTP error: {self.exception}')
            elif isinstance(self.exception, Exception):
                print(f'HDL ingresa a error general: {self.exception}')
            
        except Exception as e:
            print(f'HDL have error {e}')
        finally:
            handle_log_exception(self)

    