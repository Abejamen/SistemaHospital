from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Madre, Parto, RecienNacido, VacunaBCG
from .forms import MadreForm, PartoForm, RecienNacidoForm, VacunaBCGForm
from django.shortcuts import render
from .models import Madre
from .utils_export_excel import exportar_formularios_excel
from .utils_export_pdf import exportar_formularios_pdf


@login_required
def formulario_unico(request, id):
    madre = None
    parto = None
    rn = None
    bcg = None

    if id != 0:
        madre = get_object_or_404(Madre, pk=id)

        if madre.creado_por != request.user and request.user.role == "MATRONA":
            messages.error(request, "No puedes editar formularios creados por otra persona.")
            return redirect("/dashboard/")

        if madre.estado in ["ENVIADO", "APROBADO"] and request.user.role == "MATRONA":
            messages.error(request, "Este formulario ya fue enviado al supervisor y no puede ser editado.")
            return redirect("/dashboard/")

        parto = Parto.objects.filter(madre=madre).first()
        rn = RecienNacido.objects.filter(parto=parto).first() if parto else None
        bcg = VacunaBCG.objects.filter(rn=rn).first() if rn else None

    if request.method == "POST":
        accion = request.POST.get("accion", "guardar_borrador")

        incluir_parto = request.POST.get("incluir_parto") == "on"
        incluir_rn = request.POST.get("incluir_rn") == "on"
        incluir_bcg = request.POST.get("incluir_bcg") == "on"

        madre_form = MadreForm(request.POST, instance=madre)

        parto_form = PartoForm(
            request.POST if incluir_parto else None,
            instance=parto if incluir_parto else None
        )

        rn_form = RecienNacidoForm(
            request.POST if incluir_rn else None,
            instance=rn if incluir_rn else None
        )

        bcg_form = VacunaBCGForm(
            request.POST if incluir_bcg else None,
            instance=bcg if incluir_bcg else None
        )

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
            })

        madre_obj = madre_form.save(commit=False)

        if madre_obj.creado_por_id is None:
            madre_obj.creado_por = request.user

        if accion == "enviar_supervisor":
            madre_obj.estado = "ENVIADO"
            madre_obj.fecha_envio = timezone.now()
        else:
            madre_obj.estado = "BORRADOR"

        madre_obj.save()

        parto_obj = parto
        if incluir_parto and parto_form.is_valid():
            parto_obj = parto_form.save(commit=False)
            parto_obj.madre = madre_obj
            parto_obj.save()

        rn_obj = rn
        if incluir_rn and parto_obj and rn_form.is_valid():
            rn_obj = rn_form.save(commit=False)
            rn_obj.parto = parto_obj
            rn_obj.save()

        if incluir_bcg and rn_obj and bcg_form.is_valid():
            bcg_obj = bcg_form.save(commit=False)
            bcg_obj.rn = rn_obj
            bcg_obj.save()

        if accion == "enviar_supervisor":
            messages.success(request, "Formulario enviado al supervisor correctamente.")
        else:
            messages.success(request, "Formulario guardado como borrador.")

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
    })


@login_required
def supervisor_pendientes(request):
    if request.user.role != "SUPERVISOR":
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("/dashboard/")

    formularios_enviados = Madre.objects.filter(estado="ENVIADO").order_by("-fecha_envio")

    return render(request, "supervisor_pendientes.html", {
        "formularios": formularios_enviados,
    })


@login_required
def supervisor_revisar(request, id):
    if request.user.role != "SUPERVISOR":
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("/dashboard/")

    madre = get_object_or_404(Madre, pk=id)
    parto = Parto.objects.filter(madre=madre).first()
    rn = RecienNacido.objects.filter(parto=parto).first() if parto else None
    bcg = VacunaBCG.objects.filter(rn=rn).first() if rn else None

    return render(request, "supervisor_revisar.html", {
        "madre": madre,
        "parto": parto,
        "rn": rn,
        "bcg": bcg,
    })


@login_required
def supervisor_aprobar(request, id):
    if request.user.role != "SUPERVISOR":
        messages.error(request, "No tienes permiso para realizar esta acción.")
        return redirect("/dashboard/")

    madre = get_object_or_404(Madre, pk=id)

    madre.estado = "APROBADO"
    madre.validado_por = request.user
    madre.fecha_validacion = timezone.now()
    madre.save()

    messages.success(request, "Formulario aprobado correctamente.")
    return redirect("/supervisor/pendientes/")


@login_required
def supervisor_rechazar(request, id):
    if request.user.role != "SUPERVISOR":
        messages.error(request, "No tienes permiso para realizar esta acción.")
        return redirect("/dashboard/")

    madre = get_object_or_404(Madre, pk=id)

    madre.estado = "RECHAZADO"
    madre.validado_por = request.user
    madre.fecha_validacion = timezone.now()
    madre.save()

    messages.error(request, "Formulario rechazado. La matrona podrá editarlo nuevamente.")
    return redirect("/supervisor/pendientes/")



@login_required
def menu_import_export(request):
    return render(request, "formularios_menu_import_export.html")

@login_required
def exportar_todos_excel(request):
    madres = Madre.objects.all()
    return exportar_formularios_excel(madres)


@login_required
def exportar_verificados_excel(request):
    madres = Madre.objects.filter(aprobado=True)
    return exportar_formularios_excel(madres)


@login_required
def exportar_todos_pdf(request):
    madres = Madre.objects.all()
    return exportar_formularios_pdf(madres)


@login_required
def exportar_verificados_pdf(request):
    madres = Madre.objects.filter(aprobado=True)
    return exportar_formularios_pdf(madres)


def exportar_excel_individual(request, id):
    return exportar_formularios_excel(Madre.objects.filter(id=id))


def exportar_pdf_individual(request, id):
    return exportar_formularios_pdf(Madre.objects.filter(id=id))
