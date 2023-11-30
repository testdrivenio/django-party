from django.contrib.auth.views import LoginView


class LoginPage(LoginView):
    template_name = "party/general/page_party_organizer_login.html"
