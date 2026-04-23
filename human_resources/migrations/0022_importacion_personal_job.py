from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0021_alter_contratos_personal_bonificacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='importacion_personal_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_archivo', models.CharField(max_length=255)),
                ('ruta_archivo', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('MAPPING', 'MAPPING'), ('RUNNING', 'RUNNING'), ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED')], default='PENDING', max_length=20)),
                ('total_filas', models.IntegerField(default=0)),
                ('filas_importables', models.IntegerField(default=0)),
                ('filas_procesadas', models.IntegerField(default=0)),
                ('creados', models.IntegerField(default=0)),
                ('actualizados', models.IntegerField(default=0)),
                ('omitidos', models.IntegerField(default=0)),
                ('conflictos', models.IntegerField(default=0)),
                ('errores', models.IntegerField(default=0)),
                ('no_importables', models.IntegerField(default=0)),
                ('ignoradas', models.IntegerField(default=0)),
                ('detalles_conflicto', models.JSONField(blank=True, default=list)),
                ('detalles_error', models.JSONField(blank=True, default=list)),
                ('detalles_no_importables', models.JSONField(blank=True, default=list)),
                ('mensaje_error', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
