import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Atlantic.settings")

import django

django.setup()

from django.db import transaction

from human_resources.models import (
    area,
    auxilios_contrato,
    base_personal,
    cambios_salario,
    cargo,
    contratos_personal,
    descargos,
    empalmes,
    historico_base_teorica,
    importacion_personal_job,
)

DEFAULT_BACKUP_DIR = "/code/static_media/tmp"


def ensure_backup_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def serialize_queryset(queryset):
    return list(queryset.values())


def build_backup_payload():
    return {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "areas": serialize_queryset(area.objects.values("id", "descripcion", "estructura_id", "responsable_id")),
        "cargos": serialize_queryset(
            cargo.objects.values(
                "id",
                "descripcion",
                "area_id",
                "activo",
                "cantidad_aprobada",
                "criticidad",
                "tipo_posicion",
                "tap",
            )
        ),
        "base_personal": serialize_queryset(base_personal.objects.all()),
        "contratos_personal": serialize_queryset(contratos_personal.objects.all()),
        "auxilios_contrato": serialize_queryset(auxilios_contrato.objects.all()),
        "cambios_salario": serialize_queryset(cambios_salario.objects.all()),
        "empalmes": serialize_queryset(empalmes.objects.all()),
        "descargos": serialize_queryset(descargos.objects.all()),
        "historico_base_teorica": serialize_queryset(historico_base_teorica.objects.all()),
        "importacion_personal_job": serialize_queryset(importacion_personal_job.objects.all()),
    }


def write_backup(backup_dir, payload):
    ensure_backup_dir(backup_dir)
    backup_path = Path(backup_dir) / f"hr_rebuild_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return str(backup_path)


def collect_counts():
    return {
        "areas": area.objects.count(),
        "cargos": cargo.objects.count(),
        "base_personal": base_personal.objects.count(),
        "contratos_personal": contratos_personal.objects.count(),
        "auxilios_contrato": auxilios_contrato.objects.count(),
        "cambios_salario": cambios_salario.objects.count(),
        "empalmes": empalmes.objects.count(),
        "descargos": descargos.objects.count(),
        "historico_base_teorica": historico_base_teorica.objects.count(),
        "importacion_personal_job": importacion_personal_job.objects.count(),
    }


def reset_hr_data():
    before = collect_counts()
    with transaction.atomic():
        area.objects.exclude(responsable__isnull=True).update(responsable=None)
        auxilios_contrato.objects.all().delete()
        cambios_salario.objects.all().delete()
        empalmes.objects.all().delete()
        descargos.objects.all().delete()
        contratos_personal.objects.all().delete()
        base_personal.objects.all().delete()
        historico_base_teorica.objects.all().delete()
        cargo.objects.all().delete()
        importacion_personal_job.objects.all().delete()
    after = collect_counts()
    return {"before": before, "after": after}


def main():
    parser = argparse.ArgumentParser(description="Resetea personal, contratos y cargos de RH con backup previo.")
    parser.add_argument("--backup-dir", default=DEFAULT_BACKUP_DIR)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    payload = {
        "mode": "apply" if args.apply else "dry-run",
        "current_counts": collect_counts(),
    }

    if not args.apply:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    backup_path = write_backup(args.backup_dir, build_backup_payload())
    reset_result = reset_hr_data()
    payload.update({
        "backup_path": backup_path,
        "reset_result": reset_result,
    })
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
