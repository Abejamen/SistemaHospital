from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from usuarios.models import Usuario
from formularios.models import Madre, Parto, RecienNacido, VacunaBCG
from django.utils import timezone


@login_required
def dashboard_view(request):
    if request.user.role == "ADMIN":
        return redirect("admin_panel")
    if request.user.role == "SUPERVISOR":
        return redirect("supervisor_dashboard")
    return redirect("dashboard_matrona")


@login_required
def dashboard_matrona(request):
    q = request.GET.get("q", "")

    en_proceso = Madre.objects.filter(
        creado_por=request.user
    ).exclude(estado="APROBADO").order_by("-fecha_creacion")

    verificados = Madre.objects.filter(
        creado_por=request.user,
        estado="APROBADO"
    ).order_by("-fecha_validacion")

    if q:
        en_proceso = en_proceso.filter(
            Q(nombre_completo__icontains=q) |
            Q(rut__icontains=q)
        )
        verificados = verificados.filter(
            Q(nombre_completo__icontains=q) |
            Q(rut__icontains=q)
        )

    return render(request, "dashboard_matrona.html", {
        "en_proceso": en_proceso,
        "verificados": verificados,
        "q": q
    })


@login_required
def admin_panel(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard_view")

    usuarios = Usuario.objects.all().order_by("-id")

    return render(request, "dashboard_admin.html", {
        "usuarios": usuarios
    })


@login_required
def supervisor_dashboard(request):
    if request.user.role != "SUPERVISOR":
        return redirect("dashboard_view")

    return render(request, "dashboard_supervisor.html")


@login_required
def supervisor_dashboard_listado(request):
    if request.user.role != "SUPERVISOR":
        return redirect("dashboard_view")

    pendientes = Madre.objects.filter(estado="ENVIADO").order_by("-fecha_envio")
    aprobados = Madre.objects.filter(estado="APROBADO").order_by("-fecha_validacion")
    rechazados = Madre.objects.filter(estado="RECHAZADO").order_by("-fecha_validacion")

    return render(request, "dashboard_supervisor_listado.html", {
        "pendientes": pendientes,
        "aprobados": aprobados,
        "rechazados": rechazados,
    })


@login_required
def supervisor_revisar(request, id):
    if request.user.role != "SUPERVISOR":
        return redirect("dashboard_view")

    madre = get_object_or_404(Madre, pk=id)
    parto = Parto.objects.filter(madre=madre).first()
    rn = RecienNacido.objects.filter(parto=parto).first() if parto else None
    bcg = VacunaBCG.objects.filter(rn=rn).first() if rn else None 

    if request.method == "POST":
        accion = request.POST.get("accion")

        if accion == "aprobar":
            madre.estado = "APROBADO"
        else:
            madre.estado = "RECHAZADO"

        madre.validado_por = request.user
        madre.fecha_validacion = timezone.now()
        madre.save()

        return redirect("supervisor_dashboard_listado")

    return render(request, "supervisor_revisar.html", {
        "madre": madre,
        "parto": parto,
        "rn": rn,
        "bcg": bcg,  
    })


@login_required
def ver_formulario_verificado(request, id):
    madre = get_object_or_404(Madre, pk=id)

    if madre.creado_por != request.user:
        return redirect("dashboard_matrona")

    if madre.estado != "APROBADO":
        return redirect("dashboard_matrona")

    parto = Parto.objects.filter(madre=madre).first()
    rn = RecienNacido.objects.filter(parto=parto).first() if parto else None
    bcg = VacunaBCG.objects.filter(rn=rn).first() if rn else None

    return render(request, "formulario_verificado.html", {
        "madre": madre,
        "parto": parto,
        "rn": rn,
        "bcg": bcg,
    })


@login_required
def formulario_unico(request, id):
    madre = None
    parto = None
    rn = None
    bcg = None

    if id != 0:
        madre = get_object_or_404(Madre, pk=id)
        parto = Parto.objects.filter(madre=madre).first()
        rn = RecienNacido.objects.filter(parto=parto).first() if parto else None
        if rn:
            bcg = VacunaBCG.objects.filter(rn=rn).first()

        if madre.estado == "APROBADO" and request.user.role == "MATRONA":
            return render(request, "sin_rol.html", {
                "mensaje": "Este formulario ya fue aprobado y no puede ser editado."
            })

    from formularios.forms import MadreForm, PartoForm, RecienNacidoForm, VacunaBCGForm

    if request.method == "POST":
        incluir_parto = request.POST.get("incluir_parto") == "on"
        incluir_rn = request.POST.get("incluir_rn") == "on"
        incluir_bcg = request.POST.get("incluir_bcg") == "on"

        madre_form = MadreForm(request.POST, instance=madre)
        parto_form = PartoForm(request.POST, instance=parto if incluir_parto else None)
        rn_form = RecienNacidoForm(request.POST, instance=rn if incluir_rn else None)
        bcg_form = VacunaBCGForm(request.POST, instance=bcg if incluir_bcg else None)

        forms_ok = madre_form.is_valid()
        if incluir_parto:
            forms_ok = forms_ok and parto_form.is_valid()
        if incluir_rn:
            forms_ok = forms_ok and rn_form.is_valid()
        if incluir_bcg:
            forms_ok = forms_ok and bcg_form.is_valid()

        if not forms_ok:
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

        accion = request.POST.get("accion")

        if accion == "enviar_supervisor":
            madre_obj.estado = "ENVIADO"
            madre_obj.fecha_envio = timezone.now()
        else:
            madre_obj.estado = "BORRADOR"

        madre_obj.validado_por = None
        madre_obj.fecha_validacion = None
        madre_obj.save()

        parto_obj = None
        if incluir_parto:
            parto_obj = parto_form.save(commit=False)
            parto_obj.madre = madre_obj
            parto_obj.save()
        else:
            parto_obj = parto

        rn_obj = None
        if incluir_rn:
            rn_obj = rn_form.save(commit=False)
            if parto_obj:
                rn_obj.parto = parto_obj
            rn_obj.save()
        else:
            rn_obj = rn

        if incluir_bcg and rn_obj:
            bcg_obj = bcg_form.save(commit=False)
            bcg_obj.rn = rn_obj
            bcg_obj.save()

        return redirect("dashboard_matrona")

    madre_form = MadreForm(instance=madre)
    parto_form = PartoForm(instance=parto) if parto else PartoForm()
    rn_form = RecienNacidoForm(instance=rn) if rn else RecienNacidoForm()
    from formularios.forms import VacunaBCGForm
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
