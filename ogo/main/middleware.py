class MobileMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def process_template_response(self, request, response):
        if 'Mobile' in request.META['HTTP_USER_AGENT']:
            response.context_data['mobile'] = True
        return response
