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
    # Opções
    VELOCIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('moderada', 'Moderada'),
        ('alta', 'Alta'),
    ]
    
    # --- ETAPA 1 (Identificação e Básico) ---
    id_cao = models.CharField(
        primary_key=True, 
        unique=True, 
        max_length=36,
        verbose_name="ID do Cão / Microchip",
        help_text="Número de identificação único"
    )
    nome_cao = models.CharField(max_length=255)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10) # Pode usar choices se quiser
    nascimento_cao = models.DateField()
    
    # --- ETAPA 2 (Dados Técnicos e Complementares) ---
    peso_cao = models.FloatField(null=True, blank=True)
    tamanho = models.FloatField(verbose_name="Altura (cm)", null=True, blank=True)
    velocidade_caminhada = models.CharField(
        max_length=20, 
        choices=VELOCIDADE_CHOICES, 
        null=True, 
        blank=True
    )
    
    # Dados de Treinamento (Etapa 2)
    inicio_treinamento = models.DateField(null=True, blank=True)
    termino_treinamento = models.DateField(null=True, blank=True)
    total_horas_treinadas = models.IntegerField(null=True, blank=True)
    treinador_responsavel = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome_cao

class Candidato(models.Model):
    # Opções
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    VELOCIDADE_CHOICES = [('baixa', 'Baixa'), ('moderada', 'Moderada'), ('alta', 'Alta')]
    PREFERENCIA_SEXO_CAO = [('M', 'Macho'), ('F', 'Fêmea'), ('indiferente', 'Indiferente')]
    
    class Considerado(models.TextChoices):
        APTO = 'Apto', 'Apto'
        INAPTO = 'Inapto', 'Inapto'

    # --- IDENTIFICADOR AGORA É O CPF ---
    # Removemos o default=uuid e o editable=False, pois o usuário vai digitar
    id_candidato = models.CharField(
        primary_key=True, 
        max_length=14, 
        verbose_name="CPF", 
        help_text="Digite o CPF (apenas números ou com pontuação)"
    )

    # --- ETAPA 1 ---
    nome_candidato = models.CharField(max_length=255)
    nascimento_candidato = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    
    # --- ETAPA 2 ---
    altura = models.FloatField(null=True, blank=True)
    peso_candidato = models.FloatField(null=True, blank=True)
    religiao = models.CharField(max_length=100, null=True, blank=True)
    velocidade_caminhada = models.CharField(max_length=20, choices=VELOCIDADE_CHOICES, null=True, blank=True)
    sexo_desejado_cao = models.CharField(max_length=20, choices=PREFERENCIA_SEXO_CAO, null=True, blank=True)
    
    # Outros
    estado_civil = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Considerado.choices, default=Considerado.APTO)

    def __str__(self):
        return f"{self.nome_candidato} ({self.id_candidato})"

class FormacaoDupla(models.Model):
    
    cao = models.ForeignKey(CaoGuia, null=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(Candidato, null=True, on_delete=models.SET_NULL)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)


