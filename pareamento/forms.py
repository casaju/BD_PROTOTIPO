from django import forms
from cadastros.models import Candidato # Importando do outro app

class SelecaoPareamentoForm(forms.Form):
    candidato = forms.ModelChoiceField(
        queryset=Candidato.objects.filter(status='Apto'),
        label="Selecione o Candidato Apto",
        empty_label="--- Selecione um Candidato ---",
        widget=forms.Select(attrs={'class': 'form-control'})
    )