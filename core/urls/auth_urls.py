from django.urls import path
from core.views import auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('login/', auth_views.login_user),
    path('logout/', auth_views.logout_user),
    path('me/', auth_views.current_user),
    path('users/', auth_views.list_users),
    path('user/<int:user_id>/', auth_views.get_user),
    path('user/update/', auth_views.update_user),
    path('user/delete/', auth_views.delete_user),
    path('user/change-password/', auth_views.change_password),
]


