from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import SignupView

app_name = "users"

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'reset-password/', 
        PasswordResetView.as_view(
            success_url = reverse_lazy("users:password_reset_done")
        ), 
        name='reset-password'
    ),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset-confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            success_url = reverse_lazy("users:password_reset_complete")
        ), 
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/', 
        PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'
    ),
]
