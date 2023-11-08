from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from gastos import models
from gastos.forms import *
from gastos.models import Categorias
from django.db.models import Sum
from datetime import date, timedelta

def home_gastos(request):
    cuentas = Cuentas.objects.filter(user=request.user)
    categorias = Categorias.objects.filter(user=request.user)

    context = {
        'cuentas_data': [],
        'cuentas': cuentas,
        'categorias': categorias,
    }

    today = date.today()

    for cuenta in cuentas:
        ultimo_gasto_cuenta = Gastos.objects.filter(fk_id_cuenta=cuenta).order_by('-fecha', '-hora').first()
        
        gastos_cuenta = Gastos.objects.filter(fk_id_cuenta=cuenta)

        primer_dia_mes = today.replace(day=1)
        ultimo_dia_mes = (today.replace(day=1, month=(today.month % 12) + 1) - timedelta(days=1))

        mes_actual_cuenta = gastos_cuenta.filter(
            fecha__range=[primer_dia_mes, ultimo_dia_mes]
        ).aggregate(Sum('precio'))['precio__sum']

        mes_actual = mes_actual_cuenta if mes_actual_cuenta else 0

        gasto_total_cuenta = gastos_cuenta.aggregate(Sum('precio'))['precio__sum']
        gasto_total = gasto_total_cuenta if gasto_total_cuenta else 0

        cuenta_data = {
            'cuenta': cuenta,
            'ultimo_gasto': ultimo_gasto_cuenta,
            'mes_actual': mes_actual,
            'gasto_total': gasto_total,
            'gastos_cuenta': gastos_cuenta,
        }

        context['cuentas_data'].append(cuenta_data)

    return render(request, 'gastos/homeGastos.html', context)

def home_categorias(request):
    categorias = Categorias.objects.filter(user=request.user)
    context = {
        'categorias' : categorias
    }
    return render(request, 'gastos/homeCategorias.html', context)

def home_cuentas(request):
    cuentas = Cuentas.objects.filter(user=request.user)
    context = {
        'cuentas' : cuentas,
    }
    return render(request, 'gastos/homeCuentas.html', context)

def detalle_gastos(request, cuenta_id):
    cuenta = get_object_or_404(Cuentas, id=cuenta_id, user=request.user)
    gastos = Gastos.objects.filter(fk_id_cuenta=cuenta)
    categorias = Categorias.objects.filter(user=request.user)
    
    context = {
        'cuenta': cuenta,
        'gastos': gastos,
        'categorias': categorias
    }

    return render(request, 'gastos/detalleGastos.html', context)

# VIEWS CATEGORIAS
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = request.user
            categoria.save()
            return redirect('home_categorias')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'gastos/homeCategorias.html', context)

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categorias, id=categoria_id, user=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('home_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form
    }
    
    return render(request, 'gastos/homeCategorias.html', context)

def borrar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categorias, id=categoria_id, user=request.user)
    if request.method == 'POST':
        categoria.delete()
        return redirect('home_categorias')
    
    context = {
        'categoria': categoria
    }
    
    return render(request, 'gastos/homeCategorias.html', context)
# END VIEWS CATEGORIAS

# VIEWS CUENTAS
def agregar_cuenta(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.user = request.user
            cuenta.save()
            return redirect('home_cuentas')
    else:
        form = PerfilForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'gastos/homeCuentas.html', context)

def borrar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuentas, id=cuenta_id, user=request.user)
    if request.method == 'POST':
        cuenta.delete()
        return redirect('home_cuentas')
    
    context = {
        'cuenta': cuenta
    }
    
    return render(request, 'gastos/homeCuentas.html', context)

def editar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuentas, id=cuenta_id, user=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('home_cuentas')
    else:
        form = PerfilForm(instance=cuenta)
    
    context = {
        'cuenta': cuenta,
        'form': form
    }
    
    return render(request, 'gastos/editarCuenta.html', context)
# END VIEWS CUENTAS


# VIEWS GASTOS
def crear_gasto(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categorias, id=categoria_id, user=request.user)
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        fecha = request.POST.get('fecha')
        fecha_gasto = date.fromisoformat(fecha)
        if fecha_gasto > date.today():
            messages.error(request, "No puedes agregar un gasto en el futuro.")
            return redirect('home_gastos')

        cuentas_seleccionadas = request.POST.getlist('cuentas')

        for cuenta_id in cuentas_seleccionadas:
            cuenta = get_object_or_404(Cuentas, id=cuenta_id, user=request.user)

            nuevo_gasto = Gastos(
                fk_id_categoria=categoria,
                fk_id_cuenta=cuenta,
                descripción=descripcion,
                precio=precio,
                fecha=fecha
            )
            nuevo_gasto.save()
            
        return redirect('home_gastos')

def eliminar_gasto(request, gasto_id, cuenta_id):
    gasto = get_object_or_404(Gastos, id=gasto_id, fk_id_cuenta__user=request.user)

    if request.method == 'POST':
        gasto.delete()
        return redirect('detalle_gastos', cuenta_id=cuenta_id)
    
    context = {
        'gasto': gasto
    }

    return render(request, 'gastos/detalleGastos.html', context)

def editar_gasto(request, gasto_id, cuenta_id):
    gasto = get_object_or_404(Gastos, id=gasto_id, fk_id_cuenta__user=request.user)

    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('detalle_gastos', cuenta_id=cuenta_id)
    else:
        form = GastoForm(instance=gasto)

    context = {
        'form' : form,
        'gasto' : gasto,
    }

    return render(request, 'gastos/detalleGastos.html', context)

# END VIEWS GASTOS

class GastoCalendar(ListView):
    model = models.Gastos
    template_name = "gastos/homeGastos.html"