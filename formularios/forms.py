from django import forms
from .models import Madre, Parto, RecienNacido, VacunaBCG


class MadreForm(forms.ModelForm):
    class Meta:
        model = Madre
        fields = [
            "nombre_completo",
            "rut",
            "fecha_nacimiento",
            "edad",
            "comuna",
            "cesfam",
            "migrante",
            "pueblo_originario",
            "vih_positivo",
            "vdrl_resultado",
            "vdrl_tratamiento",
            "hepatitis_b_resultado",
            "profilaxis_completa",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            )
        }

class PartoForm(forms.ModelForm):
    class Meta:
        model = Parto
        fields = [
            "fecha_parto",
            "hora_parto",
            "tipo_parto",
            "ive_causal2",
            "acompanante_pabellon",
            "clampeo_tardio",
            "gases_cordon",
            "apego_canguro",
            "apego_tunel",
            "profesional_responsable",
            "observaciones",
            "edad_gestacional_semanas",
            "edad_gestacional_dias",
        ]
        widgets = {
            "fecha_parto": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "hora_parto": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False

        self.fields["fecha_parto"].input_formats = ["%Y-%m-%d"]

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})



class RecienNacidoForm(forms.ModelForm):
    class Meta:
        model = RecienNacido
        fields = [
            "apellido_paterno",
            "sexo",
            "peso",
            "talla",
            "circunferencia_craneana",
            "diagnostico",
            "malformacion_congenita",
            "descripcion_malformacion",
            "apgar_1",
            "apgar_5",
            "reanimacion_basica",
            "reanimacion_avanzada",
            "profilaxis_ocular",
            "vacuna_hepatitis_b",
            "vacuna_bcg",
            "profesional_vacuna_vhb",
            "profilaxis_completa",
            "semanas_gestacion",
            "dias_gestacion",
            "apego_inmediato",
            "destino_final",
            "notas_rn",
        ]


class VacunaBCGForm(forms.ModelForm):
    class Meta:
        model = VacunaBCG
        fields = [
            "numero_registro",
            "aplicada",
            "comuna",
            "reaccion_adversa",
            "cama_ubicacion",
        ]