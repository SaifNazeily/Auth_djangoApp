from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('otp/', views.otp_view, name='otp'),
    path('hello/', views.hello_view, name='hello'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to homepage after logout
    
]
