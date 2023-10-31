from functools import wraps
from django.http import JsonResponse
from InstalledApps.general.constants import Constants

#__DEVELOPMENT__
def custom_authorization_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica la existencia del encabezado Authorization y el formato adecuado
        authorization_header = request.session.get(Constants.ACCESS_TOKEN)
        if authorization_header and authorization_header.startswith('{Constants.AUTORIZATION_TYPE} '):
            access_token = authorization_header.split(' ')[1]

            # Realiza la validación del token si es necesario
            # Por ejemplo, verifica la validez del token

            # Si la validación es exitosa, continúa con la vista
            return view_func(request, *args, **kwargs)
        else:
            # Si no se proporciona un encabezado de autorización válido
            return JsonResponse({'error': 'Acceso no autorizado'}, status=401)

    return _wrapped_view
