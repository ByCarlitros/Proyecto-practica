from django import forms
from .models import Solicitud
from django.forms import DateTimeInput
from datetime import datetime

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre_usuario', 'nombre_archivo', 'validado_por', 'fecha_subida', 'fecha_actualizacion', 'fuente', 'lugar', 'estado', 'comentario']

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        
        if not solicitud.pk:  # Si es una nueva solicitud
            solicitud.fecha_subida = datetime.now()  # Asignamos la fecha y hora actual a 'fecha_subida'
        
        # Actualizamos la fecha de actualización solo cuando se edite
        if solicitud.pk and not solicitud.fecha_actualizacion:
            solicitud.fecha_actualizacion = datetime.now()  # Solo si no tiene un valor previo
        
        if commit:
            solicitud.save()
        return solicitud

    # Fecha subido: solo lectura, no editable por el usuario
    fecha_subida = forms.CharField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), disabled=True)

    # Fecha de actualización: solo debe ser modificada en el backend cuando se actualiza
    fecha_actualizacion = forms.CharField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), disabled=True)
