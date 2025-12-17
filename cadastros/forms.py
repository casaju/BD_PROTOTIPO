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

#formulário da Etapa 1
class CandidatoEtapa1Form(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['id_candidato', 'nome_candidato', 'nascimento_candidato', 'sexo', 'cidade']
        labels = {'id_candidato': 'CPF'}
        widgets = {
            'nascimento_candidato': forms.DateInput(attrs={'type': 'date'}),
        }

# Formulário Etapa 2: Dados complementares
class CandidatoEtapa2Form(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['peso_candidato', 'altura', 'religiao', 'velocidade_caminhada', 'sexo_desejado_cao']

# Novo Formulário: Apenas para verificar o CPF antes de entrar na Etapa 2
class BuscaCPFForm(forms.Form):
    cpf = forms.CharField(label='Digite o CPF do Candidato', max_length=14)

class FormacaoDuplaForm(forms.ModelForm):
    class Meta:
        model = FormacaoDupla
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)