from django.shortcuts import render, redirect

from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator

from .forms import UserRegisterForm, URLDataForm, URLUpdateForm
from .models import URLData

from matplotlib import pyplot as plt
from io import BytesIO
import base64
import random


@method_decorator(login_required(login_url=reverse_lazy("core:login")), name="dispatch")
class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search")
        urls = URLData.objects.filter(user=request.user)
        if search_term:
            urls = urls.filter(url__icontains=search_term)
        context = self.get_context_data(urls=urls)
        return self.render_to_response(context)


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


class URLCreateView(CreateView, LoginRequiredMixin):
    model = URLData
    template_name = "create_url.html"
    form_class = URLDataForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(URLCreateView, self).dispatch(*args, **kwargs)


class URLUpdateView(UpdateView, LoginRequiredMixin):
    model = URLData
    form_class = URLUpdateForm
    template_name = "update_url.html"
    success_url = reverse_lazy("core:home")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(URLUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        shortened_url = self.kwargs.get("shortened_url")
        return URLData.objects.get(shortened_url=shortened_url)


class URLDeleteView(DeleteView):
    model = URLData
    template_name = "delete_url.html"
    success_url = reverse_lazy("core:home")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(URLDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        shortened_url = self.kwargs.get("shortened_url")
        return URLData.objects.get(shortened_url=shortened_url)


# Redirect to Original URL
class RedirectURLView(View):
    def get(self, request, shortened_url):
        url_data = URLData.objects.filter(shortened_url=shortened_url).first()
        if url_data:
            url_data.increment_click_count()

            return redirect(url_data.url)
        return redirect("core:home")


class StatsPageView(TemplateView):
    template_name = "stats.html"

    def get(self, request):
        user = request.user
        url_data = URLData.objects.filter(user=user)
        click_counts = [data.click_count for data in url_data]
        shortened_urls = [data.shortened_url for data in url_data]

        colors = []
        for _ in range(len(url_data)):
            r = random.random()
            g = random.random()
            b = random.random()
            colors.append((r, g, b))

        plt.bar(shortened_urls, click_counts, color=colors)
        plt.xlabel("Shortened URL")
        plt.ylabel("Click")
        plt.title("URL Click Statistics")

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        graph_img = buf.getvalue()
        buf.close()

        graph_img_base64 = base64.b64encode(graph_img).decode("utf-8")

        context = {"graph_img": graph_img_base64}

        return render(request, self.template_name, context)
