from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla # Importando do app cadastros
from .forms import SelecaoPareamentoForm
from datetime import date

# --- LÓGICA DO ALGORITMO ---
def calcular_compatibilidade(candidato, caes_disponiveis):
    resultados = []
    
    # Pesos
    P_ALTURA = 0.35
    P_PESO = 0.25
    P_VELOCIDADE = 0.30
    P_SEXO = 0.10

    for cao in caes_disponiveis:
        pontuacao = 0
        
        # 1. Altura (Comparando Altura do Candidato vs Tamanho do Cão)
        if candidato.altura and cao.tamanho:
            diff_altura = abs(candidato.altura - cao.tamanho)
            # Exemplo de lógica: quanto menor a diferença, mais pontos
            score_altura = max(0, 10 - (diff_altura * 10)) 
            pontuacao += score_altura * P_ALTURA

        # 2. Peso
        if candidato.peso_candidato and cao.peso_cao:
            diff_peso = abs(candidato.peso_candidato - cao.peso_cao)
            score_peso = max(0, 10 - (diff_peso * 0.2))
            pontuacao += score_peso * P_PESO

        # 3. Velocidade
        score_vel = 0
        if candidato.velocidade_caminhada == cao.velocidade_caminhada:
            score_vel = 10
        elif (candidato.velocidade_caminhada == 'alta' and cao.velocidade_caminhada == 'moderada') or \
            (candidato.velocidade_caminhada == 'baixa' and cao.velocidade_caminhada == 'moderada') or \
            (candidato.velocidade_caminhada == 'moderada'):
            score_vel = 5
        pontuacao += score_vel * P_VELOCIDADE

        # 4. Sexo
        score_sexo = 0
        if candidato.sexo_desejado_cao == 'indiferente':
            score_sexo = 10
        elif candidato.sexo_desejado_cao == cao.sexo:
            score_sexo = 10
        pontuacao += score_sexo * P_SEXO

        resultados.append({
            'cao': cao,
            'pontuacao': round(pontuacao, 2)
        })

    resultados.sort(key=lambda x: x['pontuacao'], reverse=True)
    return resultados

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
    
    # Filtra cães que NÃO estão em dupla ativa (data_fim é null)
    caes_indisponiveis = FormacaoDupla.objects.filter(data_fim__isnull=True).values_list('cao_id', flat=True)
    caes_disponiveis = CaoGuia.objects.exclude(id_cao__in=caes_indisponiveis)
    
    match_list = calcular_compatibilidade(candidato, caes_disponiveis)
    
    return render(request, 'pareamento/resultado.html', {
        'candidato': candidato,
        'match_list': match_list,
        'titulo': f'Compatibilidade para {candidato.nome_candidato}'
    })

def confirmar_pareamento(request, cpf, id_cao):
    candidato = get_object_or_404(Candidato, pk=cpf)
    cao = get_object_or_404(CaoGuia, pk=id_cao)
    
    if request.method == 'POST':
        FormacaoDupla.objects.create(
            usuario=candidato,
            cao=cao,
            data_inicio=date.today()
        )
        messages.success(request, f'Dupla formada com sucesso: {candidato.nome_candidato} e {cao.nome_cao}!')
        return redirect('home') # Redireciona para a home (que está no outro app, mas o Django acha pelo nome)
    
    return redirect('resultado_pareamento', cpf=cpf)
