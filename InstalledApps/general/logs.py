import logging

def handle_log_exception(self):
    print(f' Inside logger of type: {type(self.exception).__name__} message: {self.exception}')
    logger = logging.getLogger(__name__)
    try:
        if isinstance(self.exception, ValueError):
            print(f'it is a ValueError in logs {self.exception}')
            logger.error(f"Excepción ValueError: {self.exception}")

        elif isinstance(exception, YourCustomException):
            logger.error(f"Excepción personalizada: {self.exception}")

        else:
            print(f' Not managed exception in logs {self.exception}')
            logger.error(f"Excepción no manejada: {self.exception}", exc_info=True)
    # __DEVELOPMENT__
    except Exception as e:
        print(f'se abre este log de exception {e}')
        logger.error(f"LOG fallido: {self.exception}")
    finally:
        print('se abre este log')
        with open('error.log', 'a') as f:
            f.write(f"Writing excepción: {self.exception}\n")

    # emails if exist server
    # send_mail(
    #     'Se produjo una excepción en la aplicación',
    #     f"Se produjo una excepción: {self.exception}",
    #     'noreply@example.com',
    #     ['admin@example.com'],
    #  )

    response = HttpResponse("ERROR in logs. Try after", status=500)
    return response

