from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .forms import SelecaoPareamentoForm
from datetime import date

def compatibilidade_numerica(v1, v2, tolerancia):
    """
    Calcula score baseado na diferença numérica linear.
    Quanto menor a diferença, maior o score.
    """
    if v1 is None or v2 is None:
        return 0
    diff = abs(v1 - v2)
    score = 1 - (diff / tolerancia)
    return max(0, score)

def compatibilidade_ordinal(v1, v2, max_val=5):
    """
    Calcula score para escalas de 1 a 5 (ou outro max_val).
    Converte strings para int antes de calcular.
    """
    try:
        val1 = int(v1) if v1 else 0
        val2 = int(v2) if v2 else 0
    except ValueError:
        return 0
    
    return 1 - (abs(val1 - val2) / max_val)

def compatibilidade_binaria(v1, target):
    """
    Retorna 1 se v1 for igual ao target, senão 0.
    Útil para 'Sim' (1) ou 'Não' (0).
    """
    try:
        val1 = int(v1) if v1 else 0
    except ValueError:
        return 0
    
    return 1 if val1 == target else 0

# CÁLCULO DO SCORE TOTAL 
def calcular_compatibilidade(candidato, caes_disponiveis):
    resultados = []
    
    # DEFINIÇÃO DOS PESOS
    PESOS = {
        "altura": 3.0,
        "peso": 2.0,
        "velocidade": 2.5,
        "ambiente": 2.0,
        "experiencia": 1.0,
        "sociabilidade": 1.5
    }

    for cao in caes_disponiveis:
        score = 0
        
        # 1. Altura (Tolerância: 20cm)
        # O modelo está em CM? Se sim, 20 é ok. Se estiver em Metros, use 0.20.
        # Assumindo CM conforme o verbose_name do seu model.
        score += PESOS["altura"] * compatibilidade_numerica(
            candidato.altura, cao.altura, tolerancia=20
        )

        # 2. Peso (Tolerância: 15kg)
        score += PESOS["peso"] * compatibilidade_numerica(
            candidato.peso_candidato, cao.peso_cao, tolerancia=15
        )

        # 3. Velocidade (Escala 1 a 5)
        score += PESOS["velocidade"] * compatibilidade_ordinal(
            candidato.velocidade_caminhada, cao.velocidade_caminhada
        )

        # 4. Ambiente (Escala 1 a 5)
        # Compara Ambiente Moradia do Candidato vs Ambiente Preferencial do Cão
        score += PESOS["ambiente"] * compatibilidade_ordinal(
            candidato.ambiente_moradia, cao.ambiente_preferencial
        )

        # 5. Experiência (Binária)
        # Verifica se o candidato marcou '1' (Sim) na experiência
        score += PESOS["experiencia"] * compatibilidade_binaria(
            candidato.experiencia_com_caes, 1
        )

        # 6. Sociabilidade (Comparado ao ideal 5)
        # Quanto mais próximo de 5 a sociabilidade do cão, melhor
        score += PESOS["sociabilidade"] * compatibilidade_ordinal(
            5, cao.sociabilidade
        )

        resultados.append({
            'cao': cao,
            'pontuacao': round(score, 2)
        })

    # Ordena do maior score para o menor
    resultados.sort(key=lambda x: x['pontuacao'], reverse=True)
    return resultados


# VIEWS DO DJANGO


def selecionar_pareamento(request):
    if request.method == 'POST':
        form = SelecaoPareamentoForm(request.POST)
        if form.is_valid():
            candidato = form.cleaned_data['candidato']
            return redirect('resultado_pareamento', cpf=candidato.id_candidato)
    else:
        form = SelecaoPareamentoForm()
    
    return render(request, 'pareamento/selecao.html', {'form': form, 'titulo': 'Iniciar Pareamento'})

def resultado_pareamento(request, cpf):
    candidato = get_object_or_404(Candidato, pk=cpf)
    
    # Filtra cães que NÃO estão em uma dupla ativa
    caes_indisponiveis = FormacaoDupla.objects.filter(data_fim__isnull=True).values_list('cao_id', flat=True)
    caes_disponiveis = CaoGuia.objects.exclude(id_cao__in=caes_indisponiveis)
    
    # Chama a função de cálculo atualizada
    match_list = calcular_compatibilidade(candidato, caes_disponiveis)
    
    # Opcional: Pegar apenas o TOP 5 como no seu exemplo SQL
    # match_list = match_list[:5] 
    
    return render(request, 'pareamento/resultado.html', {
        'candidato': candidato,
        'match_list': match_list,
        'titulo': f'Compatibilidade para {candidato.nome_candidato}'
    })

def confirmar_pareamento(request, cpf, id_cao):
    candidato = get_object_or_404(Candidato, pk=cpf)
    cao = get_object_or_404(CaoGuia, pk=id_cao)
    
    if request.method == 'POST':
        # Cria a dupla no banco de dados
        FormacaoDupla.objects.create(
            Candidato=candidato,
            cao=cao,
            data_inicio=date.today()
        )
        messages.success(request, f'Dupla formada com sucesso: {candidato.nome_candidato} e {cao.nome_cao}!')
        return redirect('home')
    
    return redirect('resultado_pareamento', cpf=cpf)