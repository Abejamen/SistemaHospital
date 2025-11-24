from django.urls import path
from . import views
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

    path("import-export/", views.menu_import_export, name="menu_import_export"),

    # EXPORTACIONES GENERALES
    path("exportar/excel/todos/", views.exportar_todos_excel, name="exportar_todos_excel"),
    path("exportar/excel/verificados/", views.exportar_verificados_excel, name="exportar_verificados_excel"),

    path("exportar/pdf/todos/", views.exportar_todos_pdf, name="exportar_todos_pdf"),
    path("exportar/pdf/verificados/", views.exportar_verificados_pdf, name="exportar_verificados_pdf"),

    # 🚀 EXPORTACIONES INDIVIDUALES (AGREGAR AQUÍ)
    path("exportar/excel/<int:id>/", views.exportar_excel_individual, name="exportar_excel_individual"),
    path("exportar/pdf/<int:id>/", views.exportar_pdf_individual, name="exportar_pdf_individual"),
]
