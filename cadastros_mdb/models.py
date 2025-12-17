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
    # Campo para vincular ao ID do CaoGuia do banco de dados relacional
    id_cao = models.CharField(max_length=36, unique=True, null=True, blank=True)
    
    # Adicione os campos restantes para o MongoDB
    altura = models.FloatField()
    peso = models.FloatField()
    sexo = models.CharField(max_length=50)
    velocidade_caminhada = models.CharField(max_length=50)
    def __str__(self):
        return f"Informações de {self.id_cao}"