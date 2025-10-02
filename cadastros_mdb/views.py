# pareamento/views.py

from django.shortcuts import render
from .models import Candidatoinformacoes, Caoinformacoes
import math

# A função de cálculo que você já tem
def calcular_pontuacao_compatibilidade(candidato, caes_disponiveis):
    
    # 1. Definição dos Pesos (Ponderação) dos critérios
    pesos = {
        "altura": 0.35,
        "peso": 0.25,
        "velocidade_caminhada": 0.30,
        "sexo": 0.10
    }
    
    # Lista para armazenar os resultados de pareamento
    resultados_pareamento = []
    
    # 2. Iterar sobre os cães disponíveis e calcular a pontuação para cada um
    for cao in caes_disponiveis:
        pontuacao_total = 0
        
        # Pontuação da Altura
        # A pontuação é inversamente proporcional à diferença de altura
        # Usamos uma fórmula de penalidade
        diferenca_altura = abs(candidato["altura"] - cao["altura"])
        pontuacao_altura = max(0, 10 - diferenca_altura * 5) # O '5' é um fator de penalidade ajustável
        pontuacao_total += pontuacao_altura * pesos["altura"]

        # Pontuação do Peso
        # Mesma lógica da altura
        diferenca_peso = abs(candidato["peso"] - cao["peso"])
        pontuacao_peso = max(0, 10 - diferenca_peso * 0.5) # O '0.5' é um fator de penalidade ajustável
        pontuacao_total += pontuacao_peso * pesos["peso"]

        # Pontuação da Velocidade
        # Critério categórico, com pontuação exata por nível de compatibilidade
        if candidato["velocidade_caminhada"] == cao["velocidade_caminhada"]:
            pontuacao_velocidade = 10
        elif (candidato["velocidade_caminhada"] == "alta" and cao["velocidade_caminhada"] == "moderada") or \
            (candidato["velocidade_caminhada"] == "baixa" and cao["velocidade_caminhada"] == "moderada"):
            pontuacao_velocidade = 5
        else:
            pontuacao_velocidade = 0
        pontuacao_total += pontuacao_velocidade * pesos["velocidade_caminhada"]
        
        # Pontuação do Sexo
        # Critério categórico
        if candidato["sexo_desejado_cao"] == "indiferente" or \
        candidato["sexo_desejado_cao"] == cao["sexo"]:
            pontuacao_sexo = 10
        else:
            pontuacao_sexo = 0
        pontuacao_total += pontuacao_sexo * pesos["sexo"]
        
        # Armazenar o resultado
        resultados_pareamento.append({
            "nome_cao": cao["nome"],
            "pontuacao": round(pontuacao_total, 2)
        })
        
    # 3. Ordenar os resultados pela pontuação de forma decrescente
    resultados_pareamento.sort(key=lambda x: x["pontuacao"], reverse=True)
    
    return resultados_pareamento

def parear_candidato_cao(request, candidato_id):
    candidato = Candidatoinformacoes.objects.get(id=candidato_id)
    caes_disponiveis = list(Caoinformacoes.objects.all()) # Converte a queryset em uma lista

    melhores_pares = calcular_pontuacao_compatibilidade(candidato, caes_disponiveis)
    
    # Agora você pode passar esses dados para o template
    context = {
        'candidato': candidato,
        'pares': melhores_pares
    }
    
    return render(request, 'pareamento/resultado.html', context)