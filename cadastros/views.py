from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm,CandidatoEtapa1Form, CandidatoEtapa2Form, CaoGuiaForm, FormacaoDuplaForm, LoginForm, CustomUserCreationForm
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import CandidatoEtapa1Form, CandidatoEtapa2Form
from .models import Candidato

def cadastro_etapa1(request):
    if request.method == 'POST':
        form = CandidatoEtapa1Form(request.POST)
        if form.is_valid():
            # Salva a primeira parte
            candidato = form.save()
            
            # Armazena o ID do candidato na sessão para usar na etapa 2
            request.session['candidato_id'] = str(candidato.id_candidato)
            
            # Redireciona para a etapa 2
            return redirect('cadastro_etapa2')
    else:
        form = CandidatoEtapa1Form()
    
    return render(request, 'cadastros/cadastro_etapa1.html', {'form': form, 'titulo': 'Cadastro Inicial'})

def cadastro_etapa2(request):
    # Tenta pegar o ID salvo na sessão
    candidato_id = request.session.get('candidato_id')
    
    if not candidato_id:
        # Se não tiver ID, volta para o início (segurança)
        return redirect('cadastro_etapa1')
        
    # Busca o candidato no banco de dados
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    
    if request.method == 'POST':
        # Carrega o formulário com a instância do candidato existente para ATUALIZAR
        form = CandidatoEtapa2Form(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            
            # Limpa a sessão e redireciona para o sucesso ou home
            del request.session['candidato_id']
            return redirect('home') # Ou uma página de sucesso
    else:
        form = CandidatoEtapa2Form(instance=candidato)
        
    return render(request, 'cadastros/cadastro_etapa2.html', {'form': form, 'titulo': 'Cadastro Complementar'})
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