from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from core.views import (
    dashboard_view,
    admin_panel,
    dashboard_matrona,
    supervisor_dashboard_listado,
    supervisor_revisar,
    ver_formulario_verificado,
    supervisor_dashboard
)

urlpatterns = [

    path('', lambda request: redirect('/accounts/login/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('dashboard/admin/', admin_panel, name='admin_panel'),
    path('dashboard/matrona/', dashboard_matrona, name='dashboard_matrona'),
    path('dashboard/supervisor/verificacion/', supervisor_dashboard_listado, name='supervisor_dashboard_listado'),
    path('supervisor/revisar/<int:id>/', supervisor_revisar, name='supervisor_revisar'),
    path('dashboard/supervisor/listado/', supervisor_dashboard_listado, name="supervisor_listado"),
    path('dashboard/supervisor/', supervisor_dashboard, name='supervisor_dashboard'),
    path('dashboard/supervisor/listado/', supervisor_dashboard_listado, name='supervisor_listado'),
    path('formulario/', include('formularios.urls')),
    path('dashboard/admin/usuarios/', include('usuarios.urls')),
]
