from django.db import models

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nome_usuario = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_usuario


class CaoGuia(models.Model):
    id_cao = models.IntegerField(primary_key=True)
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
    class Considerado(models.TextChoices):
        APTO = 'Apto', 'Apto'
        INAPTO = 'Inapto', 'Inapto'

    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nome_candidato = models.CharField(max_length=255)
    nascimento_candidato = models.DateField()
    altura = models.FloatField()
    peso_candidato = models.FloatField()
    estado_civil = models.CharField(max_length=100)
    religiao = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=Considerado.choices)

    def __str__(self):
        return self.nome_candidato


class FormacaoDupla(models.Model):
    id_cao = models.ForeignKey(CaoGuia, null=True, on_delete=models.SET_NULL)
    id_usuario = models.ForeignKey(Candidato, null=True, on_delete=models.SET_NULL)
    data_inicio = models.DateField()
    data_fim = models.DateField()
