import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Atlantic.settings")

import django

django.setup()

from scripts.reset_hr_catalog_and_personal import collect_counts
from scripts.sync_hr_cargos_from_excel import apply_sync, build_output, build_snapshot, plan_sync
from scripts.map_hr_snapshot import Mapper, load_rows
from human_resources.views import process_import_records

DEFAULT_CARGOS_INPUT = "/code/Data personal activo.xlsx"
DEFAULT_CARGOS_SHEET = "BD PERSONAL"


def import_personal(personal_input):
    source_rows = load_rows(personal_input)
    mapper = Mapper()
    records = [mapper.map_row(raw_row, row_number) for row_number, raw_row in source_rows]
    summary = process_import_records(records)
    return {
        "input_path": personal_input,
        "total_rows": len(records),
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Orquesta reset RH, rebuild de cargos e importación de personal.")
    parser.add_argument("--personal-input", required=True)
    parser.add_argument("--cargos-input", default=DEFAULT_CARGOS_INPUT)
    parser.add_argument("--cargos-sheet", default=DEFAULT_CARGOS_SHEET)
    parser.add_argument("--backup-dir", default="/code/static_media/tmp")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    snapshot = build_snapshot(args.cargos_input, args.cargos_sheet)
    sync_plan = plan_sync(snapshot)
    payload = {
        "mode": "apply" if args.apply else "dry-run",
        "initial_counts": collect_counts(),
        "cargos_sync_preview": build_output("dry-run", sync_plan),
        "personal_input": args.personal_input,
        "cargos_input": args.cargos_input,
        "cargos_sheet": args.cargos_sheet,
    }

    if not args.apply:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return

    from scripts.reset_hr_catalog_and_personal import build_backup_payload, reset_hr_data, write_backup

    backup_path = write_backup(args.backup_dir, build_backup_payload())
    reset_result = reset_hr_data()
    sync_plan = plan_sync(snapshot)
    cargos_result = apply_sync(sync_plan, args.backup_dir)
    personal_result = import_personal(args.personal_input)

    payload.update({
        "backup_path": backup_path,
        "reset_result": reset_result,
        "cargos_result": cargos_result,
        "personal_result": personal_result,
        "final_counts": collect_counts(),
    })
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
