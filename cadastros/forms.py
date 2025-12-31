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

class CaoGuiaEtapa1Form(forms.ModelForm):
    class Meta:
        model = CaoGuia
        fields = ['id_cao', 'nome_cao', 'raca', 'sexo', 'nascimento_cao']
        widgets = {
            'nascimento_cao': forms.DateInput(attrs={'type': 'date'}),
        }

class BuscaCaoForm(forms.Form):
    id_cao = forms.CharField(label='ID do Cão / Microchip', max_length=36)

# --- ATUALIZADO: Campos novos (Ambiente, Sociabilidade, Altura) ---
class CaoGuiaEtapa2Form(forms.ModelForm):
    class Meta:
        model = CaoGuia
        fields = [
            'peso_cao', 'altura', 'velocidade_caminhada',
            'ambiente_preferencial', 'sociabilidade',
            'inicio_treinamento', 'termino_treinamento', 
            'total_horas_treinadas', 'treinador_responsavel'
        ]
        labels = {
            'altura': 'Altura (cm)',
            'velocidade_caminhada': 'Nível de Velocidade (1-5)',
            'ambiente_preferencial': 'Ambiente Ideal',
            'sociabilidade': 'Nível de Sociabilidade'
        }
        widgets = {
            'inicio_treinamento': forms.DateInput(attrs={'type': 'date'}),
            'termino_treinamento': forms.DateInput(attrs={'type': 'date'}),
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