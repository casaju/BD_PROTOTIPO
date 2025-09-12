from django import forms
from .models import Candidato, Usuario, CaoGuia, FormacaoDupla
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Obrigatório. Digite um email válido.')
    class Meta(UserCreationForm.Meta):
        # A senha é automaticamente tratada pelo UserCreationForm
        fields = ('username', 'email')

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Exibe apenas os campos nome_usuario e tipo no formulário
        fields = ('nome_usuario', 'tipo')

class CaoGuiaForm(forms.ModelForm):
    class Meta:
        model = CaoGuia
        fields = '__all__'

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'

class FormacaoDuplaForm(forms.ModelForm):
    class Meta:
        model = FormacaoDupla
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)