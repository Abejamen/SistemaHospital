from django import forms
from .models import Madre, Parto, RecienNacido, VacunaBCG


# =======================================================================================
# LISTAS OFICIALES MINSAL
# =======================================================================================

TIPO_PARTO_CHOICES = [
    ("PARTO_VAGINAL", "Parto vaginal"),
    ("PARTO_VAGINAL_INSTRUMENTAL", "Parto vaginal instrumental (Fórceps / Vacuum)"),
    ("CESAREA", "Cesárea"),
    ("CESAREA_URGENCIA", "Cesárea de urgencia"),
    ("CESAREA_ELECTIVA", "Cesárea electiva"),
]

CLASIFICACION_ROBSON_CHOICES = [
    ("G1", "G1 — Nulípara, feto único, cefálico, ≥ 37 sem, trabajo espontáneo"),
    ("G2A", "G2A — Nulípara, inducción"),
    ("G2B", "G2B — Nulípara, cesárea antes del trabajo de parto"),
    ("G3", "G3 — Multípara sin cesárea previa, feto único, cefálico, ≥ 37 sem, espontáneo"),
    ("G4A", "G4A — Multípara sin cesárea previa, inducción"),
    ("G4B", "G4B — Multípara sin cesárea previa, cesárea antes del trabajo de parto"),
    ("G5", "G5 — Cesárea previa, embarazo único, cefálico, ≥ 37 sem"),
    ("G6", "G6 — Feto podálico"),
    ("G7", "G7 — Embarazo múltiple"),
    ("G8", "G8 — Presentación anómala"),
    ("G9", "G9 — Pretérmino"),
    ("G10", "G10 — Muerte fetal"),
]

SEXO_RN_CHOICES = [
    ("M", "Masculino"),
    ("F", "Femenino"),
    ("I", "Indeterminado"),
]

DESTINO_FINAL_CHOICES = [
    ("SALA_COMUN", "Sala común"),
    ("UTI", "Unidad de Tratamiento Intermedio"),
    ("UCI", "Unidad de Cuidados Intensivos"),
    ("NEO_INTERMEDIO", "Neonatología Intermedio"),
    ("NEO_INTENSIVO", "Neonatología Intensivo"),
    ("DOMICILIO", "Alta a domicilio"),
]

RESULTADO_LAB_CHOICES = [
    ("NEGATIVO", "Negativo"),
    ("POSITIVO", "Positivo"),
    ("REACTIVO", "Reactivo"),
    ("NO_REALIZADO", "No realizado"),
    ("SIN_DATOS", "Sin datos"),
]


# =======================================================================================
# FORMULARIO MADRE
# =======================================================================================

class MadreForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Seleccione fecha de nacimiento",
            },
            format="%Y-%m-%d",
        ),
        help_text="Seleccione la fecha según documento de identidad.",
    )

    vdrl_resultado = forms.ChoiceField(
        choices=RESULTADO_LAB_CHOICES,
        required=False,
        help_text="Resultado del test VDRL según laboratorio.",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    hepatitis_b_resultado = forms.ChoiceField(
        choices=RESULTADO_LAB_CHOICES,
        required=False,
        help_text="Resultado del test Hepatitis B según laboratorio.",
        widget=forms.Select(attrs={"class": "form-control"})
    )

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
            "nombre_completo": forms.TextInput(attrs={
                "placeholder": "Nombre completo de la madre",
                "class": "form-control",
            }),
            "rut": forms.TextInput(attrs={
                "placeholder": "Ej: 12345678-9",
                "maxlength": "12",
                "class": "form-control",
            }),
            "edad": forms.NumberInput(attrs={
                "placeholder": "Edad materna",
                "min": "10",
                "max": "60",
            }),
            "comuna": forms.TextInput(attrs={"placeholder": "Comuna de residencia"}),
            "cesfam": forms.TextInput(attrs={"placeholder": "CESFAM de control prenatal"}),
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
            raise forms.ValidationError("La parte numérica debe ser solo números.")

        if not (dv.isdigit() or dv.lower() == "k"):
            raise forms.ValidationError("El dígito verificador debe ser número o K.")

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


# =======================================================================================
# FORMULARIO PARTO
# =======================================================================================

class PartoForm(forms.ModelForm):

    fecha_parto = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Seleccione fecha de parto",
            },
            format="%Y-%m-%d",
        ),
        help_text="Fecha del nacimiento registrada clínicamente.",
    )

    hora_parto = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
                "placeholder": "Hora del parto",
            }
        ),
        help_text="Indique la hora exacta del parto.",
    )

    tipo_parto = forms.ChoiceField(
        choices=TIPO_PARTO_CHOICES,
        required=False,
        help_text="Seleccione el tipo de parto según registro clínico.",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    clasificacion_robson = forms.ChoiceField(
        choices=CLASIFICACION_ROBSON_CHOICES,
        required=False,
        help_text="Seleccione la clasificación según el sistema Robson.",
        widget=forms.Select(attrs={"class": "form-control"})
    )

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
            "profesional_responsable": forms.TextInput(attrs={"placeholder": "Nombre del profesional"}),
            "observaciones": forms.Textarea(attrs={"rows": 2, "placeholder": "Observaciones clínicas"}),
            "motivo_no_acompanado": forms.Textarea(attrs={"rows": 2, "placeholder": "Motivo del no acompañamiento"}),
            "causa_cesarea": forms.Textarea(attrs={"rows": 2, "placeholder": "Causa de cesárea según ficha"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = False
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


# =======================================================================================
# FORMULARIO RN
# =======================================================================================

class RecienNacidoForm(forms.ModelForm):

    sexo = forms.ChoiceField(
        choices=SEXO_RN_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Seleccione el sexo asignado al nacer.",
    )

    destino_final = forms.ChoiceField(
        choices=DESTINO_FINAL_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Destino clínico del recién nacido.",
    )

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

        widgets = {
            "apellido_paterno": forms.TextInput(attrs={"placeholder": "Apellido paterno"}),
            "peso": forms.NumberInput(attrs={"placeholder": "Peso en gramos"}),
            "talla": forms.NumberInput(attrs={"placeholder": "Talla en cm"}),
            "circunferencia_craneana": forms.NumberInput(attrs={"placeholder": "Circunferencia craneana (cm)"}),
            "diagnostico": forms.TextInput(attrs={"placeholder": "Diagnóstico clínico"}),
            "descripcion_malformacion": forms.Textarea(attrs={"rows": 2, "placeholder": "Descripción de la malformación"}),
            "profesional_vacuna_vhb": forms.TextInput(attrs={"placeholder": "Profesional que aplica VHB"}),
            "notas_rn": forms.Textarea(attrs={"rows": 2, "placeholder": "Notas clínicas adicionales"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = False
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


# =======================================================================================
# FORMULARIO BCG
# =======================================================================================

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

        widgets = {
            "numero_registro": forms.TextInput(attrs={"placeholder": "N° de registro BCG"}),
            "comuna": forms.TextInput(attrs={"placeholder": "Comuna donde se aplica"}),
            "reaccion_adversa": forms.TextInput(attrs={"placeholder": "Descripción de reacción adversa"}),
            "cama_ubicacion": forms.TextInput(attrs={"placeholder": "Ubicación del RN al momento de vacunación"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = False
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})
