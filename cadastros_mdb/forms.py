from django import forms
from .models import Candidatoinformacoes, Caoinformacoes
from cadastros.models import CaoGuia # Importe o modelo do app 'cadastros'

class CandidatoinformacoesForm(forms.ModelForm):
    class Meta:
        model = Candidatoinformacoes
        fields = '__all__'

class CaoinformacoesForm(forms.ModelForm):
    # Campo para selecionar o cão-guia do banco de dados relacional
    cao = forms.ModelChoiceField(
        queryset=CaoGuia.objects.all(),
        label="Selecione o Cão-Guia",
        empty_label="---"
    )

    class Meta:
        model = Caoinformacoes
        fields = ['velocidade_caminhada']