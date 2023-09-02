from django.contrib import admin
from .models import Cuentas, Categorias, Gastos
# Register your models here.

class CuentasAdmin(admin.ModelAdmin):
    list_display = ["user", "nombre", "fecha_de_creacion"]
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ["user", "nombre"]
class GastosAdmin(admin.ModelAdmin):
    list_display = ["fk_id_categoria", "fk_id_cuenta", "descripción", "precio", "fecha"]

admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(Cuentas, CuentasAdmin)
admin.site.register(Gastos, GastosAdmin)