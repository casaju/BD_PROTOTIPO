# pareamento/views.py

from django.shortcuts import render, redirect
from .forms import CandidatoinformacoesForm, CaoinformacoesForm 
from .models import Candidatoinformacoes, Caoinformacoes
from cadastros.models import CaoGuia
import math

def informacoes_candidato(request):
    if request.method == 'POST':
        form = CandidatoinformacoesForm(request.POST) # Use a classe de formulário
        if form.is_valid():
            form.save()
            return redirect('informacoes_candidato')
    else:
        form = CandidatoinformacoesForm() # Use a classe de formulário
    
    candidatos_cadastrados = Candidatoinformacoes.objects.all()
    context = {
        'form': form,
        'titulo': 'Informações do Candidato',
        'candidatos_cadastrados': candidatos_cadastrados
    }
    return render(request, 'cadastros_mdb/cadastros_mdb.html', context)


def informacoes_caoguia(request):
    caes_cadastrados_mdb = Caoinformacoes.objects.all()

    if request.method == 'POST':
        form = CaoinformacoesForm(request.POST)
        if form.is_valid():
            # Obtém o objeto CaoGuia selecionado do formulário
            cao_selecionado = form.cleaned_data['cao']
            
            # Cria a instância de Caoinformacoes, mas não salva ainda
            nova_info_cao = form.save(commit=False)
            
            # Atribui o ID, altura, peso e sexo do objeto relacional
            nova_info_cao.id_cao = cao_selecionado.id_cao
            nova_info_cao.altura = cao_selecionado.tamanho
            nova_info_cao.peso = cao_selecionado.peso_cao
            nova_info_cao.sexo = cao_selecionado.sexo
            
            # Salva a nova instância no MongoDB
            nova_info_cao.save()

            return redirect('informacoes_caoguia')
    else:
        form = CaoinformacoesForm()
    
    context = {
        'form': form,
        'titulo': 'Informações do Cão-Guia',
        'caes_cadastrados_mdb': caes_cadastrados_mdb,
    }
    return render(request, 'cadastros_mdb/cadastros_mdb.html', context)


def informacoes_cadastro(request):
    return render(request, 'cadastros_mdb/botoes.html', {'titulo': 'Informações de Cão-Guia e Candidato'})

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
        diferenca_altura = abs(candidato.altura - cao.altura)
        pontuacao_altura = max(0, 10 - diferenca_altura * 5) # O '5' é um fator de penalidade ajustável
        pontuacao_total += pontuacao_altura * pesos["altura"]

        # Pontuação do Peso
        # Mesma lógica da altura
        diferenca_peso = abs(candidato.peso - cao.peso)
        pontuacao_peso = max(0, 10 - diferenca_peso * 0.5) # O '0.5' é um fator de penalidade ajustável
        pontuacao_total += pontuacao_peso * pesos["peso"]

        # Pontuação da Velocidade
        # Critério categórico, com pontuação exata por nível de compatibilidade
        if candidato.velocidade_caminhada == cao.velocidade_caminhada:
            pontuacao_velocidade = 10
        elif (candidato.velocidade_caminhada == "alta" and cao.velocidade_caminhada == "moderada") or \
            (candidato.velocidade_caminhada == "baixa" and cao.velocidade_caminhada == "moderada"):
            pontuacao_velocidade = 5
        else:
            pontuacao_velocidade = 0
        pontuacao_total += pontuacao_velocidade * pesos["velocidade_caminhada"]
        
        # Pontuação do Sexo
        # Critério categórico
        if candidato.sexo_desejado_cao == "indiferente" or \
        candidato.sexo_desejado_cao == cao.sexo:
            pontuacao_sexo = 10
        else:
            pontuacao_sexo = 0
        pontuacao_total += pontuacao_sexo * pesos["sexo"]
        
        # Armazenar o resultado
        resultados_pareamento.append({
            "nome_cao": cao.nome,
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

    return render(request, 'cadastros_mdb/pareamento.html', context)