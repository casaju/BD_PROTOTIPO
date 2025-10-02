from django import forms
from .models import Candidato, Usuario, CaoGuia, FormacaoDupla
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')
        labels = {
            'username': 'User',
            'email': 'Email',
        }
        help_texts = {
            'username': None, # Remove a ajuda do campo username
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'tipo')
        labels = {
            'nome_usuario': 'Nome Completo',
            'tipo': 'Tipo de Usuário',
        }

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