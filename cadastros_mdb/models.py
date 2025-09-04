from django.db import models

class teste (models.Model):
    teste = models.CharField(max_length=100)

    def __str__(self):
        return self.teste

