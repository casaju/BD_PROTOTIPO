from django.shortcuts import render, redirect
from .forms import UsuarioForm,CandidatoForm, CaoGuiaForm, FormacaoDuplaForm, LoginForm, CustomUserCreationForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

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
        user_form = CustomUserCreationForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if user_form.is_valid() and usuario_form.is_valid():
            # Salva o novo usuário do Django auth
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data.get('email')
            user.save()

            # Salva o modelo Usuario, linkando-o ao novo usuário
            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()
            
            print("Dados salvos com sucesso!")
            return redirect('cadastrar_usuario')
        else:
            print("O formulário NÃO é válido. Erros no formulário de usuário:", user_form.errors)
            print("O formulário NÃO é válido. Erros no formulário de dados adicionais:", usuario_form.errors)
    else:
        user_form = CustomUserCreationForm()
        usuario_form = UsuarioForm()

    context = {
        'user_form': user_form,
        'usuario_form': usuario_form,
        'titulo': 'Cadastrar Usuario'
    }
    return render(request, 'cadastros/cadastro.html', context)


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
            
            # Autentica o usuário usando o email e a senha
            user = authenticate(request, username=email, password=senha)
            
            if user is not None:
                # Se o usuário for válido, faz o login e redireciona
                login(request, user)
                return redirect('home')
            else:
                # Se a autenticação falhar, adiciona um erro ao formulário
                form.add_error(None, "Email ou senha incorretos.")
    else:
        form = LoginForm()

    return render(request, 'cadastros/login.html', {'form': form, 'titulo': 'Login'})