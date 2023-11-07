from InstalledApps.general.logs import handle_log_exception

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            print(f'Request LoggingMiddleware {request}')
            response = self.get_response(request)
            print(f'Response LoggingMiddleware {response}')
        except Exception as e:
            print(f'ERROR in ExceptionLoggingMiddleware {request} - {e}')
            # __DEVELOPMENT__: Could redirect to a personalized page
            handle_log_exception(request, e)  
            response = self.get_response(request) 
        return response

    