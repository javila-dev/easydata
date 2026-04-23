from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0020_alter_base_personal_tipo_riesgo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratos_personal',
            name='bonificacion',
            field=models.CharField(
                blank=True,
                choices=[
                    ('BONIFICACION POR RENDIMIENTO DE PLANTA', 'BONIFICACION POR RENDIMIENTO DE PLANTA'),
                    ('COMISION', 'COMISION'),
                    ('COMISION COMERCIALES', 'COMISION COMERCIALES'),
                    ('AUXILIO POR PORCIONADOR', 'AUXILIO POR PORCIONADOR'),
                    ('AUXILIO POR MONTACARGAS', 'AUXILIO POR MONTACARGAS'),
                    ('AUXILIO POR CONECTIVIDAD', 'AUXILIO POR CONECTIVIDAD'),
                    ('AUXILIO POR INVENTARIOS', 'AUXILIO POR INVENTARIOS'),
                    ('AUXILIO DE DISPONIBILIDAD', 'AUXILIO DE DISPONIBILIDAD'),
                    ('AUXILIO DE ESCOLARIDAD', 'AUXILIO DE ESCOLARIDAD'),
                    ('AUXILIO DE VIVIENDA', 'AUXILIO DE VIVIENDA'),
                    ('BONO DE MOVILIZACION MENSUAL ADICIONAL CELTA', 'BONO DE MOVILIZACION MENSUAL ADICIONAL CELTA'),
                    ('INDICADORES', 'INDICADORES'),
                    ('EBITDA', 'EBITDA'),
                    ('CXS', 'CXS'),
                    ('COMPENSACION VARIABLE', 'COMPENSACION VARIABLE'),
                    ('CARGO X ENCARGO', 'CARGO X ENCARGO'),
                    ('ENCARGO', 'ENCARGO'),
                    ('ENCARGO X 3 MESES', 'ENCARGO X 3 MESES'),
                    ('ENCARGO X 6 MESES', 'ENCARGO X 6 MESES'),
                    ('GARANTIZADO X 3 MESES', 'GARANTIZADO X 3 MESES'),
                    ('GARANTIZADO LOS 6 PRIMERO MESES', 'GARANTIZADO LOS 6 PRIMERO MESES'),
                    ('GARANTIZADO LOS 2 PRIMEROS MESES', 'GARANTIZADO LOS 2 PRIMEROS MESES'),
                    ('GARANTIZADO HASTA DEFINIR INDICADORES', 'GARANTIZADO HASTA DEFINIR INDICADORES'),
                    ('GARANTIZADO SUSPENDIDO POR INC', 'GARANTIZADO SUSPENDIDO POR INC'),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
