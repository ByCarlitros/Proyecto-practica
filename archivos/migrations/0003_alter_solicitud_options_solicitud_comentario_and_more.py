# Generated by Django 5.2.1 on 2025-05-14 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivos', '0002_solicitud_delete_archivo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solicitud',
            options={'ordering': ['-fecha_subida'], 'verbose_name': 'Solicitud', 'verbose_name_plural': 'Solicitudes'},
        ),
        migrations.AddField(
            model_name='solicitud',
            name='comentario',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.IntegerField(choices=[(1, 'En revisión'), (2, 'Aprobado'), (3, 'Rechazado')], default=1),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='nombre_usuario',
            field=models.CharField(default='Usuario', max_length=255),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_subida',
            field=models.DateField(default=datetime.date.today, editable=False),
        ),
    ]
