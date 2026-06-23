from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm, LoginForm


class RegisterView(CreateView):
    """
    Handles user registration.
    """

    form_class = RegistrationForm
    template_name = "accounts/register.html"

    # Temporary until Module 3
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        messages.success(
            self.request,
            f"Welcome, {self.object.username}! Your account has been created.",
        )

        return response


class CustomLoginView(LoginView):
    """
    Custom LoginView using Bootstrap-styled AuthenticationForm.
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Welcome back, {self.request.user.username}!"
        )

        return response

    def get_success_url(self):
        """
        Temporary redirect until documents module exists.
        """
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    """
    Secure logout using Django's built-in LogoutView.
    """

    next_page = reverse_lazy("home")