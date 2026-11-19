from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cadastros.models import Candidato, CaoGuia, FormacaoDupla
from .models import Matching
from .forms import SelecaoPareamentoForm
from datetime import date   

MAPA_NIVEL = {
    'Baixa': 1, 'Baixo': 1, 'Lenta': 1, 'Nenhuma': 1, 'Tranquilo': 1, 'Calmo': 1,
    'Simples/Retilíneos': 1,
    'Média': 2, 'Médio': 2, 'Iniciante': 2, 'Moderado': 2, 'Equilibrado': 2,
    'Mistos/Moderados': 2,
    'Alta': 3, 'Alto': 3, 'Rápida': 3, 'Experiente': 3, 'Movimentado': 3, 'Agitado': 3,
    'Complexos/Transporte Público': 3,
}

def nivel_num(valor, padrao=2):
    return MAPA_NIVEL.get(valor, padrao)

def normalizar_altura_cm(altura):
    if not altura:
        return None
    return altura * 100 if altura < 3.0 else altura

def calcular_indice_compatibilidade(cao, candidato):
    PESO_ALTO = 20.0   # 5 critérios fundamentais = 100 pts
    PESO_MEDIO = 10.0  # 5 critérios complementares = 50 pts
    score_total = 0.0
    score_maximo_possivel = (PESO_ALTO * 5) + (PESO_MEDIO * 5)  # 150 pts

    # 1. Velocidade cão ↔ velocidade usuário (20 pts)
    diff_vel = abs(nivel_num(cao.velocidade) - nivel_num(candidato.velocidade_caminhada))
    if diff_vel == 0:
        score_total += PESO_ALTO
    elif diff_vel == 1:
        score_total += PESO_ALTO * 0.5

    # 2. Exigência de condução cão ↔ capacidade de condução do usuário (20 pts)
    exig_cao = nivel_num(cao.exigencia_conducao)
    cap_cand = nivel_num(candidato.capacidade_conducao)
    if cap_cand >= exig_cao:
        score_total += PESO_ALTO if cap_cand == exig_cao else PESO_ALTO * 0.85
    elif exig_cao - cap_cand == 1:
        score_total += PESO_ALTO * 0.25
    else:
        score_total -= PESO_ALTO * 0.5

    # 3. Complexidade de trabalho cão ↔ complexidade da rotina e trajetos (20 pts)
    comp_cao = nivel_num(cao.complexidade_trabalho)
    comp_rotina = nivel_num(candidato.complexidade_rotina)
    comp_trajeto = nivel_num(getattr(candidato, 'caracteristicas_trajetos', None), comp_rotina)
    demanda_rotina = max(comp_rotina, comp_trajeto)
    if comp_cao == demanda_rotina:
        score_total += PESO_ALTO
    elif comp_cao > demanda_rotina:
        score_total += PESO_ALTO * 0.8
    elif demanda_rotina - comp_cao == 1:
        score_total += PESO_ALTO * 0.5

    # 4. Concentração/distração do cão ↔ nível de distração dos trajetos (20 pts)
    conc_cao = nivel_num(cao.concentracao)
    dist_cao = nivel_num(getattr(cao, 'nivel_distracao', None), 4 - conc_cao)
    est_trajeto = nivel_num(candidato.nivel_distracao_trajetos)
    foco_cao = (conc_cao + (4 - dist_cao)) / 2.0
    if foco_cao >= est_trajeto:
        score_total += PESO_ALTO
    elif est_trajeto - foco_cao <= 1.0:
        score_total += PESO_ALTO * 0.5
    else:
        score_total -= PESO_ALTO * 0.5

    # 5. Adequação Física: Altura (10 pts) e Peso (10 pts)
    alt_cao = normalizar_altura_cm(cao.altura)
    alt_cand = normalizar_altura_cm(candidato.altura)
    if alt_cao and alt_cand:
        altura_cao_ideal = alt_cand * 0.35  # Ex: 170cm * 0.35 = 59.5cm na cernelha
        diff_alt = abs(alt_cao - altura_cao_ideal)
        if diff_alt <= 5:
            score_total += (PESO_ALTO / 2)
        elif diff_alt <= 10:
            score_total += (PESO_ALTO / 2) * 0.6

    if cao.peso and candidato.peso and candidato.peso > 0:
        proporcao_peso = cao.peso / candidato.peso  # Ideal: cão entre 25% e 50% do peso do usuário
        if 0.25 <= proporcao_peso <= 0.50:
            score_total += (PESO_ALTO / 2)
        elif 0.20 <= proporcao_peso <= 0.60:
            score_total += (PESO_ALTO / 2) * 0.5

    # 6. Energia cão ↔ nível de atividade do usuário (10 pts)
    diff_en = abs(nivel_num(cao.nivel_energia) - nivel_num(candidato.nivel_atividade))
    if diff_en == 0:
        score_total += PESO_MEDIO
    elif diff_en == 1:
        score_total += PESO_MEDIO * 0.5

    # 7. Sociabilidade/convívio cão ↔ presença de pessoas/animais na rotina (10 pts)
    soc_cao = nivel_num(cao.sociabilidade)
    conv_animais = nivel_num(getattr(cao, 'convivio_animais', None), soc_cao)
    pres_cand = nivel_num(candidato.presenca_pessoas_animais)
    media_social_cao = (soc_cao + conv_animais) / 2.0
    if media_social_cao >= pres_cand:
        score_total += PESO_MEDIO
    elif pres_cand - media_social_cao <= 1.0:
        score_total += PESO_MEDIO * 0.5

    # 8. Temperamento cão ↔ características ambientais da rotina (10 pts)
    if cao.temperamento in ['Calmo', 'Equilibrado']:
        score_total += PESO_MEDIO
    elif cao.temperamento == 'Agitado' and candidato.caracteristicas_ambientais == 'Tranquilo':
        score_total += PESO_MEDIO * 0.7

    # 9. Experiência do usuário ↔ necessidade de manejo do cão (10 pts)
    man_cao = nivel_num(cao.necessidade_manejo)
    exp_cand = nivel_num(candidato.experiencia_cao_guia)
    if man_cao == 1 or exp_cand >= man_cao:
        score_total += PESO_MEDIO
    elif man_cao - exp_cand == 1:
        score_total += PESO_MEDIO * 0.5

    # 10. Adequação ao ambiente de moradia (10 pts)
    if candidato.tipo_moradia in ['apartamento_escada', 'apartamento_elevador', 'casa_sem_quintal']:
        if cao.nivel_energia in ['Baixo', 'Médio'] and cao.temperamento in ['Calmo', 'Equilibrado']:
            score_total += PESO_MEDIO
        elif cao.nivel_energia in ['Baixo', 'Médio'] or cao.temperamento in ['Calmo', 'Equilibrado']:
            score_total += PESO_MEDIO * 0.5
    else:
        score_total += PESO_MEDIO

    score_total = max(0.0, min(score_total, score_maximo_possivel))
    indice_compatibilidade = round((score_total / score_maximo_possivel) * 100, 2)

    return {
        'score_absoluto': round(score_total, 1),
        'percentual': indice_compatibilidade,
        'recomendado': indice_compatibilidade >= 70
    }


def selecionar_pareamento(request):
    if request.method == 'POST':
        form = SelecaoPareamentoForm(request.POST)
        if form.is_valid():
            # Obtém o candidato selecionado no formulário (ou CPF digitado)
            candidato = form.cleaned_data.get('candidato') or form.cleaned_data.get('cpf')
            cpf = candidato.id_candidato if hasattr(candidato, 'id_candidato') else candidato
            return redirect('resultado_pareamento', cpf=cpf)
    else:
        form = SelecaoPareamentoForm()

    return render(request, 'pareamento/selecao_pareamento.html', {'form': form})

def resultado_pareamento(request, cpf):
    candidato = get_object_or_404(Candidato, id_candidato=cpf)
    caes = CaoGuia.objects.all()

    match_list = []
    for cao in caes:
        dados_compatibilidade = calcular_indice_compatibilidade(cao, candidato)
        match_list.append({
            'cao': cao,
            'score_total': dados_compatibilidade['percentual'],
            'score_absoluto': dados_compatibilidade['score_absoluto'],
            'percentual': dados_compatibilidade['percentual'],
            'recomendado': dados_compatibilidade['recomendado'],
        })

    # Ordena os cães do maior percentual de compatibilidade para o menor
    match_list.sort(key=lambda x: x['score_total'], reverse=True)

    context = {
        'titulo': 'Resultado do Pareamento',
        'candidato': candidato,
        'match_list': match_list,
    }
    return render(request, 'pareamento/resultado_pareamento.html', context)

def confirmar_pareamento(request, cpf, id_cao):
    candidato = get_object_or_404(Candidato, id_candidato=cpf)
    cao = get_object_or_404(CaoGuia, pk=id_cao)

    # Registra a formação da dupla
    FormacaoDupla.objects.create(
        cao=cao,
        Candidato=candidato,
        data_inicio=date.today()
    )

    messages.success(request, f"Pareamento entre {candidato.nome_candidato} e {cao.nome_cao} confirmado com sucesso!")
    return redirect('selecionar_pareamento')