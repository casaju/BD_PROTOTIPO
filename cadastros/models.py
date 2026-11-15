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
    altura = models.FloatField()
    peso = models.FloatField()
    velocidade = models.CharField(choices=[('Lenta', 'Lenta'), ('Média', 'Média'), ('Rápida', 'Rápida')])
    nivel_energia = models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')])
    complexidade_trabalho = models.CharField(choices=[('Média', 'Média'), ('Alta', 'Alta')])
    exigencia_conducao = models.CharField(choices=[('Média', 'Média'), ('Alta', 'Alta')])
    concentracao = models.CharField(choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')])
    sociabilidade = models.CharField(choices=[('Baixa', 'Baixa'), ('Alta', 'Alta')]) # Convívio com pessoas/animais
    temperamento = models.CharField(choices=[('Calmo', 'Calmo'), ('Agitado', 'Agitado')])
    necessidade_manejo = models.CharField(choices=[('Baixa', 'Baixa'), ('Alta', 'Alta')]) # Relacionado à experiência de treinamento
    nome_cao = models.CharField(max_length=255)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10) 
    nascimento_cao = models.DateField()
    inicio_treinamento = models.DateField(null=True, blank=True)
    termino_treinamento = models.DateField(null=True, blank=True)
    total_horas_treinadas = models.IntegerField(null=True, blank=True)
    treinador_responsavel = models.CharField(max_length=255, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    def __str__(self):
        return self.nome_cao

class Candidato(models.Model):
    altura = models.FloatField()
    peso = models.FloatField()
    velocidade_caminhada = models.CharField(choices=[('Lenta', 'Lenta'), ('Média', 'Média'), ('Rápida', 'Rápida')])
    nivel_atividade = models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')])
    complexidade_rotina = models.CharField(choices=[('Média', 'Média'), ('Alta', 'Alta')])
    capacidade_conducao = models.CharField(choices=[('Média', 'Média'), ('Alta', 'Alta')])
    nivel_distracao_trajetos = models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')])
    presenca_pessoas_animais = models.CharField(choices=[('Baixa', 'Baixa'), ('Alta', 'Alta')]) # Sociabilidade exigida
    caracteristicas_ambientais = models.CharField(choices=[('Tranquilo', 'Tranquilo'), ('Movimentado', 'Movimentado')])
    experiencia_cao_guia = models.CharField(choices=[('Nenhuma', 'Nenhuma'), ('Iniciante', 'Iniciante'), ('Experiente', 'Experiente')])

    class Considerado(models.TextChoices):
        APTO = 'Apto', 'Apto'
        INAPTO = 'Inapto', 'Inapto'

    id_candidato = models.CharField(
        primary_key=True, 
        max_length=14, 
        verbose_name="CPF", 
        help_text="Digite o CPF (apenas números ou com pontuação)"
    )
    nome_candidato = models.CharField(max_length=255)
    nascimento_candidato = models.DateField()
    sexo = models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')])
    cidade = models.CharField(max_length=100, null=True, blank=True)
    religiao = models.CharField(max_length=100, null=True, blank=True)
    TIPO_MORADIA_CHOICES = [
        ('casa_com_quintal', 'Casa com quintal'),
        ('casa_sem_quintal', 'Casa sem quintal'),
        ('apartamento_elevador', 'Apartamento com elevador'),
        ('apartamento_escada', 'Apartamento com escada (sem elevador)'),
        ('area_rural', 'Sítio / Chácara / Área Rural'),
        ]
    tipo_moradia = models.CharField(
        max_length=30, 
        choices=TIPO_MORADIA_CHOICES, 
        verbose_name="Tipo de Moradia"
        )
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

