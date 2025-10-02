from django.db import models

class Candidatoinformacoes(models.Model):
    nome = models.CharField(max_length=200)
    altura = models.FloatField()
    peso = models.FloatField()
    velocidade_caminhada = models.CharField(max_length=50)
    sexo_desejado_cao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Caoinformacoes(models.Model):
    nome = models.CharField(max_length=200)
    raca = models.CharField(max_length=100)
    altura = models.FloatField()
    peso = models.FloatField()
    velocidade_caminhada = models.CharField(max_length=50)
    sexo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome