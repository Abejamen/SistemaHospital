from django.db import models
from django.contrib.auth.models import User


class Madre(models.Model):
    nombre_completo_madre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12)
    fecha_nac_madre = models.DateField(null=True, blank=True)
    edad_materna = models.IntegerField(null=True, blank=True)
    comuna = models.CharField(max_length=60, null=True, blank=True)
    cesfam = models.CharField(max_length=80, null=True, blank=True)
    madre_vih = models.CharField(max_length=20)
    vdrl_materno = models.CharField(max_length=30)
    hepatitis_b_materno = models.CharField(max_length=30)
    migrante = models.BooleanField(default=False)
    pueblo_originario = models.BooleanField(default=False)
    e_paridad = models.IntegerField(null=True, blank=True)
    g_gestaciones = models.IntegerField(null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo_madre



class Parto(models.Model):
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE)

    fecha_nac = models.DateField()
    hora = models.TimeField(null=True, blank=True)

    tipo_parto = models.CharField(max_length=40)
    gases_cordon = models.BooleanField(default=False)
    apego_canguro = models.BooleanField(default=False)
    apego_tunel = models.BooleanField(default=False)
    clampeo_tardio = models.BooleanField(default=False)
    ive_causal_2 = models.BooleanField(default=False)

    destino_rn = models.CharField(max_length=40) 
    alojamiento_conjunto_puerperio = models.BooleanField(default=False)
    lactancia_antes_60min = models.BooleanField(default=False)
    acompanante_en_pabellon = models.CharField(max_length=120, null=True, blank=True)

    observaciones_parto = models.TextField(null=True, blank=True)
    interno = models.BooleanField(default=False)

    resultado_examen_1 = models.CharField(max_length=40, null=True, blank=True)
    resultado_examen_2 = models.CharField(max_length=40, null=True, blank=True)
    tratamiento_parto = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Parto de {self.madre.nombre_completo_madre}"


class RecienNacido(models.Model):
    parto = models.ForeignKey(Parto, on_delete=models.CASCADE)

    apellido_paterno_rn = models.CharField(max_length=80)
    sexo = models.CharField(max_length=12)

    peso = models.IntegerField()
    talla = models.DecimalField(max_digits=4, decimal_places=1) 
    circunferencia_craneana = models.DecimalField(max_digits=4, decimal_places=1)  

    diagnostico = models.TextField(null=True, blank=True)
    malformacion_congenita = models.BooleanField(default=False)
    descripcion_malformacion = models.TextField(null=True, blank=True)

    apgar_1min = models.IntegerField(null=True, blank=True)
    apgar_5min = models.IntegerField(null=True, blank=True)

    reanimacion_basica = models.BooleanField(default=False)
    reanimacion_avanzada = models.BooleanField(default=False)

    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    vacuna_bcg = models.BooleanField(default=False)

    profesional_que_vacuna_vhb = models.CharField(max_length=120, null=True, blank=True)
    profilaxis_completa = models.BooleanField(default=False)

    semanas_gestacion = models.IntegerField(null=True, blank=True)
    dias_gestacion = models.IntegerField(null=True, blank=True)

    apego_inmediato = models.BooleanField(default=False)
    destino_final = models.CharField(max_length=40)

    notas_rn = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"RN del parto: {self.parto.id}"
