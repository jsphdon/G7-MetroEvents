from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('myaccount/', views.homePage, name="myaccount"),
    
    path('metroadmin/', views.adminPage, name="metroadmin"),
]