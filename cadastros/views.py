from django.shortcuts import render, redirect
from .forms import CandidatoForm, UsuarioForm, CaoGuiaForm, FormacaoDuplaForm,  LoginForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm


def cadastrar_candidato(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_candidato')
    else:
        form = CandidatoForm()
    return render(request, 'cadastros/cadastro.html', {'form': form, 'titulo': 'Cadastrar candidato'})

def cadastrar_usuario(request): 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crie seu modelo de usuário vinculado ao user do Django
            Usuario.objects.create(nome_usuario=user.username, user=user)
            print("Dados salvos com sucesso!")
            return redirect('cadastrar_usuario')
        else:
            print("O formulário NÃO é válido. Erros:", form.errors)
    else:
        form= UserCreationForm
    return render(request, 'cadastros/cadastro.html', {'form': form, 'titulo': 'Cadastrar Usuario'})



def cadastrar_caoguia(request):
    if request.method == 'POST':
        form = CaoGuiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_caoguia')
    else:
        form = CaoGuiaForm()
    return render(request, 'cadastros/cadastro.html', {'form': form, 'titulo': 'Cadastrar Cão-guia'})

def cadastrar_formacao(request):
    form = FormacaoDuplaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cadastrar_formacao')
    return render(request, 'cadastros/cadastro.html', {'form': form, 'titulo': 'Formar Dupla'})

def cadastro_inicio(request):
    return render(request, 'cadastros/botao.html')

def home(request):
    return render(request, 'cadastros/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')
            
            try:
                usuario = Usuario.objects.get(email=email, senha=senha)
                # Se o usuário e a senha correspondem, redirecione para a página inicial
                return redirect('home')
            except Usuario.DoesNotExist:
                # Se o usuário não existe ou a senha está incorreta, adicione um erro ao formulário
                form.add_error(None, "Email ou senha incorretos.")
    else:
        form = LoginForm()

    return render(request, 'cadastros/login.html', {'form': form, 'titulo': 'Login'})
