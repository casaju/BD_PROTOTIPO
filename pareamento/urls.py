from django.urls import path
from .views import selecionar_pareamento, resultado_pareamento, confirmar_pareamento

urlpatterns = [
    path('', selecionar_pareamento, name='selecionar_pareamento'),
    path('resultado/<str:cpf>/', resultado_pareamento, name='resultado_pareamento'),
    path('confirmar/<str:cpf>/<str:id_cao>/', confirmar_pareamento, name='confirmar_pareamento'),
]