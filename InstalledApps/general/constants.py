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


class Constants:
    FORM = 'form'
    FORM_TITLE = 'title'
    FORM_CARD_TITLE = 'cardtitle'
    FORM_CARD_SUBTITLE = 'cardsubtitle'
    MEDIA_URL = 'MEDIA_URL'
    FORM_ENCTYPE = 'formenctype'
    FORM_ACTION = 'formaction'
    ERROR_FORM = 'errorform'
    ERROR_SET = 'errorset'
    ERROR_CUSTOM = 'controller exception: '
    ERROR_MY_CUSTOM = 'SetMyErrorCustom'
    ERROR_EXCEPTION = 'Exception: '
    ERROR_NOT_MANAGED = 'not managed exception: '
    ERROR_ITEMS = 'DataBase Exception: '
    ERROR_HTTP_REST = 'Rest call error: '
    VALUE_ERROR = 'incorrected value: '
    INTEGRITY_ERROR = 'integrity error: '

    FORM_CONTENT_TYPE = 'Content-Type'
    
    #permisos
    ALLOW_VIEWER = 'Viewers'

    # APIS
    # ValidationError: Esta excepción se utiliza para indicar errores de validación en los datos de entrada, como campos faltantes o datos incorrectos.
    # PermissionDenied: Se utiliza para indicar que un usuario no tiene permisos para realizar una acción específica.
    # NotAuthenticated: Indica que un usuario no está autenticado y no tiene permiso para realizar una acción.
    # MethodNotAllowed: Se utiliza cuando se intenta acceder a una vista con un método HTTP no permitido (por ejemplo, hacer una solicitud POST a una vista que solo admite GET).
    # NotAcceptable: Indica que el servidor no puede generar una respuesta en un formato aceptable para el cliente, según las cabeceras "Accept" de la solicitud.
    # APIException: Esta es una excepción base para otras excepciones de la API personalizadas que puedes definir.
    # ParseError: Se utiliza cuando hay un error al analizar los datos de la solicitud.
    # AuthenticationFailed: Indica un fallo en la autenticación.
    # Throttled: Se produce cuando se supera el límite de solicitudes permitido por la tasa de uso.

    # rest
    AUTHORIZATION = 'Authorization'
    AUTORIZATION_TYPE = 'Bearer'
    APLICATION_JSON = 'application/json'
    ACCESS_TOKEN = 'access_token'
    TOKEN = 'token'
    REFRESH_TOKEN = 'refresh_token'
    ERROR_API = 'error'
    MESSAGE_API = 'message'

    #user
    USER_REGISTERED = 'User registered successfully'

    #tasks
    ERROR_NOT_FOUND = 'Not found'
    ERROR_PARSE = 'Not available option'
    ERROR_VALIDATION = 'Request Invalid'
    ERROR_PERMISION_DENIED = 'Not permited action'
    ERROR_INVALID_CREDENTIALS = 'Invalid credentials'
    ERROR_TASK_NOT_FOUND = 'Task not found'
