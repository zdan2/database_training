from datetime import datetime
from sqlalchemy import select
from .models import Nursery
from .normalize import split_location

def import_nurseries(db, records: list[dict]) -> dict:
    inserted = updated = skipped = 0

    for r in records:
        # --- 必須 ---
        if "id" not in r or "保育園名" not in r:
            skipped += 1
            continue

        try:
            source_id = int(r["id"])
        except Exception:
            skipped += 1
            continue

        name = str(r.get("保育園名", "")).strip()
        if not name:
            skipped += 1
            continue


        postal_code, address = split_location(r.get("所在地"))

        phone = (str(r.get("電話", "")).strip() or None)

        # 複数行のまま保存してOK（必要なら後でサービス表に分解できる）
        other_services = (str(r.get("その他の事業内容", "")).strip() or None)

        homepage_url = (str(r.get("ホームページ", "")).strip() or None)
        guidebook_url = (str(r.get("ガイドブック", "")).strip() or None)

        # 既存行を source_id で検索
        existing = db.scalar(select(Nursery).where(Nursery.source_id == source_id))

        now = datetime.now()

        if existing is None:
            db.add(Nursery(
                source_id=source_id,
                name=name,
                postal_code=postal_code,
                address=address,
                phone=phone,
                other_services=other_services,
                homepage_url=homepage_url,
                guidebook_url=guidebook_url,
                imported_at=now,
            ))
            inserted += 1
        else:
            changed = False

            def set_if_diff(attr: str, value):
                nonlocal changed
                if getattr(existing, attr) != value:
                    setattr(existing, attr, value)
                    changed = True

            set_if_diff("name", name)
            set_if_diff("postal_code", postal_code)
            set_if_diff("address", address)
            set_if_diff("phone", phone)
            set_if_diff("other_services", other_services)
            set_if_diff("homepage_url", homepage_url)
            set_if_diff("guidebook_url", guidebook_url)

            if changed:
                existing.imported_at = now
                updated += 1

    db.commit()
    return {"inserted": inserted, "updated": updated, "skipped": skipped}
