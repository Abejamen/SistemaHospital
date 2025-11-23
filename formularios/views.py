from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Madre, Parto, RecienNacido
from .forms import MadreForm, PartoForm, RecienNacidoForm


@login_required
def formulario_unico(request, id):
    madre = None
    parto = None
    rn = None

    if id != 0:
        madre = get_object_or_404(Madre, pk=id)
        parto = Parto.objects.filter(madre=madre).first()
        if parto:
            rn = RecienNacido.objects.filter(parto=parto).first()

    if request.method == "POST":
        madre_form = MadreForm(request.POST, instance=madre)

        incluir_parto = request.POST.get("incluir_parto") == "on"
        incluir_rn = request.POST.get("incluir_rn") == "on"

        if incluir_parto or parto:
            parto_form = PartoForm(request.POST, instance=parto)
        else:
            parto_form = PartoForm(request.POST)

        if incluir_rn or rn:
            rn_form = RecienNacidoForm(request.POST, instance=rn)
        else:
            rn_form = RecienNacidoForm(request.POST)

        error = None
        if incluir_rn and not (incluir_parto or parto):
            error = "Para registrar un RN debe registrar primero el parto."

        madre_valida = madre_form.is_valid()
        parto_valido = not incluir_parto or parto_form.is_valid()
        rn_valido = not incluir_rn or rn_form.is_valid()

        if madre_valida and parto_valido and rn_valido and not error:
            madre_obj = madre_form.save(commit=False)
            if madre_obj.creado_por_id is None:
                madre_obj.creado_por = request.user
            madre_obj.save()

            parto_obj = parto
            if incluir_parto:
                parto_obj = parto_form.save(commit=False)
                parto_obj.madre = madre_obj
                parto_obj.save()

            if incluir_rn and parto_obj:
                rn_obj = rn_form.save(commit=False)
                rn_obj.parto = parto_obj
                rn_obj.save()

            return redirect("/dashboard/")


    else:
        madre_form = MadreForm(instance=madre)
        parto_form = PartoForm(instance=parto) if parto else PartoForm()
        rn_form = RecienNacidoForm(instance=rn) if rn else RecienNacidoForm()
        error = None
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
        "error": error,
    })
