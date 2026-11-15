from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .models import Matching
from .forms import SelecaoPareamentoForm
from datetime import date   

def calcular_indice_compatibilidade(cao, candidato):
    # Definindo os pesos para o cálculo (índice tecnicamente justificável)
    PESO_ALTO = 20    # Variáveis fundamentais
    PESO_MEDIO = 10   # Variáveis importantes, mas secundárias
    PESO_BAIXO = 5    # Variáveis de ajuste fino (nome, raça, sexo têm peso 0 ou 1 no seu sistema)
    
    score_total = 0
    score_maximo_possivel = (PESO_ALTO * 5) + (PESO_MEDIO * 5) # Total base para gerar uma porcentagem

    # =====================================================================
    # BLOCO 1: VARIÁVEIS DE ALTO PESO (Fundamentais para o sucesso)
    # =====================================================================

    # 1. Velocidade cão ↔ velocidade usuário
    if cao.velocidade == candidato.velocidade_caminhada:
        score_total += PESO_ALTO

    # 2. Exigência de condução cão ↔ capacidade de condução do usuário
    if cao.exigencia_conducao == candidato.capacidade_conducao:
        score_total += PESO_ALTO
    elif cao.exigencia_conducao == 'Alta' and candidato.capacidade_conducao == 'Média':
        # Penalidade forte: Cão exige muito, mas usuário tem capacidade média
        score_total -= (PESO_ALTO / 2)

    # 3. Complexidade de trabalho cão ↔ complexidade da rotina
    if cao.complexidade_trabalho == candidato.complexidade_rotina:
        score_total += PESO_ALTO
    elif cao.complexidade_trabalho == 'Alta' and candidato.complexidade_rotina == 'Média':
        # Cão superqualificado para rotina média (ok, mas sem bônus máximo)
        score_total += (PESO_ALTO / 2)

    # 4. Concentração cão ↔ nível de distração dos trajetos
    if cao.concentracao == 'Alta' and candidato.nivel_distracao_trajetos == 'Alto':
        score_total += PESO_ALTO
    elif cao.concentracao == 'Alta' and candidato.nivel_distracao_trajetos in ['Médio', 'Baixo']:
        score_total += PESO_ALTO * 0.8  # Cão muito concentrado em rotina calma é ótimo
    elif cao.concentracao == 'Média' and candidato.nivel_distracao_trajetos in ['Médio', 'Baixo']:
        score_total += PESO_ALTO
    elif cao.concentracao == 'Baixa' and candidato.nivel_distracao_trajetos == 'Alto':
        # Penalidade: Cão distrai fácil em rota complexa = perigoso
        score_total -= PESO_ALTO

    # 5. Adequação Física: Altura e Peso ↔ características físicas do usuário
    margem_altura = 15 # ex: diferença máxima de 15cm considerada ideal
    margem_peso = 20   # ex: diferença de proporção de peso
    adequacao_fisica = 0
    if abs(cao.altura - candidato.altura) <= margem_altura:
        adequacao_fisica += (PESO_ALTO / 2)
    if abs(cao.peso - candidato.peso) <= margem_peso:
        adequacao_fisica += (PESO_ALTO / 2)
    score_total += adequacao_fisica


    # =====================================================================
    # BLOCO 2: VARIÁVEIS DE MÉDIO PESO (Comportamento e Rotina Diária)
    # =====================================================================

    # 6. Energia cão ↔ nível de atividade do usuário
    if cao.nivel_energia == candidato.nivel_atividade:
        score_total += PESO_MEDIO
    
    # 7. Sociabilidade/convívio cão ↔ presença de pessoas/animais na rotina
    if cao.sociabilidade == candidato.presenca_pessoas_animais:
        score_total += PESO_MEDIO

    # 8. Temperamento cão ↔ características ambientais da rotina
    # Ex: Cão calmo vai bem em ambientes movimentados ou tranquilos; cão agitado precisa de vazão
    if cao.temperamento == 'Calmo' and candidato.caracteristicas_ambientais == 'Movimentado':
        score_total += PESO_MEDIO
    elif cao.temperamento == candidato.caracteristicas_ambientais: # Lógica simplificada de match
        score_total += PESO_MEDIO

    # 9. Experiência do usuário ↔ necessidade de manejo do cão
    # Cães que precisam de muito manejo devem ir para usuários experientes
    if cao.necessidade_manejo == 'Alta' and candidato.experiencia_cao_guia == 'Experiente':
        score_total += PESO_MEDIO
    elif cao.necessidade_manejo == 'Baixa':
        # Cão fácil de manejar atende a qualquer usuário
        score_total += PESO_MEDIO
    elif cao.necessidade_manejo == 'Alta' and candidato.experiencia_cao_guia in ['Nenhuma', 'Iniciante']:
        # Penalidade de manejo
        score_total -= PESO_MEDIO

    # 10. Presença de outros animais (Convívio direto)
    # Se o candidato tem animais, o cão TEM que ter bom histórico de convívio
    if candidato.presenca_pessoas_animais == 'Alta' and cao.sociabilidade == 'Alta':
        score_total += PESO_MEDIO


    # =====================================================================
    # CÁLCULO FINAL: GERANDO O ÍNDICE (%)
    # =====================================================================
    
    # Previne scores negativos caso o candidato seja totalmente incompatível
    if score_total < 0:
        score_total = 0
        
    # Calcula a porcentagem de compatibilidade
    indice_compatibilidade = (score_total / score_maximo_possivel) * 100
    
    # Limita a 100% no máximo
    if indice_compatibilidade > 100:
        indice_compatibilidade = 100

    return {
        'score_absoluto': score_total,
        'percentual': round(indice_compatibilidade, 2),
        'recomendado': indice_compatibilidade >= 70 # Define uma linha de corte (ex: 70%)
    }