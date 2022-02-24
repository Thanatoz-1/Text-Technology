from django.urls import path
from . import views

app_name = "ver0"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/researchers", views.search_researcher, name="researcher_search"),
    path("search/keywords", views.search_keyword, name="researcher_search"),
    path("search/affiliations", views.search_affiliations, name="researcher_search"),
    path("keywords", views.keywords_page, name="keywords"),
    path("researchers", views.researchers_page, name="researchers"),
    path("affiliations", views.affiliations_page, name="affiliations"),
    path("downloads", views.download_file, name="downloads"),
]
# path("link name", function, key)
