from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')

class RegisterView(CreateView):
    redirect_authenticated_user = True
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')



