from django.urls import path
from .views import cadastro_etapa1, cadastro_cao_etapa1, verificar_id_cao_etapa2, cadastro_cao_etapa2, cadastrar_usuario, cadastrar_formacao, cadastro_etapa2, home, login_view, verificar_cpf_etapa2

urlpatterns = [
# urls de usuário e formacao 
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('formacoes/cadastrar/', cadastrar_formacao, name='cadastrar_formacao'),

    # urls DE CANDIDATO ---
    path('candidato/novo/', cadastro_etapa1, name='cadastro_etapa1'),
    path('candidato/buscar/', verificar_cpf_etapa2, name='verificar_cpf_etapa2'),
    path('candidato/etapa2/<str:cpf>/', cadastro_etapa2, name='cadastro_etapa2'),

    # urls DE CÃO-GUIA ---
    path('cao/novo/', cadastro_cao_etapa1, name='cadastro_cao_etapa1'),
    path('cao/buscar/', verificar_id_cao_etapa2, name='verificar_id_cao_etapa2'),
    path('cao/etapa2/<str:id_cao>/', cadastro_cao_etapa2, name='cadastro_cao_etapa2'),

    # urls de login e home
    path('home/', home, name='home'),
    path('', login_view, name='login'),
]

