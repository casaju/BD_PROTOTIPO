from django import forms
from .models import teste

class testeForm(forms.ModelForm):
    class Meta:
        model = teste
        fields = '__all__'