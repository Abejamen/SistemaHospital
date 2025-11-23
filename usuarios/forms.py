from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'correo@example.com'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '********'
        })
