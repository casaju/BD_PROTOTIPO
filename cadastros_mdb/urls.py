from django.urls import path
from . import views
urlpatterns = [

    path('informacoes/candidatos/', views.informacoes_candidato, name='informacoes_candidato'),
    path('informacoes/cao-guia/', views.informacoes_caoguia, name='informacoes_caoguia'),
    path('informacoes/', views.informacoes_cadastro, name='informacoes_cadastros'),
    path('parear/<int:candidato_id>/', views.parear_candidato_cao, name='parear'),
]