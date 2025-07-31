from django.shortcuts import render, redirect
from .forms import CandidatoForm, UsuarioForm, CaoGuiaForm, FormacaoDuplaForm

def cadastrar_candidato(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_candidato')
    else:
        form = CandidatoForm()
    return render(request, 'cadastros/form.html', {'form': form, 'titulo': 'Cadastrar candidato'})

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            print("Dados salvos com sucesso!")
            return redirect('cadastrar_usuario')
        else:
            print("O formulário NÃO é válido. Erros:", form.errors)
    else:
        form= UsuarioForm
    return render(request, 'cadastro.html', {'form': form, 'titulo': 'Cadastrar Usuario'})


def cadastrar_caoguia(request):
    if request.method == 'POST':
        form = CaoGuiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_caoguia')
    else:
        form = CaoGuiaForm()
    return render(request, 'cadastro.html', {'form': form, 'titulo': 'Cadastrar Cão-guia'})

def cadastrar_formacao(request):
    form = FormacaoDuplaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastrar_formacao')
    return render(request, 'cadastro.html', {'form': form, 'titulo': 'Formar Dupla'})
