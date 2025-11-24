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
            "rut": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "12",
                "placeholder": "Ej: 12345678-9"
            }),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
        }


    def clean_rut(self):
        rut = self.cleaned_data.get("rut")

        if not rut:
            raise forms.ValidationError("El RUT es obligatorio.")

        rut = rut.replace(".", "").replace(" ", "").strip()
        self.cleaned_data["rut"] = rut


        if len(rut) < 8 or len(rut) > 12:
            raise forms.ValidationError("El RUT no tiene un largo válido.")


        if "-" not in rut:
            raise forms.ValidationError("El RUT debe incluir guion. Ej: 12345678-9")

        numero, dv = rut.split("-")


        if not numero.isdigit():
            raise forms.ValidationError("La parte numérica del RUT solo debe contener números.")


        if not (dv.isdigit() or dv.lower() == "k"):
            raise forms.ValidationError("El dígito verificador debe ser número o 'K'.")


        query = Madre.objects.filter(rut=rut)


        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise forms.ValidationError("Este RUT ya está registrado.")

        return rut


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})



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
            "monitor",
            "ttc",
            "induccion",
            "alumno",
            "plan_parto",
            "alumbramiento_rigido",
            "clasificacion_robson",
            "acompanante_parto",
            "motivo_no_acompanado",
            "persona_acompanante",
            "acompanante_corta_cordon",
            "causa_cesarea",
            "uso_sala_saip",
            "recuerdos",
            "retira_placenta",
            "estampado_placenta",
            "manejo_dolor_farmacologico",
        ]

        widgets = {
            "fecha_parto": forms.DateInput(attrs={"type": "date"}),
            "hora_parto": forms.TimeInput(attrs={"type": "time"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
            "motivo_no_acompanado": forms.Textarea(attrs={"rows": 2}),
            "causa_cesarea": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for name, field in self.fields.items():
            field.required = False

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for name, field in self.fields.items():
            field.required = False

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})



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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for name, field in self.fields.items():
            field.required = False

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})
