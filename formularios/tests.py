from django.urls import path
from .views import crear_formulario

urlpatterns = [
    path("crear/", crear_formulario, name="crear_formulario"),
]
