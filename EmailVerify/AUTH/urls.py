from django.urls import path 
from .views import Signup_view,Login_view,Activate_account,Logout_view

urlpatterns = [
    path('signup/',Signup_view,name='signup_url'),
    path('login/',Login_view,name='lg_url'),
    path('logout/',Logout_view,name='logout_url')
    
]
