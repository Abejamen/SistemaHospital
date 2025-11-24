from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from .models import Parto, RecienNacido, VacunaBCG


def exportar_formularios_pdf(madres_qs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="formularios_completos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    first = True
    for madre in madres_qs:
        if not first:
            story.append(PageBreak())
        first = False

        story.append(Paragraph("Formulario Clínico Completo", styles["Title"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Datos de la Madre", styles["Heading2"]))
        for label, value in [
            ("Nombre completo", madre.nombre_completo),
            ("RUT", madre.rut),
            ("Fecha nacimiento", madre.fecha_nacimiento),
            ("Edad", madre.edad),
            ("Comuna", madre.comuna),
            ("CESFAM", madre.cesfam),
            ("Migrante", madre.migrante),
            ("Pueblo originario", madre.pueblo_originario),
            ("VIH positivo", madre.vih_positivo),
            ("VDRL resultado", madre.vdrl_resultado),
            ("VDRL tratamiento", madre.vdrl_tratamiento),
            ("Hepatitis B resultado", madre.hepatitis_b_resultado),
            ("Profilaxis completa", madre.profilaxis_completa),
            ("Estado", madre.estado),
        ]:
            story.append(Paragraph(f"{label}: {value}", styles["Normal"]))

        parto = Parto.objects.filter(madre=madre).first()
        if parto:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Datos del Parto", styles["Heading2"]))
            for label, value in [
                ("Fecha parto", parto.fecha_parto),
                ("Hora parto", parto.hora_parto),
                ("Tipo parto", parto.tipo_parto),
                ("Edad gestacional (semanas)", parto.edad_gestacional_semanas),
                ("Edad gestacional (días)", parto.edad_gestacional_dias),
                ("Clasificación Robson", parto.clasificacion_robson),
            ]:
                story.append(Paragraph(f"{label}: {value}", styles["Normal"]))

            rn = RecienNacido.objects.filter(parto=parto).first()
            if rn:
                story.append(Spacer(1, 12))
                story.append(Paragraph("Recién Nacido", styles["Heading2"]))
                for label, value in [
                    ("Apellido paterno", rn.apellido_paterno),
                    ("Sexo", rn.sexo),
                    ("Peso", rn.peso),
                    ("Talla", rn.talla),
                    ("Circunferencia craneana", rn.circunferencia_craneana),
                    ("Diagnóstico", rn.diagnostico),
                    ("Malformación congénita", rn.malformacion_congenita),
                    ("APGAR 1", rn.apgar_1),
                    ("APGAR 5", rn.apgar_5),
                    ("Vacuna BCG", rn.vacuna_bcg),
                    ("Vacuna Hepatitis B", rn.vacuna_hepatitis_b),
                    ("Destino final", rn.destino_final),
                ]:
                    story.append(Paragraph(f"{label}: {value}", styles["Normal"]))

                bcg = VacunaBCG.objects.filter(rn=rn).first()
                if bcg:
                    story.append(Spacer(1, 12))
                    story.append(Paragraph("Vacuna BCG", styles["Heading2"]))
                    for label, value in [
                        ("Número registro", bcg.numero_registro),
                        ("Aplicada", bcg.aplicada),
                        ("Comuna", bcg.comuna),
                        ("Reacción adversa", bcg.reaccion_adversa),
                        ("Cama / ubicación", bcg.cama_ubicacion),
                    ]:
                        story.append(Paragraph(f"{label}: {value}", styles["Normal"]))

    doc.build(story)
    return response
