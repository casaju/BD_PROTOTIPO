from django.urls import path
from .views import cadastro_etapa1, cadastrar_caoguia, cadastrar_usuario, cadastrar_formacao, cadastro_etapa2, cadastro_inicio, home, login_view, verificar_cpf_etapa2

urlpatterns = [
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('caes/cadastrar/', cadastrar_caoguia, name='cadastrar_caoguia'),
    path('formacoes/cadastrar/', cadastrar_formacao, name='cadastrar_formacao'),
    path('cadastro/', cadastro_inicio, name='cadastro_inicio'),
    path('home/', home, name='home'),
    path('', login_view, name='login'),
    path('candidato/novo/', cadastro_etapa1, name='cadastro_etapa1'),
    path('candidato/buscar/', verificar_cpf_etapa2, name='verificar_cpf_etapa2'),
    path('candidato/etapa2/<str:cpf>/', cadastro_etapa2, name='cadastro_etapa2'),
]


