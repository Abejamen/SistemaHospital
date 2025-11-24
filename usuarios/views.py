from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario


@login_required
def admin_usuarios_lista(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_view")

    usuarios = Usuario.objects.all().order_by("-id")

    return render(request, "admin_usuarios_lista.html", {
        "usuarios": usuarios
    })


@login_required
def admin_usuarios_crear(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_view")

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rol = request.POST.get("rol")

        if Usuario.objects.filter(email=email).exists():
            return render(request, "admin_usuarios_crear.html", {
                "error": "El correo ya está registrado."
            })

        Usuario.objects.create_user(
            username=email,
            email=email,
            first_name=nombre,
            last_name=apellido,
            role=rol,
            password=password
        )

        return redirect("admin_usuarios_lista")

    return render(request, "admin_usuarios_crear.html")


@login_required
def admin_usuarios_editar(request, id):
    if request.user.role != "ADMIN":
        return redirect("dashboard_view")

    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == "POST":
        usuario.first_name = request.POST.get("nombre")
        usuario.last_name = request.POST.get("apellido")
        usuario.email = request.POST.get("email")
        usuario.role = request.POST.get("rol")

        nueva_pass = request.POST.get("password")
        if nueva_pass:
            usuario.set_password(nueva_pass)

        usuario.save()
        return redirect("admin_usuarios_lista")

    return render(request, "admin_usuarios_editar.html", {
        "usuario": usuario
    })


@login_required
def admin_usuarios_eliminar(request, id):
    if request.user.role != "ADMIN":
        return redirect("dashboard_view")

    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == "POST":
        usuario.delete()
        return redirect("admin_usuarios_lista")

    return render(request, "admin_usuarios_confirmar_eliminar.html", {
        "usuario": usuario
    })
