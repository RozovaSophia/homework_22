from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm


class UserRegisterView(CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")  # или 'users:profile'

    def form_valid(self, form):
        """Дополнительная логика после успешной регистрации"""
        response = super().form_valid(form)

        user = form.save()
        login(self.request, user)

        self.send_welcome_email(user)

        messages.success(
            self.request, _("Registration successful! Welcome to our site!")
        )

        return response

    def send_welcome_email(self, user):
        """Отправка приветственного письма"""
        subject = _("Welcome to our site!")
        message = _(
            f"Hello, {user.get_short_name()}!\n\n"
            f"Thank you for registering on our site.\n"
            f"Your email: {user.email}\n\n"
            f"Best regards,\nSite Team"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"✅ Приветственное письмо отправлено на {user.email}")
        except Exception as e:
            print(f"⚠️ Не удалось отправить письмо: {e}")


class UserLoginView(LoginView):
    """Вход пользователя"""

    form_class = UserLoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        """Дополнительная логика после успешного входа"""
        response = super().form_valid(form)
        messages.success(self.request, _("You have successfully logged in!"))
        return response

    def form_invalid(self, form):
        """Обработка неверных данных"""
        messages.error(self.request, _("Invalid email or password. Please try again."))
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Выход пользователя"""

    next_page = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You have successfully logged out."))
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Профиль пользователя"""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        """Получаем текущего пользователя"""
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def form_valid(self, form):
        messages.success(self.request, _("Profile updated successfully!"))
        return super().form_valid(form)


class UserDashboardView(LoginRequiredMixin, TemplateView):
    """Личный кабинет пользователя"""

    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
