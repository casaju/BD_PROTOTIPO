from django.db import models
from django.contrib.auth.models import User
import uuid

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, unique=True)
    nome_usuario = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_usuario


class CaoGuia(models.Model):
    id_cao = models.CharField(primary_key=True, unique=True, max_length=36)
    nome_cao = models.CharField(max_length=255)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10)
    nascimento_cao = models.DateField()
    peso_cao = models.FloatField()
    tamanho = models.FloatField()
    inicio_treinamento = models.DateField()
    termino_treinamento = models.DateField()
    total_horas_treinadas = models.IntegerField()
    treinador_responsavel = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_cao


class Candidato(models.Model):
    # Opções (Choices)
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    VELOCIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('moderada', 'Moderada'),
        ('alta', 'Alta'),
    ]
    
    PREFERENCIA_SEXO_CAO = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
        ('indiferente', 'Indiferente'),
    ]

    class Considerado(models.TextChoices):
        APTO = 'Apto', 'Apto'
        INAPTO = 'Inapto', 'Inapto'

    # --- IDENTIFICADOR (Chave Primária) ---
    # Esta linha é crucial. Ela impede que o Django tente criar o campo 'id' automático.
    id_candidato = models.CharField(primary_key=True, unique=True, max_length=36, default=uuid.uuid4, editable=False)

    # --- ETAPA 1 (Dados Pessoais) ---
    nome_candidato = models.CharField(max_length=255)
    nascimento_candidato = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    
    # --- ETAPA 2 (Dados Técnicos e Preferências) ---
    altura = models.FloatField(null=True, blank=True)
    peso_candidato = models.FloatField(null=True, blank=True)
    religiao = models.CharField(max_length=100, null=True, blank=True)
    velocidade_caminhada = models.CharField(max_length=20, choices=VELOCIDADE_CHOICES, null=True, blank=True)
    sexo_desejado_cao = models.CharField(max_length=20, choices=PREFERENCIA_SEXO_CAO, null=True, blank=True)
    
    # Outros Campos
    estado_civil = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Considerado.choices, default=Considerado.APTO)

    def __str__(self):
        return self.nome_candidato


class FormacaoDupla(models.Model):
    
    cao = models.ForeignKey(CaoGuia, null=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(Candidato, null=True, on_delete=models.SET_NULL)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)


