def norm_role(r: str) -> str:
    r = (r or "").lower()
    if "project" in r or r == "pm":
        return "project manager"
    if "data eng" in r or r == "de":
        return "data engineer"
    if "data sci" in r or r == "ds":
        return "data scientist"
    if "mlops" in r or "devops" in r:
        return "mlops"
    if "qa" in r or "test" in r:
        return "qa"
    if "design" in r or "ux" in r:
        return "designer"
    if "software" in r or "engineer" in r or r in {"se", "swe", "fe", "be"}:
        return "software engineer"
    return r
