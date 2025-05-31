from django.db import models
from datetime import datetime

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        (1, 'En revisión'),
        (2, 'Aprobado'),
        (3, 'Rechazado'),
    ]

    nombre_usuario = models.CharField(max_length=255)
    nombre_archivo = models.CharField(max_length=255)
    validado_por = models.CharField(max_length=255, default="Ninguno")
    fecha_subida = models.DateTimeField(default=datetime.now)  # Cambié a DateTimeField
    fecha_actualizacion = models.DateTimeField()  # Cambié a DateTimeField
    fuente = models.CharField(max_length=255)
    lugar = models.CharField(max_length=255)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=1)
    comentario = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'solicitud'

    def __str__(self):
        return self.nombre_archivo
