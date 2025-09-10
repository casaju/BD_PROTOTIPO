from django import forms
from .models import Candidato, Usuario, CaoGuia, FormacaoDupla

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class CaoGuiaForm(forms.ModelForm):
    class Meta:
        model = CaoGuia
        fields = '__all__'

class FormacaoDuplaForm(forms.ModelForm):
    class Meta:
        model = FormacaoDupla
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)