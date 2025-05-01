from django.urls import path
from core.views import auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('login/', auth_views.login_user),
    path('logout/', auth_views.logout_user),
    path('me/', auth_views.current_user),
]
