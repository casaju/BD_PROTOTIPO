from django.urls import path
from .views import cadastrar_candidato, cadastrar_caoguia, cadastrar_usuario, cadastrar_formacao

urlpatterns = [
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('caes/cadastrar/', cadastrar_caoguia, name='cadastrar_cao'),
    path('formacoes/cadastrar/', cadastrar_formacao, name='cadastrar_formacao'),
    path('candidatos/cadastrar/', cadastrar_candidato, name='cadastrar_candidato'),
]
