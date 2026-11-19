from django import forms
from .models import Candidato, Usuario, CaoGuia, FormacaoDupla
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')
        labels = {'username': 'User', 'email': 'Email'}
        help_texts = {'username': None}

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'tipo')
        labels = {'nome_usuario': 'Nome Completo', 'tipo': 'Tipo de Usuário'}


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        # Todos os campos do Candidato em uma única tela
        fields = [
            'id_candidato',
            'nome_candidato',
            'nascimento_candidato',
            'sexo',
            'altura',
            'peso',
            'velocidade_caminhada',
            'nivel_atividade',
            'complexidade_rotina',
            'caracteristicas_trajetos',
            'nivel_distracao_trajetos',
            'capacidade_conducao',
            'experiencia_cao_guia',
            'tipo_moradia',
            'caracteristicas_ambientais',
            'presenca_pessoas_animais',
            'necessidades_especificas',
            'cidade',
            'religiao',
            'estado_civil',
            'status',
        ]
        widgets = {
            'id_candidato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF'}),
            'nome_candidato': forms.TextInput(attrs={'class': 'form-control'}),
            'nascimento_candidato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 1.75'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ex: 70.5'}),
            'velocidade_caminhada': forms.Select(attrs={'class': 'form-control'}),
            'nivel_atividade': forms.Select(attrs={'class': 'form-control'}),
            'complexidade_rotina': forms.Select(attrs={'class': 'form-control'}),
            'caracteristicas_trajetos': forms.Select(attrs={'class': 'form-control'}),
            'nivel_distracao_trajetos': forms.Select(attrs={'class': 'form-control'}),
            'capacidade_conducao': forms.Select(attrs={'class': 'form-control'}),
            'experiencia_cao_guia': forms.Select(attrs={'class': 'form-control'}),
            'tipo_moradia': forms.Select(attrs={'class': 'form-control'}),
            'caracteristicas_ambientais': forms.Select(attrs={'class': 'form-control'}),
            'presenca_pessoas_animais': forms.Select(attrs={'class': 'form-control'}),
            'necessidades_especificas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'religiao': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_civil': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CaoGuiaForm(forms.ModelForm):
    class Meta:
        model = CaoGuia
        # Todos os campos do Cão-Guia em uma única tela
        fields = [
            'id_cao',
            'nome_cao',
            'raca',
            'sexo',
            'nascimento_cao',
            'altura',
            'peso',
            'velocidade',
            'temperamento',
            'nivel_energia',
            'sociabilidade',
            'convivio_animais',
            'concentracao',
            'nivel_distracao',
            'complexidade_trabalho',
            'exigencia_conducao',
            'necessidade_manejo',
            'historico_relevante',
            'inicio_treinamento',
            'termino_treinamento',
            'total_horas_treinadas',
            'treinador_responsavel',
        ]
        widgets = {
            'id_cao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Microchip ou ID'}),
            'nome_cao': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'nascimento_cao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 0.58 ou 58'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ex: 28.5'}),
            'velocidade': forms.Select(attrs={'class': 'form-control'}),
            'temperamento': forms.Select(attrs={'class': 'form-control'}),
            'nivel_energia': forms.Select(attrs={'class': 'form-control'}),
            'sociabilidade': forms.Select(attrs={'class': 'form-control'}),
            'convivio_animais': forms.Select(attrs={'class': 'form-control'}),
            'concentracao': forms.Select(attrs={'class': 'form-control'}),
            'nivel_distracao': forms.Select(attrs={'class': 'form-control'}),
            'complexidade_trabalho': forms.Select(attrs={'class': 'form-control'}),
            'exigencia_conducao': forms.Select(attrs={'class': 'form-control'}),
            'necessidade_manejo': forms.Select(attrs={'class': 'form-control'}),
            'historico_relevante': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inicio_treinamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'termino_treinamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_horas_treinadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'treinador_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
        }

CandidatoEtapa1Form = CandidatoForm
CandidatoEtapa2Form = CandidatoForm
CaoGuiaEtapa1Form = CaoGuiaForm
CaoGuiaEtapa2Form = CaoGuiaForm

class BuscaCaoForm(forms.Form):
    id_cao = forms.CharField(label='ID do Cão / Microchip', max_length=36)

class BuscaCPFForm(forms.Form):
    cpf = forms.CharField(label='Digite o CPF do Candidato', max_length=14)

class FormacaoDuplaForm(forms.ModelForm):
    class Meta:
        model = FormacaoDupla
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)