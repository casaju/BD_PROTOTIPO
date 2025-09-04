from django.shortcuts import render, redirect
from .forms import testeForm

def informacoes_candidato(request):
    if request.method == 'POST':
        form = testeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('informacoes_candidato')
    else:
        form = testeForm()
    return render(request, 'cadastros_mdb/cadastros_mdb.html', {'form': form, 'titulo': 'Cadastrar candidato'})



def informacoes_caoguia(request):
    contexto = {
        'text': 'Olá 😊, Você está na página de informações do Cao Guia.'
    }
    return render(request, 'cadastros_mdb/cadastros_mdb.html', contexto)

def informacoes_cadastro(request):
    return render(request, 'cadastros_mdb/botoes.html',)

