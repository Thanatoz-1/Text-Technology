from django.urls import path
from . import views 

app_name = "ver0"
urlpatterns = [
    path("", views.index, name="index")
]