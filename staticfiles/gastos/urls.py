from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_gastos, name='home_gastos'),
    path('categorias/', views.home_categorias, name='home_categorias'),
    path('cuentas/', views.home_cuentas, name='home_cuentas'),
    
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/borrar/<int:categoria_id>/', views.borrar_categoria, name='borrar_categoria'),
    
    path('cuentas/crear/', views.agregar_cuenta, name='agregar_cuenta'),
    path('cuentas/borrar/<int:cuenta_id>/', views.borrar_cuenta, name='borrar_cuenta'),
    path('cuentas/editar/<int:cuenta_id>/', views.editar_cuenta, name='editar_cuenta'),
    
    path('nuevo/', views.crear_gasto, name='crear_gasto'),
    path('detalle/<int:cuenta_id>/', views.detalle_gastos, name='detalle_gastos'),
    path('eliminar/<int:cuenta_id>/<int:gasto_id>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('editar/<int:gasto_id>/<int:cuenta_id>/', views.editar_gasto, name='editar_gasto'),
    
]
