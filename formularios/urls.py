from django.urls import path
from core.views import (
    formulario_unico,
    supervisor_revisar,
    ver_formulario_verificado,
    supervisor_dashboard_listado,
    dashboard_historial_formularios, 
)

app_name = "formularios"

urlpatterns = [
    path("<int:id>/", formulario_unico, name="formulario_unico"),

    path("verificado/<int:id>/", ver_formulario_verificado, name="formulario_verificado"),

    path("supervisor/revisar/<int:id>/", supervisor_revisar, name="supervisor_revisar"),

    path("supervisor/listado/", supervisor_dashboard_listado, name="supervisor_dashboard_listado"),

    path("supervisor/historial/", dashboard_historial_formularios, name="dashboard_historial_formularios"),
]
