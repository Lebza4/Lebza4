from django.urls import path
from leboapp import views

urlpatterns = [
    path('',views.home,name='home'),
]
