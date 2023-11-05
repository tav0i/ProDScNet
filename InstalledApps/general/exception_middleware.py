from InstalledApps.general.logs import handle_log_exception

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            print(f'Call to ExceptionLoggingMiddleware {request}')
            response = self.get_response(request)
        except Exception as e:
            print('Exception in ExceptionLoggingMiddleware {request}')
            # __DEVELOPMENT__: Could redirect to a personalized page
            handle_log_exception(request, e)  
            response = self.get_response(request) 
        return response

    