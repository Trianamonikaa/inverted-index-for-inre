from django.urls import path
from inr import views
from . import views

app_name = 'inr'
urlpatterns = [
    path('', views.index),
    path('hasil/',views.hasil ),

]