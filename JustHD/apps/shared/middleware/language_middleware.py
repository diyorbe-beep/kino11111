from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')[:2]
        if lang not in ['en', 'uz', 'ru']:
            lang = 'en'
        
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        request.lang = lang
        
        response = self.get_response(request)
        
        response['Content-Language'] = lang
        
        return response