from django.db import models
from django.conf import settings


class Madre(models.Model):
    nombre_completo = models.CharField(max_length=150)
    rut = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    cesfam = models.CharField(max_length=100, null=True, blank=True)
    migrante = models.BooleanField(default=False)
    pueblo_originario = models.BooleanField(default=False)
    vih_positivo = models.BooleanField(default=False)
    vdrl_resultado = models.CharField(max_length=50, null=True, blank=True)
    vdrl_tratamiento = models.BooleanField(default=False)
    hepatitis_b_resultado = models.CharField(max_length=50, null=True, blank=True)
    profilaxis_completa = models.BooleanField(default=False)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo


class Parto(models.Model):
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE)
    fecha_parto = models.DateField()
    hora_parto = models.TimeField(null=True, blank=True)
    tipo_parto = models.CharField(max_length=50)
    ive_causal2 = models.BooleanField(default=False)
    acompanante_pabellon = models.BooleanField(default=False)
    clampeo_tardio = models.BooleanField(default=False)
    gases_cordon = models.BooleanField(default=False)
    apego_canguro = models.BooleanField(default=False)
    apego_tunel = models.BooleanField(default=False)
    profesional_responsable = models.CharField(max_length=150, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    edad_gestacional_semanas = models.IntegerField(null=True, blank=True)
    edad_gestacional_dias = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Parto de {self.madre.nombre_completo}"


class RecienNacido(models.Model):
    parto = models.ForeignKey(Parto, on_delete=models.CASCADE)
    apellido_paterno = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10)
    peso = models.IntegerField()
    talla = models.DecimalField(max_digits=4, decimal_places=1)
    circunferencia_craneana = models.DecimalField(max_digits=4, decimal_places=1)
    diagnostico = models.CharField(max_length=200, null=True, blank=True)
    malformacion_congenita = models.BooleanField(default=False)
    descripcion_malformacion = models.TextField(null=True, blank=True)
    apgar_1 = models.IntegerField(null=True, blank=True)
    apgar_5 = models.IntegerField(null=True, blank=True)
    reanimacion_basica = models.BooleanField(default=False)
    reanimacion_avanzada = models.BooleanField(default=False)
    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    vacuna_bcg = models.BooleanField(default=False)
    profesional_vacuna_vhb = models.CharField(max_length=150, null=True, blank=True)
    profilaxis_completa = models.BooleanField(default=False)
    semanas_gestacion = models.IntegerField(null=True, blank=True)
    dias_gestacion = models.IntegerField(null=True, blank=True)
    apego_inmediato = models.BooleanField(default=False)
    destino_final = models.CharField(max_length=50)
    notas_rn = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"RN de {self.parto.madre.nombre_completo}"


class VacunaBCG(models.Model):
    rn = models.ForeignKey(RecienNacido, on_delete=models.SET_NULL, null=True)

    nombre_completo_madre = models.CharField(max_length=150, null=True, blank=True)
    rut_madre = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento_madre = models.DateField(null=True, blank=True)
    fecha_nacimiento_hijo = models.DateField(null=True, blank=True)
    sexo_rn = models.CharField(max_length=10, null=True, blank=True)
    peso_rn = models.IntegerField(null=True, blank=True)

    aplicada = models.BooleanField(default=False)
    comuna = models.CharField(max_length=100)
    reaccion_adversa = models.CharField(max_length=100, null=True, blank=True)
    cama_ubicacion = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.rn:
            self.nombre_completo_madre = self.rn.parto.madre.nombre_completo
            self.rut_madre = self.rn.parto.madre.rut
            self.fecha_nacimiento_madre = self.rn.parto.madre.fecha_nacimiento
            self.fecha_nacimiento_hijo = self.rn.parto.fecha_parto
            self.sexo_rn = self.rn.sexo
            self.peso_rn = self.rn.peso
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vacuna BCG - RN {self.rn_id}"
