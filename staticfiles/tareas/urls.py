from django.contrib import admin
from django.urls import path, include
from tareas import views

urlpatterns = [
    # URL de tareasPendientes
    path('tareas/', views.tareasPendientes, name='tareasPendientes'),
    
    # URL para crear una tarea
    path('tareas/crear/', views.crearTarea, name='crearTarea'),
    
    # URL para borrar una tarea por su ID en la pagina de tareasPendientes
    path('tareas/pendientes/<int:tarea_id>/borrar/', views.borrarTarea, name='borrarTareaPendientes'),
    
    # URL para borrar una tarea por su ID en la pagina de tareasCurso
    path('tareas/curso/<int:tarea_id>/borrar/', views.borrarTarea, name='borrarTareaCurso'),
    
    # URL para borrar una tarea por su ID en la pagina de tareasCompletadas
    path('tareas/completadas/<int:tarea_id>/borrar/', views.borrarTarea, name='borrarTareaCompletadas'),
    
    # URL para editar tareas
    path('tareas/editar/<int:tarea_id>/', views.editarTarea, name='editarTarea'),
    
    # URL de tareasCurso
    path('tareas/curso/', views.tareasCurso, name='tareasCurso'),
    
    # URL para mover una tarea pendiente a una tarea en curso
    path('tareas/mover-a-curso/<int:tarea_id>/', views.mover_a_curso, name='mover_a_curso'),
    
    # URL para mover una tarea en curso a tarea pendiente
    path('tareas/curso/<int:tarea_id>/mover-a-pendientes/', views.mover_a_pendientes, name='mover_a_pendientes'),
    
    # URL para mover una tarea en curso a tarea completada
    path('tareas/curso/<int:tarea_id>/completar/', views.completar_tarea, name='completar_tarea'),
    
    # URL de tareasCompletadas
    path('tareas/completadas/', views.tareasCompletadas, name='tareasCompletadas'),
    

]