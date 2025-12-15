import re

POSTAL_RE = re.compile(r"^\s*(\d{3}-\d{4})\s*$")

def split_location(location_raw: str | None) -> tuple[str | None, str | None]:
    """
    '194-0211\n相原町3338-1' -> ('194-0211', '相原町3338-1')
    """
    if not location_raw:
        return None, None

    s = str(location_raw).strip().strip('"')  # たまに引用符が混ざる場合に備える
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.strip() for ln in s.split("\n") if ln.strip()]

    if not lines:
        return None, None

    m = POSTAL_RE.match(lines[0])
    if m:
        postal = m.group(1)
        addr = " ".join(lines[1:]) if len(lines) > 1 else None
        return postal, addr

    # 先頭が郵便番号じゃない場合は、全部住所として扱う
    return None, " ".join(lines)
