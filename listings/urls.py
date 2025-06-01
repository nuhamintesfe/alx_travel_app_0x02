from django.urls import path
from . import views

urlpatterns = [
    # example:
    path('', views.home, name='home'),  # or whatever views you have
]
