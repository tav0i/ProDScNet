from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import send_mail
from InstalledApps.general.logs import handle_log_exception
'''
exception_handlers = {
    "ValueError": lambda e: print("Produce error ValueError:", e),
    "TypeError": lambda e: print("Produce TypeError:", e),
    "IndexError": lambda e: print("Produce IndexError:", e),
    "NameError": lambda e: print("Produce NameError:", e),
    "KeyError": lambda e: print("Produce KeyError:", e),
    "ImportError": lambda e: print("Produce ImportError:", e),
    "IntegrityError": lambda e: print("Produce IntegrityError:", e),
    "Exception": lambda e: print(f"Produce not handler error: {e}"),
}
'''


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
            elif isinstance(self.exception, Exception):
                print(f'HDL ingresa a error general: {self.exception}')
        except Exception as e:
            print(f'HDL have error {e}')
        finally:
            handle_log_exception(self)

    