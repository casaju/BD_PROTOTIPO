from django.shortcuts import render, redirect
from .forms import CandidatoForm, UsuarioForm, CaoGuiaForm

def cadastrar_candidato(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_candidato')
    else:
        form = CandidatoForm()
    return render(request, 'cadastros/form.html', {'form': form})

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_usuario')
    else:
        form = UsuarioForm()
    return render(request, 'cadastros/form.html', {'form': form})


def cadastrar_caoguia(request):
    if request.method == 'POST':
        form = CaoGuiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_caoguia')
    else:
        form = CaoGuiaForm()
    return render(request, 'cadastros/form.html', {'form': form})