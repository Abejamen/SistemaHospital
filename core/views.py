from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from formularios.models import Madre, Parto, RecienNacido
from formularios.forms import MadreForm, PartoForm, RecienNacidoForm


@login_required
def dashboard_view(request):
    q = request.GET.get("q", "")

    madres = Madre.objects.all().order_by("-fecha_creacion")

    if q:
        madres = madres.filter(
            Q(nombre_completo__icontains=q) |
            Q(rut__icontains=q)
        )

    return render(request, "dashboard_matrona.html", {
        "madres": madres,
        "q": q
    })


@login_required
def formulario_unico(request, id):
    madre = None
    parto = None
    rn = None

    if id != 0:
        madre = get_object_or_404(Madre, pk=id)
        parto = Parto.objects.filter(madre=madre).first()
        rn = RecienNacido.objects.filter(parto=parto).first() if parto else None

    if request.method == "POST":

        incluir_parto = request.POST.get("incluir_parto") == "on"
        incluir_rn = request.POST.get("incluir_rn") == "on"

        madre_form = MadreForm(request.POST, instance=madre)
        parto_form = PartoForm(request.POST, instance=parto if incluir_parto else None)
        rn_form = RecienNacidoForm(request.POST, instance=rn if incluir_rn else None)

        if not madre_form.is_valid():
            return render(request, "formulario_unico.html", {
                "madre_form": madre_form,
                "parto_form": parto_form,
                "rn_form": rn_form,
                "madre": madre,
                "parto": parto,
                "rn": rn,
                "incluir_parto": incluir_parto,
                "incluir_rn": incluir_rn,
                "error": None,
            })

        madre_obj = madre_form.save(commit=False)
        if madre_obj.creado_por_id is None:
            madre_obj.creado_por = request.user
        madre_obj.save()

        parto_obj = None
        if incluir_parto and parto_form.is_valid():
            parto_obj = parto_form.save(commit=False)
            parto_obj.madre = madre_obj
            parto_obj.save()

        if incluir_rn and rn_form.is_valid():
            rn_obj = rn_form.save(commit=False)
            if parto_obj:
                rn_obj.parto = parto_obj
            rn_obj.save()

        return redirect("/dashboard/")

    madre_form = MadreForm(instance=madre)
    parto_form = PartoForm(instance=parto) if parto else PartoForm()
    rn_form = RecienNacidoForm(instance=rn) if rn else RecienNacidoForm()

    incluir_parto = bool(parto)
    incluir_rn = bool(rn)

    return render(request, "formulario_unico.html", {
        "madre_form": madre_form,
        "parto_form": parto_form,
        "rn_form": rn_form,
        "madre": madre,
        "parto": parto,
        "rn": rn,
        "incluir_parto": incluir_parto,
        "incluir_rn": incluir_rn,
        "error": None,
    })
