from django.urls import path
from .views import formulario_unico

urlpatterns = [
    path("<int:id>/", formulario_unico, name="formulario_unico"),
]
