import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Atlantic.settings')

import django

django.setup()

from human_resources.models import eps, sede, temporales


SEDES_TO_CREATE = [
    'PVA MEDELLIN',
    'VTAS BARRANQUILLA',
    'OFICINA BARRANQUILLA',
    'OFICINA CARTAGENA',
    'OFICINA CALDAS',
    'RETAIL CEDI',
    'VTAS BUCARAMANGA',
    'OFICINA COTA',
    'OFICINA PEREIRA',
    'OFICINA BUCARAMANGA',
]

TEMPORALES_TO_CREATE = [
    'ACTIVOS SAS',
    'AHORA SAS',
]

EPS_TO_CREATE = [
    'EPS SOS SERVICIO OCCIDENTAL',
    'EPS ASMET SALUD',
    'EPS ALIAN SALUD',
    'EPS MEDIMAS',
    'EPS COMFAORIENTE',
    'EPS COMFANORTE',
    'EPS COMFACHOCO',
    'EPS ECOOPSOS',
    'EPS COMFAHUILA',
    'EPS FUNDACION SALUD MIA',
]


def seed_sedes():
    created = []
    for descripcion in SEDES_TO_CREATE:
        _, was_created = sede.objects.get_or_create(
            descripcion=descripcion,
            defaults={'codigo_sap': None, 'codigo_map': None},
        )
        if was_created:
            created.append(descripcion)
    return created


def seed_temporales():
    created = []
    for nombre in TEMPORALES_TO_CREATE:
        _, was_created = temporales.objects.get_or_create(
            nombre=nombre,
            defaults={'activa': True},
        )
        if was_created:
            created.append(nombre)
    return created


def seed_eps():
    created = []
    for nombre in EPS_TO_CREATE:
        _, was_created = eps.objects.get_or_create(nombre=nombre)
        if was_created:
            created.append(nombre)
    return created


if __name__ == '__main__':
    sedes_created = seed_sedes()
    temporales_created = seed_temporales()
    eps_created = seed_eps()

    print('sedes_creadas', sedes_created)
    print('temporales_creadas', temporales_created)
    print('eps_creadas', eps_created)
