from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('myaccount/', views.homePage, name="myaccount"),

    path('administrator/', views.adminPage, name="administrator"),
    path('administrator/addEvent/', views.addEvent, name="addEvent"),

    path('organizer/', views.organizerPage, name="organizer"),
    path('organizer/addEvent/', views.addEvent, name="addEvent"),
    # path('organizer/addEvent/', views.organizerPage, name="organizer"),
]
