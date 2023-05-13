from django.urls import path

from frontend.views import index, how_it_works, team

urlpatterns = [
    path("", index, name="index"),
    path("team", team, name="team"),
    path("how-it-works", how_it_works, name="htw"),
]
