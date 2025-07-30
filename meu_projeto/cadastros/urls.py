from django.urls import path
from .views import cadastrar_candidato, cadastrar_caoguia, cadastrar_usuario

urlpatterns = [
    path('cadastrar/candidatos/', cadastrar_candidato, name='cadastrar_candidato'),
    path('cadastrar/caoguia/', cadastrar_caoguia, name='cadastrar_caoguia'),
    path('cadastrar/usuario/', cadastrar_usuario, name='cadastrar_usuario'),
]
