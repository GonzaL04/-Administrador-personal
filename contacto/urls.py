from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexContacto, name='indexContacto'),
    path('editar_contacto/<int:contacto_id>/', views.editar_contacto, name='editar_contacto'),
    path('borrar_contacto/<int:id>', views.borrar_contacto, name="borrar_contacto"),
    path('agregar_contacto/', views.agregar_contacto, name='agregar_contacto'),
]
