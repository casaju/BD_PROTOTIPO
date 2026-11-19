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
    id_cao = models.CharField(
        primary_key=True,
        max_length=36,
        default=uuid.uuid4,
        verbose_name="ID do Cão / Microchip"
    )
    nome_cao = models.CharField(max_length=255, verbose_name="Nome do Cão")
    raca = models.CharField(max_length=100, verbose_name="Raça")
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    nascimento_cao = models.DateField(verbose_name="Data de Nascimento")
    altura = models.FloatField(help_text="Altura em cm (ex: 58) ou metros (ex: 0.58)")
    peso = models.FloatField(help_text="Peso em kg (ex: 28.5)")
    velocidade = models.CharField(
        max_length=20,
        choices=[('Lenta', 'Lenta'), ('Média', 'Média'), ('Rápida', 'Rápida')],
        verbose_name="Velocidade"
    )
    temperamento = models.CharField(
        max_length=20,
        choices=[('Calmo', 'Calmo'), ('Equilibrado', 'Equilibrado'), ('Agitado', 'Agitado')],
        null=True, blank=True
    )
    nivel_energia = models.CharField(
        max_length=20,
        choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')],
        null=True, blank=True,
        verbose_name="Nível de Energia"
    )
    sociabilidade = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Sociabilidade (Pessoas)"
    )
    convivio_animais = models.CharField(
        max_length=20,
        choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')],
        null=True, blank=True,
        verbose_name="Convívio com Outros Animais"
    )
    concentracao = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Concentração"
    )
    nivel_distracao = models.CharField(
        max_length=20,
        choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')],
        null=True, blank=True,
        verbose_name="Nível de Distração do Cão"
    )
    complexidade_trabalho = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Capacidade / Complexidade de Trabalho"
    )
    exigencia_conducao = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Nível de Condução Exigido"
    )
    necessidade_manejo = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Experiência de Treinamento / Exigência de Manejo"
    )
    historico_relevante = models.TextField(
        null=True, blank=True,
        verbose_name="Histórico Relevante (Saúde, sensibilidades, observações)"
    )
    inicio_treinamento = models.DateField(null=True, blank=True)
    termino_treinamento = models.DateField(null=True, blank=True)
    total_horas_treinadas = models.IntegerField(null=True, blank=True)
    treinador_responsavel = models.CharField(max_length=255, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    def __str__(self):
        return f"{self.nome_cao} ({self.id_cao})"


class Candidato(models.Model):
    class Considerado(models.TextChoices):
        APTO = 'Apto', 'Apto'
        INAPTO = 'Inapto', 'Inapto'

    TIPO_MORADIA_CHOICES = [
        ('casa_com_quintal', 'Casa com quintal'),
        ('casa_sem_quintal', 'Casa sem quintal'),
        ('apartamento_elevador', 'Apartamento com elevador'),
        ('apartamento_escada', 'Apartamento com escada (sem elevador)'),
        ('area_rural', 'Sítio / Chácara / Área Rural'),
    ]

    id_candidato = models.CharField(
        primary_key=True,
        max_length=14,
        verbose_name="CPF",
        help_text="Digite o CPF (apenas números ou com pontuação)"
    )
    nome_candidato = models.CharField(max_length=255, verbose_name="Nome Completo")
    nascimento_candidato = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(max_length=1, choices=[('F', 'Feminino'), ('M', 'Masculino')])
    altura = models.FloatField(help_text="Altura em metros (ex: 1.70) ou cm (ex: 170)")
    peso = models.FloatField(help_text="Peso em kg (ex: 70.5)")
    velocidade_caminhada = models.CharField(
        max_length=20,
        choices=[('Lenta', 'Lenta'), ('Média', 'Média'), ('Rápida', 'Rápida')],
        verbose_name="Velocidade de Caminhada"
    )
    nivel_atividade = models.CharField(
        max_length=20,
        choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')],
        null=True, blank=True,
        verbose_name="Rotina e Nível de Atividade"
    )
    complexidade_rotina = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Complexidade da Rotina"
    )
    caracteristicas_trajetos = models.CharField(
        max_length=30,
        choices=[
            ('Simples/Retilíneos', 'Simples / Retilíneos / Calçadas regulares'),
            ('Mistos/Moderados', 'Mistos / Obstáculos moderados'),
            ('Complexos/Transporte Público', 'Complexos / Múltiplos modais / Centros urbanos'),
        ],
        null=True, blank=True,
        verbose_name="Características dos Trajetos"
    )
    nivel_distracao_trajetos = models.CharField(
        max_length=20,
        choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto')],
        null=True, blank=True,
        verbose_name="Nível de Estímulos / Distrações nos Trajetos"
    )
    capacidade_conducao = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Capacidade de Condução / Manejo"
    )
    experiencia_cao_guia = models.CharField(
        max_length=20,
        choices=[('Nenhuma', 'Nenhuma'), ('Iniciante', 'Iniciante'), ('Experiente', 'Experiente')],
        null=True, blank=True,
        verbose_name="Experiência Anterior com Cão-Guia"
    )
    tipo_moradia = models.CharField(
        max_length=30,
        choices=TIPO_MORADIA_CHOICES,
        verbose_name="Ambiente de Moradia",
        null=True, blank=True
    )
    caracteristicas_ambientais = models.CharField(
        max_length=20,
        choices=[('Tranquilo', 'Tranquilo'), ('Moderado', 'Moderado'), ('Movimentado', 'Movimentado')],
        null=True, blank=True,
        verbose_name="Características Ambientais da Rotina"
    )
    presenca_pessoas_animais = models.CharField(
        max_length=20,
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')],
        null=True, blank=True,
        verbose_name="Presença de Pessoas / Outros Animais"
    )
    necessidades_especificas = models.TextField(
        null=True, blank=True,
        verbose_name="Necessidades Específicas Relacionadas ao Uso do Cão-Guia"
    )
    cidade = models.CharField(max_length=100, null=True, blank=True)
    religiao = models.CharField(max_length=100, null=True, blank=True)
    estado_civil = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Considerado.choices,
        default=Considerado.APTO
    )

    def __str__(self):
        return f"{self.nome_candidato} ({self.id_candidato})"


class FormacaoDupla(models.Model):
    id_dupla = models.AutoField(primary_key=True, unique=True)
    cao = models.ForeignKey(CaoGuia, null=True, on_delete=models.SET_NULL)
    Candidato = models.ForeignKey(Candidato, null=True, on_delete=models.SET_NULL)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

