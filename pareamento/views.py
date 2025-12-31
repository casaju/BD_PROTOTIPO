from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .models import Matching  # <--- Importe o novo modelo aqui
from .forms import SelecaoPareamentoForm
from datetime import date

# ... (Mantenha as funções auxiliares: compatibilidade_numerica, ordinal, etc.) ...

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

# --- LÓGICA DO ALGORITMO ---

def calcular_e_salvar_compatibilidade(candidato, caes_disponiveis):
    # 1. Limpar matchings anteriores deste candidato para não duplicar (Opcional, mas recomendado)
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
        
        score += PESOS["altura"] * compatibilidade_numerica(candidato.altura, cao.altura, 20)
        score += PESOS["peso"] * compatibilidade_numerica(candidato.peso_candidato, cao.peso_cao, 15)
        score += PESOS["velocidade"] * compatibilidade_ordinal(candidato.velocidade_caminhada, cao.velocidade_caminhada)
        score += PESOS["ambiente"] * compatibilidade_ordinal(candidato.ambiente_moradia, cao.ambiente_preferencial)
        score += PESOS["experiencia"] * compatibilidade_binaria(candidato.experiencia_com_caes, 1)
        score += PESOS["sociabilidade"] * compatibilidade_ordinal(5, cao.sociabilidade)

        # Arredonda score final
        score_final = round(score, 2)

        # Cria o objeto Matching na memória (sem salvar ainda)
        matches_to_create.append(Matching(
            candidato=candidato,
            cao=cao,
            score_total=score_final
        ))

    # 2. Salva todos de uma vez no banco (Bulk Create)
    Matching.objects.bulk_create(matches_to_create)

# --- VIEWS ---

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
    
    # Filtra cães disponíveis
    caes_indisponiveis = FormacaoDupla.objects.filter(data_fim__isnull=True).values_list('cao_id', flat=True)
    caes_disponiveis = CaoGuia.objects.exclude(id_cao__in=caes_indisponiveis)
    
    # 1. Executa o cálculo e SALVA no banco
    calcular_e_salvar_compatibilidade(candidato, caes_disponiveis)
    
    # 2. Busca os resultados DO BANCO (Tabela Matching), ordenados pelo score
    match_list = Matching.objects.filter(candidato=candidato).order_by('-score_total')
    
    # (Opcional) Limitar ao Top 5
    # match_list = match_list[:5]

    # Ajuste para o template: O template espera um objeto com .cao e .pontuacao
    # O modelo Matching tem .cao e .score_total. 
    # Podemos passar a lista de objetos Matching direto, mas precisaremos ajustar o template.
    
    return render(request, 'pareamento/resultado.html', {
        'candidato': candidato,
        'match_list': match_list, # Agora enviamos objetos 'Matching'
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
        )
        messages.success(request, f'Dupla formada com sucesso!')
        return redirect('home')
    
    return redirect('resultado_pareamento', cpf=cpf)