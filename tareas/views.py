from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Tareas
from contacto.models import Contacto
from django.contrib.auth.decorators import login_required

# Create your views here.

# TAREAS PENDIENTES TAREAS PENDIENTES TAREAS PENDIENTES TAREAS PENDIENTES 
@login_required(login_url='signin')
#Funcion para mostrar las tareas pendientes.
def tareasPendientes(request):
    #Recupera las tareas del modelo tareas en las que el usuario es el actual. Se utiliza filter para filtrar las tareas, en este caso para que cada user tenga sus tareas.
    tareas = Tareas.objects.filter(user=request.user)
    #Recupera las tareas en progreso y que pertenecen a un usuario.
    tareas_en_curso = Tareas.objects.filter(estado='en_curso', user=request.user)
    #Recupera los contactos del modelo Contacto que pertenecen al user.
    contactos = Contacto.objects.filter(user=request.user)
    
    #Diccionario de contexto para almacenar los datos que se van a pasar a la plantilla.
    context = {
        #Tareas recuperadas anteriormente, permite acceder a las tareas en la plantilla utilizando la clave tareas
        'tareas': tareas,
        #Igual que tareas
        'contactos': contactos,
        #Igual que tareas
        'tareas_en_curso': tareas_en_curso
    }
    #Renderiza la plantila tareasPendientes.html con el diccionario contexto. Con el contexto la plantilla tendra acceso a los datos de las tareas, contactos y tareas en progreso.
    return render(request, 'tareas/tareasPendientes.html', context)
# FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES FIN TAREAS PENDIENTES 


# TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO TAREAS EN CURSO
@login_required(login_url='signin')
#Funcion para mostrar las tareas en curso 
def tareasCurso(request):
    #Recupera las tareas del modelo tareas en las que el usuario es el actual. Se utiliza filter para filtrar las tareas, en este caso para que cada user tenga sus tareas.
    tareas_curso = Tareas.objects.filter(estado='en_curso', user=request.user)
    #Recupera los contactos del modelo Contacto que pertenecen al user.
    contactos = Contacto.objects.filter(user=request.user)
    
    #Diccionario de contexto para almacenar los datos que se van a pasar a la plantilla.
    context = {
        #Tareas recuperadas anteriormente, permite acceder a las tareas en la plantilla utilizando la clave tareas
        'tareas': tareas_curso,
        #Igual que tareas
        'contactos': contactos
    }
    #Renderiza la plantila tareasCurso.html con el diccionario contexto. Con el contexto la plantilla tendra acceso a los datos de las tareas, contactos y tareas en progreso.
    return render(request, 'tareas/tareasCurso.html', context)
# FIN TAREAS EN CURSO # FIN TAREAS EN CURSO # FIN TAREAS EN CURSO # FIN TAREAS EN CURSO 


# TAREAS COMPLETADAS TAREAS COMPLETADAS TAREAS COMPLETADAS TAREAS COMPLETADAS
@login_required(login_url='signin')
#Funcion para mostrar las tareas completadas. 
def tareasCompletadas(request):
    #Recupera las tareas del modelo tareas en las que el usuario es el actual. Se utiliza filter para filtrar las tareas, en este caso para que cada user tenga sus tareas.
    tareas_completadas = Tareas.objects.filter(estado='completada', user=request.user)
    #Recupera los contactos del modelo Contacto que pertenecen al user.
    contactos = Contacto.objects.filter(user=request.user)
    
    #Bucle en todas las tareas completadas
    for tarea in tareas_completadas:
        #Establece el campo fcompletada de la tarea actual en el valor actual de la fecha y hora actual teniendo en cuenta la zona horaria configurada en Django.
        tarea.fcompletada = timezone.now()
        #Se guarda la tarea en la BBDD
        tarea.save()
    
    #Contexto igual que en todas las funciones con las claves y valores de lo que se renderizara en pantalla
    context = {
        'tareas_completadas': tareas_completadas,
        'contactos': contactos,
    }
    #Renderizacion igual que todas
    return render(request, 'tareas/tareasCompletadas.html', context)
# FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS FIN TAREAS COMPLETADAS 


# CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA CREAR TAREA
@login_required(login_url='signin')
#Funcion para crear tareas  
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
#Funcion para borrar la tarea  
def borrarTarea(request, tarea_id):
    #Obtiene la tarea especifica con el ID y el user. Si la tarea no existe o no pertenece al user actual arroja error 404.
    tarea = get_object_or_404(Tareas, id=tarea_id, user=request.user)
    #Borra la tarea de la BBDD
    tarea.delete()

    #Verifica si existe parametro next en la URL de la solicitud. Se utiliza para redirigir al user a una pagina especifica despues de eliminar la tarea.
    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)
    else:
        #Si no existe el parametro next en la URL lo redirecciona a tareasPendientes
        return redirect('tareasPendientes')
# FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA FIN BORRAR TAREA 


# EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA EDITAR TAREA
@login_required(login_url='signin')
#Funcion para editar tareas. 
def editarTarea(request, tarea_id):
    #Obtiene la tarea por su ID
    tarea = Tareas.objects.get(id=tarea_id)

    #Verifica si la solicitud es POST, se actualizan los campos de la tarea con los valores proporcionados en la solicitud.
    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.importante = request.POST['importante']
        
        #Se obtienen los ID de los contactos seleccionados y se filtran los contactos correspondientes
        contactos_ids = request.POST.getlist('contactos')  
        contactos = Contacto.objects.filter(id__in=contactos_ids)

        #Actualiza la relacion de contactos de la tarea usando set y se guarda la tarea modificada.
        tarea.contacto.set(contactos)
        tarea.save()

        #Despues de guardar la tarea modificada redirige al user a tareasPendientes
        return redirect('tareasPendientes')

    #Contexto y render igual que todas las funciones.
    context = {
        'tarea': tarea,
        'contactos': Contacto.objects.all(),
    }

    return render(request, 'tareas/editarTarea.html', context)
# FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA FIN MOVER TAREA  


# MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A CURSO MOVER A 
@login_required(login_url='signin')
#Funcion para mover una tarea de estado pendiente o completada a estado en curso 
def mover_a_curso(request, tarea_id):
    #Obtiene la tarea por el ID o el user o arroja un 404 
    tarea = get_object_or_404(Tareas, pk=tarea_id, user=request.user)
    #Actualiza la tarea a en curso.
    tarea.estado = 'en_curso'
    #Guarda la tarea en la BBDD.
    tarea.save()

    #Obtiene las tareas pendientes del user y excluye la tarea que se movio a en curso utilizando exclude.
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
#Funcion para mover una tarea de estado en curso o completada a estado pendiente. 
def mover_a_pendientes(request, tarea_id):
    #Obtiene la tarea por el ID, actualiza el estado y la guarda en la BBDD
    tarea = Tareas.objects.get(pk=tarea_id)
    tarea.estado = 'pendiente'
    tarea.save()
    
    #Redirecciona
    return redirect('tareasPendientes')
# FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES FIN MOVER A PENDIENTES 


# MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA MOVER A COMPLETADA
@login_required(login_url='signin') 
#Funcion para mover una tarea de estado pendiente o en curso a estado completada.
def completar_tarea(request, tarea_id):
    #Obtiene la tarea mediante el ID, cambia el estado a completada, obtiene la fecha y horario en la que se completo la tarea y la guarda en la BBDD
    tarea = Tareas.objects.get(pk=tarea_id)
    tarea.estado = 'completada'
    tarea.fcompletada = timezone.now()
    tarea.save()
    
    #Redirecciona
    return redirect('tareasCompletadas')
# FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA FIN MOVER A COMPLETADA 


# VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA VER TAREA 

# FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA FIN VER TAREA 