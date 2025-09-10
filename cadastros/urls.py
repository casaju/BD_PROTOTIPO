from django.urls import path
from .views import cadastrar_candidato, cadastrar_caoguia, cadastrar_usuario, cadastrar_formacao, cadastro_inicio, home, login_view

urlpatterns = [
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('caes/cadastrar/', cadastrar_caoguia, name='cadastrar_caoguia'),
    path('formacoes/cadastrar/', cadastrar_formacao, name='cadastrar_formacao'),
    path('candidatos/cadastrar/', cadastrar_candidato, name='cadastrar_candidato'),
    path('cadastro/', cadastro_inicio, name='cadastro_inicio'),
    path('home/', home, name='home'),
    path('', login_view, name='login'),
]


