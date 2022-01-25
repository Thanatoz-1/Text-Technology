from django.urls import path
from . import views 

app_name = "ver0"
urlpatterns = [
    path("", views.index, name="index"),
    path("keywords", views.keywords_page, name="keywords"),
    path("researchers", views.researchers_page, name="researchers"),
    path("affiliations", views.affiliations_page, name="affiliations")
]
# path("link name", function, key)