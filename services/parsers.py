import re

TEAM_LINE = re.compile(
    r"^\s*[-*]?\s*(?P<name>[^()\[\]]+?)\s*\((?P<role>[^()\[\]]+)\)\s*(?:\[(?P<kv>[^\]]+)\])?\s*$"
)

def parse_team(text: str):
    """
    Lines:
      - Jane Doe (Software Engineer)
      - Jane Doe (Software Engineer) [wh=25]
    wh = weekly capacity in hours
    """
    rows = []
    for line in (text or "").splitlines():
        m = TEAM_LINE.match(line)
        if not m:
            continue
        name = m.group("name").strip()
        role = m.group("role").strip()
        wh = None
        kv = (m.group("kv") or "").strip()
        if kv:
            for pair in kv.split(","):
                parts = [s.strip() for s in pair.split("=", 1)]
                if len(parts) == 2 and parts[0].lower() == "wh":
                    try:
                        wh = max(0, int(parts[1]))
                    except:
                        pass
        rows.append({"name": name, "role": role, "weekly_hours": wh})
    return rows

def parse_bullets(text: str):
    items = []
    for line in (text or "").splitlines():
        s = re.sub(r"^[-*]\s*", "", line.strip())
        if s:
            items.append(s)
    return items
