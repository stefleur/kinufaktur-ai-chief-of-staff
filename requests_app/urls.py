from django.urls import path

from . import views

app_name = "requests_app"

urlpatterns = [
    path("", views.request_list, name="list"),
    path("requests/new/", views.request_create, name="create"),
    path("requests/<int:pk>/", views.request_detail, name="detail"),
    path("requests/<int:pk>/edit/", views.request_update, name="update"),
]
