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
        ('1', 'Baixa'),
        ('2', 'Média'),
        ('3', 'Moderada'),
        ('4', 'Rápida'),
        ('5', 'Muito Rápida'),
    ]
    
    AMBIENTE_CHOICES = [
        ('1', 'Rural'),
        ('2', 'Urbano'),
        ('3', 'Barulhento'),
        ('4', 'Calmo'),
        ('5', 'Animais'),
    ]

    SOCIABILIDADE_CHOICES = [
            ('1', 'Baixa'),
            ('2', 'Média'),
            ('3', 'Moderada'),
            ('4', 'Sociável'),
            ('5', 'Muito Sociável'),
        ]
    # --- ETAPA 1 (Identificação e Básico) ---
    id_cao = models.CharField(
        primary_key=True, 
        unique=True, 
        max_length=36,
        verbose_name="ID do Cão / Microchip",
    )
    nome_cao = models.CharField(max_length=255)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10) 
    nascimento_cao = models.DateField()
    
    # --- ETAPA 2 (Dados Técnicos e Complementares) ---
    peso_cao = models.FloatField(null=True, blank=True)
    altura = models.FloatField(verbose_name="Altura (cm)", null=True, blank=True)
    velocidade_caminhada = models.CharField(
        max_length=20, 
        choices=VELOCIDADE_CHOICES, 
        null=True, 
        blank=True,
    )
    ambiente_preferencial = models.CharField(
        max_length=20, 
        choices=AMBIENTE_CHOICES, 
        null=True, 
        blank=True,
    )
    sociabilidade = models.CharField(
        max_length=20, 
        choices=SOCIABILIDADE_CHOICES, 
        null=True, 
        blank=True,
    )
    # Dados de Treinamento (Etapa 2)
    inicio_treinamento = models.DateField(null=True, blank=True)
    termino_treinamento = models.DateField(null=True, blank=True)
    total_horas_treinadas = models.IntegerField(null=True, blank=True)
    treinador_responsavel = models.CharField(max_length=255, null=True, blank=True)

    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    def __str__(self):
        return self.nome_cao

class Candidato(models.Model):
    # Opções
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    VELOCIDADE_CHOICES = [
        ('1', 'Baixa'),
        ('2', 'Média'),
        ('3', 'Moderada'),
        ('4', 'Rápida'),
        ('5', 'Muito Rápida'),
    ]
    
    AMBIENTE_CHOICES = [
        ('1', 'Rural'),
        ('2', 'Urbano'),
        ('3', 'Barulhento'),
        ('4', 'Calmo'),
        ('5', 'Animais'),
    ]

    EXPERIENCIA_CHOICES = [
        ('0', 'Não'),
        ('1', 'Sim'),
    ]

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
    velocidade_caminhada = models.CharField(
        max_length=20,
        choices=VELOCIDADE_CHOICES,
        null=True,
        blank=True
    )

    ambiente_moradia = models.CharField(
        max_length=20, choices=AMBIENTE_CHOICES,
        null=True,
        blank=True)
    
    experiencia_com_caes = models.CharField(
        max_length=1,)
    # Outros
    estado_civil = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Considerado.choices, default=Considerado.APTO)

    def __str__(self):
        return f"{self.nome_candidato} ({self.id_candidato})"

class FormacaoDupla(models.Model):
    id_dupla = models.AutoField(primary_key=True, unique=True)
    cao = models.ForeignKey(CaoGuia, null=True, on_delete=models.SET_NULL)
    Candidato = models.ForeignKey(Candidato, null=True, on_delete=models.SET_NULL)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

