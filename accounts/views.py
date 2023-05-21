from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomLoginForm, CustomRegistrationForm

class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'
