
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from inr import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('inr.urls'))
]
