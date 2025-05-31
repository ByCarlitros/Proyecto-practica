from django import forms
from .models import Solicitud
from datetime import datetime

class SolicitudForm(forms.ModelForm):
    fecha_subida = forms.DateTimeField(
        disabled=True,
        required=False,
        label="Fecha Subida",
        widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'readonly': 'readonly'})
    )

    fecha_actualizacion = forms.DateTimeField(
        label="Fecha Actualización",
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )

    class Meta:
        model = Solicitud
        fields = [
            'nombre_usuario',
            'nombre_archivo',
            'validado_por',
            'fecha_subida',
            'fecha_actualizacion',
            'fuente',
            'lugar',
            'estado',
            'comentario'
        ]
        labels = {
            'nombre_usuario': 'Nombre Usuario',
            'nombre_archivo': 'Nombre Archivo',
            'validado_por': 'Validado Por',
            'fuente': 'Fuente',
            'lugar': 'Lugar',
            'estado': 'Estado',
            'comentario': 'Comentario',
        }
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'placeholder': 'Nombre Usuario'}),
            'nombre_archivo': forms.TextInput(attrs={'placeholder': 'Nombre Archivo'}),
            'validado_por': forms.TextInput(attrs={'placeholder': 'Validado Por'}),
            'fuente': forms.TextInput(attrs={'placeholder': 'Fuente'}),
            'lugar': forms.TextInput(attrs={'placeholder': 'Lugar'}),
            'comentario': forms.Textarea(attrs={'placeholder': 'Comentario'}),
            'estado': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya existe instancia con fecha_actualizacion, la mostramos en formato compatible con datetime-local
        if self.instance and self.instance.fecha_actualizacion:
            self.fields['fecha_actualizacion'].initial = self.instance.fecha_actualizacion.strftime('%Y-%m-%dT%H:%M')
        # Mostrar fecha_subida con formato legible
        if self.instance and self.instance.fecha_subida:
            self.fields['fecha_subida'].initial = self.instance.fecha_subida.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, commit=True):
        solicitud = super().save(commit=False)

        # Si es nueva, asignar fecha_subida
        if not solicitud.pk:
            solicitud.fecha_subida = datetime.now()

        # fecha_actualizacion será la que viene del formulario, sin modificarla aquí

        if commit:
            solicitud.save()
        return solicitud
