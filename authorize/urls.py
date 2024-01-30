from django.urls import path
from .views import OrganizerSignup, AttenderSignup, Login, Logout

urlpatterns = [
    path('organizer/signup/', OrganizerSignup.as_view(), name="auth_organizer_signup"),
    path('attender/signup/', AttenderSignup.as_view(), name="auth_attender_signup"),
    path('login/', Login.as_view(), name="auth_login"),
    path('logout/', Logout.as_view(), name="auth_logout")
]
