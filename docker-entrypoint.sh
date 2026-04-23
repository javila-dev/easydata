#!/bin/sh
set -e

echo "Esperando conexión a la base de datos..."
python - <<'PY'
import os
import time
import django
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Atlantic.settings")
django.setup()

max_attempts = 30
for attempt in range(1, max_attempts + 1):
    try:
        connections["default"].cursor()
        print("Base de datos disponible.")
        break
    except Exception as exc:
        if attempt == max_attempts:
            raise
        print(f"Intento {attempt}/{max_attempts} falló: {exc}")
        time.sleep(2)
PY

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando aplicación..."
exec "$@"
