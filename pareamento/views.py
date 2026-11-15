from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .models import Matching
from .forms import SelecaoPareamentoForm
from datetime import date

def definir_peso_ideal_cao(peso_candidato):
    """
    Define o peso ideal do cão baseado no peso do candidato.
    """
    if peso_candidato is None:
        return 32 # Peso médio padrão de um Labrador/Golden
        
    if peso_candidato <= 60: 
        # Pessoa Leve (até 60kg) -> Cão mais compacto
        return 27  # kg
        
    elif 60 < peso_candidato <= 85:
        # Pessoa Média -> Cão Padrão
        return 32  # kg
        
    else:
        # Pessoa Pesada (> 85kg) -> Cão Robusto
        return 38  
    
def definir_altura_ideal_cao(altura_candidato):
    """
    Define a altura ideal do cão baseada na estatura do candidato.
    """
    if altura_candidato is None:
        return 50 # Retorna um tamanho médio padrão se não tiver dados
        
    if altura_candidato <= 165: 
        return 35 
    elif 165 < altura_candidato <= 180:
        # Pessoa Média -> Cão Médio
        return 55
    else:
        # Pessoa Alta -> Cão Grande
        return 65
    
# FUNÇÕES DE CÁLCULO 
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

# ALGORITMO PRINCIPAL 
def calcular_e_salvar_compatibilidade(candidato, caes_disponiveis):
    # Limpa matchings anteriores
    Matching.objects.filter(candidato=candidato).delete()
    
    PESOS = {
        "altura": 3.0, "peso": 2.0, "velocidade": 2.5,
        "ambiente": 2.0, "experiencia": 1.0, "sociabilidade": 1.5
    }

    for cao in caes_disponiveis:
        score = 0
        #score de altura
        altura_ideal = definir_altura_ideal_cao(candidato.altura)
        score_altura = PESOS["altura"] * compatibilidade_numerica(altura_ideal, cao.altura, 15)
        score += score_altura
        #score de peso
        peso_ideal = definir_peso_ideal_cao(candidato.peso_candidato)
        score_peso = PESOS["peso"] * compatibilidade_numerica(peso_ideal, cao.peso_cao, 8)
        score += score_peso
        #score de ambiente
        def verificar_ambiente(cand_amb, cao_amb):
            # Converte para string para facilitar a comparação visual
            cand = str(cand_amb)
            cao = str(cao_amb)
            
            # Se for igual, perfeito (100%)
            if cand == cao:
                return 1.0
                
            # Combinações aceitáveis (50% da nota)
            pares_aceitaveis = [
                ('1', '4'), # Rural e Calmo
                ('4', '1'),
                ('2', '3'), # Urbano e Barulhento (talvez o cão tolere)
                ('1', '5'), # Rural e Animais
            ]
            
            if (cand, cao) in pares_aceitaveis:
                return 0.5
                
            # Qualquer outra coisa é 0
            return 0.0
        #score de ambiente
        score += PESOS["ambiente"] * verificar_ambiente(candidato.ambiente_moradia, cao.ambiente_preferencial)
        #score de experiencia
        score += PESOS["experiencia"] * compatibilidade_binaria(candidato.experiencia_com_caes, 1)
        #score de sociabilidade
        score += PESOS["sociabilidade"] * compatibilidade_ordinal(5, cao.sociabilidade)

        # Cria e Salva um por um
        Matching.objects.create(
            candidato=candidato,
            cao=cao,
            score_total=round(score, 2)
        )


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
    

    ids_indisponiveis = list(FormacaoDupla.objects.filter(data_fim__isnull=True).values_list('cao_id', flat=True))
    

    if ids_indisponiveis:
        caes_disponiveis = CaoGuia.objects.exclude(id_cao__in=ids_indisponiveis)
    else:
        # Se a lista estiver vazia, pegamos todos
        caes_disponiveis = CaoGuia.objects.all()
    
    # Calcula e Salva
    calcular_e_salvar_compatibilidade(candidato, caes_disponiveis)
    
    # Busca resultados
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
        )
        messages.success(request, 'Dupla formada com sucesso!')
        return redirect('home')
    
    return redirect('resultado_pareamento', cpf=cpf)
