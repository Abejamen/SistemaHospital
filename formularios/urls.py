from django.urls import path
from core.views import (
    formulario_unico,
    supervisor_revisar,
    ver_formulario_verificado
)

app_name = "formularios"

urlpatterns = [
    path("<int:id>/", formulario_unico, name="formulario_unico"),

    path("verificado/<int:id>/", ver_formulario_verificado, name="formulario_verificado"),

    path("supervisor/revisar/<int:id>/", supervisor_revisar, name="supervisor_revisar"),


]
