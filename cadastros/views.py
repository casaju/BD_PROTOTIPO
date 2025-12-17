from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm,CandidatoEtapa1Form, CandidatoEtapa2Form, CaoGuiaForm, FormacaoDuplaForm, LoginForm, CustomUserCreationForm, BuscaCPFForm
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import CandidatoEtapa1Form, CandidatoEtapa2Form
from .models import Candidato
from django.contrib import messages

def cadastro_etapa1(request):
    if request.method == 'POST':
        form = CandidatoEtapa1Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etapa 1 concluída! Você pode continuar agora ou depois.')
            return redirect('home') # Volta para home para o usuário escolher o que fazer
    else:
        form = CandidatoEtapa1Form()
    
    return render(request, 'cadastros/cadastro_etapa1.html', {'form': form, 'titulo': 'Etapa 1: Dados Pessoais'})

# --- Nova View: Verifica CPF antes da Etapa 2 ---
def verificar_cpf_etapa2(request):
    if request.method == 'POST':
        form = BuscaCPFForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            # Verifica se existe no banco
            if Candidato.objects.filter(pk=cpf).exists():
                # Se existe, vai para a etapa 2 passando o CPF na URL
                return redirect('cadastro_etapa2', cpf=cpf)
            else:
                messages.error(request, 'CPF não encontrado! Realize a Etapa 1 primeiro.')
    else:
        form = BuscaCPFForm()
    
    return render(request, 'cadastros/busca_cpf.html', {'form': form, 'titulo': 'Acessar Etapa 2'})

# --- View da Etapa 2 ---
def cadastro_etapa2(request, cpf):
    # Busca o candidato pelo CPF passado na URL ou dá erro 404
    candidato = get_object_or_404(Candidato, pk=cpf)
    
    if request.method == 'POST':
        form = CandidatoEtapa2Form(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro completo realizado com sucesso!')
            return redirect('home')
    else:
        form = CandidatoEtapa2Form(instance=candidato)
        
    return render(request, 'cadastros/cadastro_etapa2.html', {
        'form': form, 
        'titulo': f'Etapa 2: Completar perfil de {candidato.nome_candidato}'
    })


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
    return render(request, 'cadastros/cadastrosuser.html', context)


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

            # Tenta encontrar o usuário pelo email
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                user_obj = None
                username = None

            # Autentica o usuário usando o username e a senha
            user = authenticate(request, username=username, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Email ou senha incorretos.")
    else:
        form = LoginForm()

    return render(request, 'cadastros/login.html', {'form': form, 'titulo': 'Login'})