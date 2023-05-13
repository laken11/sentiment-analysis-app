from django.urls import path

from backend.views.history.views import analyse

urlpatterns = [
    path("analyse", analyse, name="analyse")
]
