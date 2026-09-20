from django.urls import path
from .views import Register, Login, Logout, CurrentUser

urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', Login, name= "login"),
    path('logout/', Logout, name= "logout"),
    path('current-user/', CurrentUser, name="CurrentUser")
    
]