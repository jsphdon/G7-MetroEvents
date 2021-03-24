from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.LoginPage.as_view(), name="login"),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('myaccount/', views.HomePage.as_view(), name="myaccount"),

    path('administrator/', views.AdminPage.as_view(), name="administrator"),

    path('addEvent/', views.AddEvent.as_view(), name="addEvent"),

    path('organizer/', views.OrganizerPage.as_view(), name="organizer"),
    # path('organizer/addEvent/', views.organizerPage, name="organizer"),
]
