from django.contrib.auth import logout
from django.shortcuts import redirect

class RestrictAdminUserInFrontendMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.path.startswith("/admin/")
            and request.user.is_authenticated
            and request.user.is_superuser
        ):
            logout(request)
            return redirect("/")  # Redirect to the login page
        response = self.get_response(request)
        return response