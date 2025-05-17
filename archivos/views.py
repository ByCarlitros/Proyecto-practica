from django.shortcuts import render, redirect, get_object_or_404
from .models import Solicitud
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect


# Vista de usuario para crear solicitudes
def menu_usuario(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario', '').strip()
        nombre_archivo = request.POST.get('nombre_archivo', '').strip()
        fuente = request.POST.get('fuente', '').strip()
        lugar = request.POST.get('lugar', '').strip()

        if all([nombre_usuario, nombre_archivo, fuente, lugar]):
            nueva_solicitud = Solicitud(
                nombre_usuario=nombre_usuario,
                nombre_archivo=nombre_archivo,
                fuente=fuente,
                lugar=lugar,
                fecha_subida=datetime.now(),
                fecha_actualizacion=datetime.now(),
                estado=1,
                validado_por="Ninguno"
            )
            nueva_solicitud.save()

            # Mostrar modal de éxito
            return render(request, 'menu_usuario.html', {
                'archivos': Solicitud.objects.all(),
                'solicitud_exitosa': True
            })
        else:
            archivos = Solicitud.objects.all()
            return render(request, 'menu_usuario.html', {
                'archivos': archivos,
                'error': 'Todos los campos son obligatorios.'
            })

    archivos = Solicitud.objects.all()
    return render(request, 'menu_usuario.html', {'archivos': archivos})

# Vista de administrador para listar solicitudes
def menu_admin(request):
    archivos = Solicitud.objects.all()
    return render(request, 'menu_admin.html', {'archivos': archivos})


# Vista para actualizar una solicitud
def actualizar_solicitud(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        if not solicitud_id:
            return redirect('menu_admin')

        solicitud = get_object_or_404(Solicitud, id=solicitud_id)

        solicitud.validado_por = request.POST.get('validado_por', '').strip()
        solicitud.comentario = request.POST.get('comentario', '').strip()

        estado_post = request.POST.get('estado')
        try:
            solicitud.estado = int(estado_post)
        except (ValueError, TypeError):
            pass

        solicitud.fecha_actualizacion = datetime.now()
        solicitud.save()

        url = reverse('menu_admin') + '?updated=1'
        return HttpResponseRedirect(url)

    return redirect('menu_admin')