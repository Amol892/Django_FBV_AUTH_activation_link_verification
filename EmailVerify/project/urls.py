from django.urls import path 
from .views import *

urlpatterns = [
    path('project/',Project_view.as_view(),name='project_url'),
    path('home/',Home_view.as_view(),name='home_url')
]
