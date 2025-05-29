from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import MyLoginView, RegisterView, MyLogoutView

app_name = 'users'

urlpatterns = [
    path('login', MyLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', MyLogoutView.as_view(), name='logout'),
]
