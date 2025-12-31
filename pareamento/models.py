from django.db import models
from cadastros.models import Candidato, CaoGuia

class Matching(models.Model):
    # Relacionamentos com as tabelas do outro app
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    cao = models.ForeignKey(CaoGuia, on_delete=models.CASCADE)
    
    # Campos de dados
    score_total = models.DecimalField(max_digits=5, decimal_places=2)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.nome_candidato} + {self.cao.nome_cao} = {self.score_total}"
