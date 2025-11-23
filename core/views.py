from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from usuarios.models import Profile
from formularios.models import Madre


@login_required
def dashboard_view(request):
    profile = Profile.objects.filter(user=request.user).select_related("position").first()

    if not profile or not profile.position:
        return render(request, "sin_rol.html")

    if profile.position.code == "ADMIN":
        return render(request, "dashboard_admin.html")

    if profile.position.code == "SUPERVISOR":
        return render(request, "dashboard_supervisor.html")

    if profile.position.code == "MATRONA":
        madres = Madre.objects.filter(creado_por=request.user).order_by("-fecha_creacion")
        return render(request, "dashboard_matrona.html", {"madres": madres})
