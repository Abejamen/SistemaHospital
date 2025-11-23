from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Madre, Parto, RecienNacido, VacunaBCG
from .forms import MadreForm, PartoForm, RecienNacidoForm, VacunaBCGForm


@login_required
def formulario_unico(request, id):
    madre = None
    parto = None
    rn = None
    bcg = None

    if id != 0:
        madre = get_object_or_404(Madre, pk=id)
        parto = Parto.objects.filter(madre=madre).first()
        if parto:
            rn = RecienNacido.objects.filter(parto=parto).first()
            if rn:
                bcg = VacunaBCG.objects.filter(rn=rn).first()

    if request.method == "POST":
        incluir_parto = request.POST.get("incluir_parto") == "on"
        incluir_rn = request.POST.get("incluir_rn") == "on"
        incluir_bcg = request.POST.get("incluir_bcg") == "on"

        madre_form = MadreForm(request.POST, instance=madre)
        parto_form = PartoForm(request.POST, instance=parto if incluir_parto else None)
        rn_form = RecienNacidoForm(request.POST, instance=rn if incluir_rn else None)
        bcg_form = VacunaBCGForm(request.POST, instance=bcg if incluir_bcg else None)

        if not madre_form.is_valid():
            return render(request, "formulario_unico.html", {
                "madre_form": madre_form,
                "parto_form": parto_form,
                "rn_form": rn_form,
                "bcg_form": bcg_form,
                "madre": madre,
                "parto": parto,
                "rn": rn,
                "bcg": bcg,
                "incluir_parto": incluir_parto,
                "incluir_rn": incluir_rn,
                "incluir_bcg": incluir_bcg,
                "error": None,
            })

        madre_obj = madre_form.save(commit=False)
        if madre_obj.creado_por_id is None:
            madre_obj.creado_por = request.user
        madre_obj.save()

        parto_obj = parto
        if incluir_parto:
            if parto_form.is_valid():
                parto_obj = parto_form.save(commit=False)
                parto_obj.madre = madre_obj
                parto_obj.save()

        rn_obj = rn
        if incluir_rn and parto_obj:
            if rn_form.is_valid():
                rn_obj = rn_form.save(commit=False)
                rn_obj.parto = parto_obj
                rn_obj.save()

        if incluir_bcg and rn_obj:
            if bcg_form.is_valid():
                bcg_obj = bcg_form.save(commit=False)
                bcg_obj.rn = rn_obj
                bcg_obj.save()

        return redirect("/dashboard/")

    else:
        madre_form = MadreForm(instance=madre)
        parto_form = PartoForm(instance=parto) if parto else PartoForm()
        rn_form = RecienNacidoForm(instance=rn) if rn else RecienNacidoForm()
        bcg_form = VacunaBCGForm(instance=bcg) if bcg else VacunaBCGForm()

        incluir_parto = bool(parto)
        incluir_rn = bool(rn)
        incluir_bcg = bool(bcg)

    return render(request, "formulario_unico.html", {
        "madre_form": madre_form,
        "parto_form": parto_form,
        "rn_form": rn_form,
        "bcg_form": bcg_form,
        "madre": madre,
        "parto": parto,
        "rn": rn,
        "bcg": bcg,
        "incluir_parto": incluir_parto,
        "incluir_rn": incluir_rn,
        "incluir_bcg": incluir_bcg,
        "error": None,
    })
