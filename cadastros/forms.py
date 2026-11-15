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
            'username': None,
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'tipo')
        labels = {
            'nome_usuario': 'Nome Completo',
            'tipo': 'Tipo de Usuário',
        }

class CandidatoEtapa1Form(forms.ModelForm):
    class Meta:
        model = Candidato
        # Etapa 1: Foco em Identificação e Dados Físicos
        fields = [
            'id_candidato',
            'nome_candidato', 
            'nascimento_candidato', 
            'sexo', 
            'altura', 
            'peso', 
            'velocidade_caminhada'
        ]
        widgets = {
            'id_candidato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF'}),
            'nome_candidato': forms.TextInput(attrs={'class': 'form-control'}),
            'nascimento_candidato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 1.75'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ex: 70.5'}),
            'velocidade_caminhada': forms.Select(attrs={'class': 'form-control'}),
        }
class BuscaCaoForm(forms.Form):
    id_cao = forms.CharField(label='ID do Cão / Microchip', max_length=36)

# --- ATUALIZADO: Campos novos (Ambiente, Sociabilidade, Altura) ---
class CandidatoEtapa2Form(forms.ModelForm):
    class Meta:
        model = Candidato
        # Etapa 2: Foco em Rotina, Comportamento e Ambiente de Moradia
        fields = [
            'tipo_moradia',
            'mora_com_criancas',
            'ambiente_muito_movimentado',
            'possui_outros_animais',
            'nivel_atividade',
            'complexidade_rotina',
            'capacidade_conducao',
            'nivel_distracao_trajetos',
            'caracteristicas_ambientais',
            'experiencia_cao_guia'
        ]
        widgets = {
            'tipo_moradia': forms.Select(attrs={'class': 'form-control'}),
            'mora_com_criancas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ambiente_muito_movimentado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'possui_outros_animais': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nivel_atividade': forms.Select(attrs={'class': 'form-control'}),
            'complexidade_rotina': forms.Select(attrs={'class': 'form-control'}),
            'capacidade_conducao': forms.Select(attrs={'class': 'form-control'}),
            'nivel_distracao_trajetos': forms.Select(attrs={'class': 'form-control'}),
            'caracteristicas_ambientais': forms.Select(attrs={'class': 'form-control'}),
            'experiencia_cao_guia': forms.Select(attrs={'class': 'form-control'}),
        }

class CandidatoEtapa1Form(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['id_candidato', 'nome_candidato', 'nascimento_candidato', 'sexo', 'cidade']
        labels = {'id_candidato': 'CPF'}
        widgets = {
            'nascimento_candidato': forms.DateInput(attrs={'type': 'date'}),
        }

# --- ATUALIZADO: Novos campos e remoção de sexo_desejado_cao ---
class CandidatoEtapa2Form(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = [
            'peso_candidato', 'altura', 'religiao', 
            'velocidade_caminhada', 'ambiente_moradia', 
            'experiencia_com_caes', 'estado_civil'
        ]
        labels = {
            'velocidade_caminhada': 'Sua Velocidade de Caminhada (1-5)',
            'ambiente_moradia': 'Onde você mora?',
            'experiencia_com_caes': 'Possui experiência com cães?',
        }
        widgets = {
            'experiencia_com_caes': forms.Select(choices=[('0', 'Não'), ('1', 'Sim')])
        }

class BuscaCPFForm(forms.Form):
    cpf = forms.CharField(label='Digite o CPF do Candidato', max_length=14)

class FormacaoDuplaForm(forms.ModelForm):
    class Meta:
        model = FormacaoDupla
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)