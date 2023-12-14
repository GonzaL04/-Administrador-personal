from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Tareas
from contacto.models import Contacto
from django.contrib.auth.decorators import login_required

# Create your views here.

# TAREAS PENDIENTES TAREAS PENDIENTES TAREAS PENDIENTES TAREAS PENDIENTES 
@login_required(login_url='signin')
def tareasPendientes(request):
    tareas = Tareas.objects.filter(user=request.user)
    tareas_en_curso = Tareas.objects.filter(estado='en_curso', user=request.user)
    contactos = Contacto.objects.filter(user=request.user)
    
    context = {
        'tareas': tareas,
        'contactos': contactos,
        'tareas_en_curso': tareas_en_curso
    }
    return render(request, 'tareas/tareasPendientes.html', context)
# FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES 


# TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO
@login_required(login_url='signin')
def tareasCurso(request):
    tareas_curso = Tareas.objects.filter(estado='en_curso', user=request.user)
    contactos = Contacto.objects.filter(user=request.user)
    
    context = {
        'tareas': tareas_curso,
        'contactos': contactos
    }
    return render(request, 'tareas/tareasCurso.html', context)
# FIN TAREAS EN CURSO # FIN TAREAS EN CURSO # FIN TAREAS EN CURSO # FIN TAREAS EN CURSO 


# TAREAS COMPLETADAS TAREAS COMPLETADAS TAREAS COMPLETADAS TAREAS COMPLETADAS
@login_required(login_url='signin')
def tareasCompletadas(request):
    tareas_completadas = Tareas.objects.filter(estado='completada', user=request.user)
    contactos = Contacto.objects.filter(user=request.user)
    
    for tarea in tareas_completadas:
        tarea.fcompletada = timezone.now()
        tarea.save()

    context = {
        'tareas_completadas': tareas_completadas,
        'contactos': contactos,
    }
    return render(request, 'tareas/tareasCompletadas.html', context)
# FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS 


# CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA
@login_required(login_url='signin')
def crearTarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        importante = request.POST['importante']
        contactos_ids = request.POST.getlist('contactos')

        tarea = Tareas(
            titulo=titulo,
            descripcion=descripcion,
            importante=importante,
            user=request.user
        )
        tarea.save()

        contactos_asignados = Contacto.objects.filter(user=request.user, id__in=contactos_ids)
        tarea.contacto.set(contactos_asignados)

        return redirect('tareasPendientes')

    contactos = Contacto.objects.filter(user=request.user)

    context = {
        'contactos': contactos,
    }

    return render(request, 'tareas/crearTarea.html', context)
# FIN CREAR TAREA FIN CREAR TAREA FIN CREAR TAREA FIN CREAR TAREA FIN CREAR TAREA 


# BORRAR TAREA BORRAR TAREA BORRAR TAREA BORRAR TAREA BORRAR TAREA BORRAR TAREA
@login_required(login_url='signin')
def borrarTarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, user=request.user)
    tarea.delete()

    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)
    else:
        return redirect('tareasPendientes')
# FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA 


# EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA
@login_required(login_url='signin')
def editarTarea(request, tarea_id):
    tarea = Tareas.objects.get(id=tarea_id)
    
    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.importante = request.POST['importante']

        contactos_ids = tarea.contacto.values_list('id', flat=True) 
        contactos = Contacto.objects.filter(id__in=contactos_ids)

        tarea.contacto.set(contactos)
        tarea.save()

        return redirect('tareasPendientes')

    context = {
        'tarea': tarea,
        'contactos': Contacto.objects.all(),
    }

    return render(request, 'tareas/editarTarea.html', context)
# FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA  


# MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A 
@login_required(login_url='signin')
def mover_a_curso(request, tarea_id):
    tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
    tarea.estado = 'en_curso'
    tarea.save()

    tareas_pendientes = Tareas.objects.filter(estado='pendiente', user=request.user)
    tareas_pendientes = tareas_pendientes.exclude(pk=tarea_id)

    #Contexto igual que en las demas funciones.
    context = {
        'tareas': tareas_pendientes
    }

    return render(request, 'tareas/tareasPendientes.html', context)
# FIN MOVER A CURSO FIN MOVER A CURSO FIN MOVER A CURSO FIN MOVER A CURSO FIN MOVER A CURSO 


# MOVER A PENDIENTES MOVER A PENDIENTES MOVER A PENDIENTES MOVER A PENDIENTES MOVER A PENDIENTES
@login_required(login_url='signin')
def mover_a_pendientes(request, tarea_id):
    tarea = Tareas.objects.get(pk=tarea_id)
    tarea.estado = 'pendiente'
    tarea.save()
    
    return redirect('tareasPendientes')
# FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES 


# MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA
@login_required(login_url='signin') 
def completar_tarea(request, tarea_id):
    tarea = Tareas.objects.get(pk=tarea_id)
    tarea.estado = 'completada'
    tarea.fcompletada = timezone.now()
    tarea.save()
    
    return redirect('tareasCompletadas')
# FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA 


# VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA 

# FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA 