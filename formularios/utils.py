from formularios.models import Madre, Parto, RecienNacido
from django.db.models import Count, Q


def generar_estadisticas():

    data = {}


    data["total_rn_vivos"] = RecienNacido.objects.count()

    data["peso_menos_500"] = RecienNacido.objects.filter(peso__lt=500).count()
    data["peso_500_999"] = RecienNacido.objects.filter(peso__gte=500, peso__lte=999).count()
    data["peso_1000_1499"] = RecienNacido.objects.filter(peso__gte=1000, peso__lte=1499).count()
    data["peso_1500_1999"] = RecienNacido.objects.filter(peso__gte=1500, peso__lte=1999).count()
    data["peso_2000_2499"] = RecienNacido.objects.filter(peso__gte=2000, peso__lte=2499).count()
    data["peso_2500_2999"] = RecienNacido.objects.filter(peso__gte=2500, peso__lte=2999).count()
    data["peso_3000_3999"] = RecienNacido.objects.filter(peso__gte=3000, peso__lte=3999).count()
    data["peso_4000_mas"] = RecienNacido.objects.filter(peso__gte=4000).count()


    data["anomalia_congenita"] = RecienNacido.objects.filter(malformacion_congenita=True).count()




    data["profilaxis_ocular"] = RecienNacido.objects.filter(profilaxis_ocular=True).count()
    data["profilaxis_hepatitis"] = RecienNacido.objects.filter(vacuna_hepatitis_b=True).count()


    data["parto_vaginal"] = Parto.objects.filter(tipo_parto__icontains="vaginal").count()
    data["parto_instrumental"] = Parto.objects.filter(tipo_parto__icontains="instrumental").count()
    data["cesarea_urgencia"] = Parto.objects.filter(tipo_parto__icontains="urgencia").count()
    data["cesarea_electiva"] = Parto.objects.filter(tipo_parto__icontains="electiva").count()


    data["apgar_1_bajo"] = RecienNacido.objects.filter(apgar_1__lte=3).count()
    data["apgar_5_bajo"] = RecienNacido.objects.filter(apgar_5__lte=5).count()


    data["reanimacion_basica"] = RecienNacido.objects.filter(reanimacion_basica=True).count()
    data["reanimacion_avanzada"] = RecienNacido.objects.filter(reanimacion_avanzada=True).count()


    data["profilaxis_gonorrea"] = RecienNacido.objects.filter(profilaxis_ocular=True).count()


    data["hepb_madres_vih"] = RecienNacido.objects.filter(
        parto__madre__vih_positivo=True
    ).count()

    data["hepb_madres_vih_profilaxis_completa"] = RecienNacido.objects.filter(
        parto__madre__vih_positivo=True,
        profilaxis_completa=True
    ).count()



    total_partos = Parto.objects.count()
    data["total_partos"] = total_partos

    data["rem24_vaginal"] = data["parto_vaginal"]
    data["rem24_instrumental"] = data["parto_instrumental"]
    data["rem24_cesarea_electiva"] = data["cesarea_electiva"]
    data["rem24_cesarea_urgencia"] = data["cesarea_urgencia"]


    data["lactancia_temprana"] = RecienNacido.objects.filter(
        peso__gte=2500,
        apego_inmediato=True
    ).count()


    data["h2_numerador"] = Parto.objects.filter(acompanante_parto=True).count()
    data["h2_denominador"] = Parto.objects.count()

    data["h2_porcentaje"] = (
        (data["h2_numerador"] / data["h2_denominador"] * 100)
        if data["h2_denominador"] > 0 else 0
    )

 
    data["h3_numerador"] = RecienNacido.objects.filter(
        peso__gte=2500,
        apego_inmediato=True
    ).count()

    data["h3_denominador"] = RecienNacido.objects.filter(peso__gte=2500).count()

    data["h3_porcentaje"] = (
        (data["h3_numerador"] / data["h3_denominador"] * 100)
        if data["h3_denominador"] > 0 else 0
    )



    data["edad_total"] = Madre.objects.count()

    data["edad_menores_15"] = Madre.objects.filter(edad__lt=15).count()
    data["edad_15_24"] = Madre.objects.filter(edad__gte=15, edad__lte=24).count()
    data["edad_25_mas"] = Madre.objects.filter(edad__gte=25).count()


    if data["edad_total"] > 0:
        data["edad_menores_15_pct"] = round(data["edad_menores_15"] * 100 / data["edad_total"], 1)
        data["edad_15_24_pct"] = round(data["edad_15_24"] * 100 / data["edad_total"], 1)
        data["edad_25_mas_pct"] = round(data["edad_25_mas"] * 100 / data["edad_total"], 1)
    else:
        data["edad_menores_15_pct"] = 0
        data["edad_15_24_pct"] = 0
        data["edad_25_mas_pct"] = 0

    return data
