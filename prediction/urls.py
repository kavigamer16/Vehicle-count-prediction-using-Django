from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_view, name='prediction'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]