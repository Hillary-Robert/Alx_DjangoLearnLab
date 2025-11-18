class ContentSecurityPolicyMiddleware:
    """
    Middleware to add a basic Content Security Policy (CSP) header.

    This reduces the risk of XSS by limiting where scripts, styles,
    and other resources can be loaded from.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Basic CSP: allow only same-origin resources
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:;"
        )
        return response
