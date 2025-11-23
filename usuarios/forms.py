from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.core.exceptions import ValidationError

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "correo@example.com"
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "********"
        })


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=50,
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"})
    )

    last_name = forms.CharField(
        max_length=50,
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Correo"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Contraseña",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmar contraseña",
        })


        self.fields["password2"].error_messages.update({
            "password_mismatch": "Las contraseñas no coinciden."
        })


    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        return password


    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = "MATRONA"
        user.save()
        return user
