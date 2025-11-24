from django.urls import path
from .views import (
    admin_usuarios_lista,
    admin_usuarios_crear,
    admin_usuarios_editar,
    admin_usuarios_eliminar,
)

urlpatterns = [
    path('', admin_usuarios_lista, name='admin_usuarios_lista'),
    path('crear/', admin_usuarios_crear, name='admin_usuarios_crear'),
    path('editar/<int:id>/', admin_usuarios_editar, name='admin_usuarios_editar'),
    path('eliminar/<int:id>/', admin_usuarios_eliminar, name='admin_usuarios_eliminar'),
]
