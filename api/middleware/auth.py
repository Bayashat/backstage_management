from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print("AuthMiddleware.process_request")

        #   If there is no return value(or return None): continue to go backwards(to the server)
        #   If there is a return value(HttpResponse/render()/redirect), it will be interrupted and go back

        #   0. Exclude pages that do not require a login to access
        # request.path_info  # Get the URL current requesting
        if request.path_info in ['/login/', '/image/code/', ]:
            return  # same thing like return None

        #   1. Read the session info of the currently visiting user. If can read it, it means it have already logged in, and continue
        info_dict = request.session.get('info')
        if info_dict:
            return

        #   2. Not logged in, redirect to login page
        return redirect('api:login')

    def process_response(self, request, response):
        # print("AuthMiddleware.process_response")
        return response
