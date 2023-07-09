from django.views.generic import TemplateView, CreateView

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator

from .forms import UserRegisterForm
from .models import URLData


@method_decorator(login_required(login_url=reverse_lazy("core:login")), name="dispatch")
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["urls"] = URLData.objects.filter(user=self.request.user)
        return context


class RegisterView(CreateView, SuccessMessageMixin):
    model = User
    template_name = "register.html"
    form_class = UserRegisterForm
    success_message = "Your user was created successfully"
    success_url = reverse_lazy("core:login")


class LoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.info(self.request, f"You are now logged in as {form.cleaned_data['username']}")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class LogoutView(LogoutView):
    next_page = reverse_lazy("core:home")
    template_name = "logout.html"
