from django.urls import path

from . import views

urlpatterns = [
    path("auth/register/", views.register, name="register"),
    path("auth/login/", views.login, name="login"),
    path("auth/csrf/", views.csrf, name="csrf"),
    path("auth/me/", views.me, name="me"),
    path("auth/logout/", views.logout, name="logout"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/<str:expense_id>/", views.expense_detail, name="expense-detail"),
]
