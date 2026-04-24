from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0022_importacion_personal_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='importacion_personal_job',
            name='stop_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='importacion_personal_job',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'PENDING'),
                    ('MAPPING', 'MAPPING'),
                    ('RUNNING', 'RUNNING'),
                    ('STOPPING', 'STOPPING'),
                    ('STOPPED', 'STOPPED'),
                    ('COMPLETED', 'COMPLETED'),
                    ('FAILED', 'FAILED'),
                ],
                default='PENDING',
                max_length=20,
            ),
        ),
    ]
