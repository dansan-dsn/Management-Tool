from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('verify/<str:token>/', views.verify_user, name='vefify_user'),
    path('new_token/', views.refresh_token, name='refresh_token'),
]
