from django import forms
from .models import Madre, Parto, RecienNacido


class MadreForm(forms.ModelForm):
    class Meta:
        model = Madre
        fields = [
            'nombre_completo_madre', 'rut', 'fecha_nac_madre', 'edad_materna',
            'comuna', 'cesfam', 'madre_vih', 'vdrl_materno',
            'hepatitis_b_materno', 'migrante', 'pueblo_originario',
            'e_paridad', 'g_gestaciones'
        ]
        widgets = {
            'fecha_nac_madre': forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
                self.fields['fecha_nac_madre'].input_formats = ['%Y-%m-%d']
            else:
                field.widget.attrs.update({'class': 'form-control'})


class PartoForm(forms.ModelForm):
    class Meta:
        model = Parto
        fields = [
            'fecha_nac', 'hora', 'tipo_parto', 'gases_cordon',
            'apego_canguro', 'apego_tunel', 'clampeo_tardio',
            'ive_causal_2', 'destino_rn', 'alojamiento_conjunto_puerperio',
            'lactancia_antes_60min', 'acompanante_en_pabellon',
            'observaciones_parto', 'interno', 'resultado_examen_1',
            'resultado_examen_2', 'tratamiento_parto'
        ]
        widgets = {
            'fecha_nac': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'hora': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_nac'].input_formats = ['%Y-%m-%d']

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})



class RecienNacidoForm(forms.ModelForm):
    class Meta:
        model = RecienNacido
        fields = [
            'apellido_paterno_rn', 'sexo', 'peso', 'talla',
            'circunferencia_craneana', 'diagnostico',
            'malformacion_congenita', 'descripcion_malformacion',
            'apgar_1min', 'apgar_5min', 'reanimacion_basica',
            'reanimacion_avanzada', 'profilaxis_ocular',
            'vacuna_hepatitis_b', 'vacuna_bcg',
            'profesional_que_vacuna_vhb', 'profilaxis_completa',
            'semanas_gestacion', 'dias_gestacion', 'apego_inmediato',
            'destino_final', 'notas_rn'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
