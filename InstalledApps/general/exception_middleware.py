from django.utils import timezone
from InstalledApps.general.logs import handle_log_exception

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        req = f'{request.method} - {request.path}'
        try:
            print(f'Request  LogMDLW {timezone.now().strftime("%y-%m-%d %H:%M:%S")} {req}')
            response = self.get_response(request)
            res = f'{response.status_code} - {response.reason_phrase}- {response.charset}'# - {response.content_type}' __DEVELEPMENT__ generate eror to manage handle_log_exception 
            print(f'Response LogMDLW {timezone.now().strftime("%y-%m-%d %H:%M:%S")} {req} -> {res}')
        except Exception as e:
            print(f'ERROR in LogMDLW {req} - {e}')
            # __DEVELOPMENT__: Could redirect to a personalized page
            # handle_log_exception(request, e)  
            response = self.get_response(request) 
        return response

    