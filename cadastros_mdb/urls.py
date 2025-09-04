from django.urls import path
from .views import informacoes_caoguia, informacoes_candidato,  informacoes_cadastro
urlpatterns = [
    path('informacoes/candidatos/', informacoes_candidato, name='informacoes_candidato'),
    path('informacoes/cao-guia/', informacoes_caoguia, name='informacoes_caoguia'),
    path('informacoes/', informacoes_cadastro, name='informacoes_cadastros'),

]