from django.shortcuts import render, redirect, get_object_or_404
from .models import Solicitud
from datetime import datetime
from django.urls import reverse
from django.utils import timezone

from django.http import HttpResponseRedirect
from django.utils.timezone import make_aware, is_naive

def menu_usuario(request):
    if request.method == "POST":
        nombre_usuario = request.POST.get("nombre_usuario")
        nombre_archivo = request.POST.get("nombre_archivo")
        fuente = request.POST.get("fuente")
        lugar = request.POST.get("lugar")
        fecha_actualizacion = request.POST.get("fecha_actualizacion")
        validado_por = request.POST.get("validado_por", "Ninguno")

        if not (nombre_usuario and nombre_archivo and fuente and lugar and fecha_actualizacion):
            return render(request, "menu_usuario.html", {
                "archivos": Solicitud.objects.all().order_by("-fecha_subida"),
                "error": "Todos los campos son requeridos.",
                "today": timezone.now().strftime('%Y-%m-%dT%H:%M'),  # formato para input datetime-local
            })

        try:
            nueva_solicitud = Solicitud.objects.create(
                nombre_usuario=nombre_usuario,
                nombre_archivo=nombre_archivo,
                fuente=fuente,
                lugar=lugar,
                fecha_actualizacion=fecha_actualizacion,
                estado=1,  # En revisión
                validado_por=validado_por,
            )
            nueva_solicitud.save()
            return render(request, "menu_usuario.html", {
                "archivos": Solicitud.objects.all().order_by("-fecha_subida"),
                "solicitud_exitosa": True,
                "today": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            })
        except Exception as e:
            return render(request, "menu_usuario.html", {
                "archivos": Solicitud.objects.all().order_by("-fecha_subida"),
                "error": f"Error al guardar la solicitud: {str(e)}",
                "today": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            })

    else:
        return render(request, "menu_usuario.html", {
            "archivos": Solicitud.objects.all().order_by("-fecha_subida"),
            "today": timezone.now().strftime('%Y-%m-%dT%H:%M'),
        })

def menu_admin(request):
    archivos = Solicitud.objects.all()
    return render(request, 'menu_admin.html', {'archivos': archivos})

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

        fecha_actualizacion_str = request.POST.get('fecha_actualizacion')
        if fecha_actualizacion_str:
            try:
                fecha_actualizacion = datetime.strptime(fecha_actualizacion_str, '%Y-%m-%dT%H:%M')
                if is_naive(fecha_actualizacion):
                    fecha_actualizacion = make_aware(fecha_actualizacion)
                solicitud.fecha_actualizacion = fecha_actualizacion
            except (ValueError, TypeError):
                pass
        else:
            # Si no se entrega fecha, no se modifica el campo
            pass

        solicitud.save()

        url = reverse('menu_admin') + '?updated=1'
        return HttpResponseRedirect(url)

    return redirect('menu_admin')