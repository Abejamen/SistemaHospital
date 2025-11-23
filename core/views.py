from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from formularios.models import Madre

@login_required
def dashboard_view(request):
    user = request.user

    if user.role == "ADMIN":
        return render(request, "dashboard_admin.html")

    elif user.role == "SUPERVISOR":
        return render(request, "dashboard_supervisor.html")

    elif user.role == "MATRONA":
        madres = Madre.objects.all().order_by("-fecha_creacion")
        return render(request, "dashboard_matrona.html", {"madres": madres})
