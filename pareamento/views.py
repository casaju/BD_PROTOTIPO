
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .models import Matching
from .forms import SelecaoPareamentoForm
from datetime import date

# --- Funções Auxiliares ---
def compatibilidade_numerica(v1, v2, tolerancia):
    if v1 is None or v2 is None: return 0
    diff = abs(v1 - v2)
    return max(0, 1 - (diff / tolerancia))

def compatibilidade_ordinal(v1, v2, max_val=5):
    try:
        val1 = int(v1) if v1 else 0
        val2 = int(v2) if v2 else 0
    except ValueError: return 0
    return 1 - (abs(val1 - val2) / max_val)

def compatibilidade_binaria(v1, target):
    try: val1 = int(v1) if v1 else 0
    except ValueError: return 0
    return 1 if val1 == target else 0

# --- Lógica de Cálculo e Salvamento ---
def calcular_e_salvar_compatibilidade(candidato, caes_disponiveis):
    # Opcional: Limpar histórico anterior deste candidato para não duplicar
    Matching.objects.filter(candidato=candidato).delete()

    matches_to_create = []
    
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
        
        # Critérios
        score += PESOS["altura"] * compatibilidade_numerica(candidato.altura, cao.altura, 20)
        score += PESOS["peso"] * compatibilidade_numerica(candidato.peso_candidato, cao.peso_cao, 15)
        score += PESOS["velocidade"] * compatibilidade_ordinal(candidato.velocidade_caminhada, cao.velocidade_caminhada)
        score += PESOS["ambiente"] * compatibilidade_ordinal(candidato.ambiente_moradia, cao.ambiente_preferencial)
        score += PESOS["experiencia"] * compatibilidade_binaria(candidato.experiencia_com_caes, 1)
        score += PESOS["sociabilidade"] * compatibilidade_ordinal(5, cao.sociabilidade)

        matches_to_create.append(Matching(
            candidato=candidato,
            cao=cao,
            score_total=round(score, 2)
        ))

    # Salva tudo de uma vez
    Matching.objects.bulk_create(matches_to_create)

# --- Views ---
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
    
    # Filtra cães que NÃO estão em dupla ativa (campo data_fim é null)
    caes_indisponiveis = FormacaoDupla.objects.filter(data_fim__isnull=True).values_list('cao_id', flat=True)
    caes_disponiveis = CaoGuia.objects.exclude(id_cao__in=caes_indisponiveis)
    
    # Calcula e salva
    calcular_e_salvar_compatibilidade(candidato, caes_disponiveis)
    
    # Busca do banco ordenado pelo score
    match_list = Matching.objects.filter(candidato=candidato).order_by('-score_total')
    
    return render(request, 'pareamento/resultado_pareamento.html', {
        'candidato': candidato,
        'match_list': match_list,
        'titulo': f'Compatibilidade para {candidato.nome_candidato}'
    })

def confirmar_pareamento(request, cpf, id_cao):
    candidato = get_object_or_404(Candidato, pk=cpf)
    cao = get_object_or_404(CaoGuia, pk=id_cao)
    
    if request.method == 'POST':
        FormacaoDupla.objects.create(
            Candidato=candidato,
            cao=cao,
            data_inicio=date.today()
            # data_fim fica vazio, indicando dupla ativa
        )
        messages.success(request, f'Dupla formada com sucesso!')
        return redirect('home')
    
    return redirect('resultado_pareamento', cpf=cpf)
