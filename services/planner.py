from datetime import datetime, date
from typing import List, Dict, Any

from .roles import norm_role

def _complexity(objectives: str, reqs: List[str]) -> float:
    req_len = sum(len(r) for r in reqs)
    base = 1.0 + 0.15 * len(reqs) + 0.0008 * (len(objectives) + req_len)
    return min(3.0, max(1.0, base))

def _template_for(ptype: str) -> List[Dict[str, Any]]:
    p = (ptype or "").lower()
    if "web" in p or "site" in p:
        return [
            {"title": "Requirements consolidation", "owner_role": "Project Manager",   "base": 10},
            {"title": "Design prototype",           "owner_role": "Designer",          "base": 16},
            {"title": "MVP implementation",         "owner_role": "Software Engineer", "base": 28},
            {"title": "QA & polish",                "owner_role": "QA",                "base": 12},
            {"title": "Deploy & handoff",           "owner_role": "DevOps",            "base": 8},
        ]
    if "data" in p:
        return [
            {"title": "Problem framing & KPIs",     "owner_role": "Project Manager",   "base": 8},
            {"title": "Data ingestion + EDA",       "owner_role": "Data Engineer",     "base": 20},
            {"title": "Modeling & evaluation",      "owner_role": "Data Scientist",    "base": 28},
            {"title": "Serving + monitoring",       "owner_role": "MLOps",             "base": 16},
        ]
    return [
        {"title": "Scope & plan",               "owner_role": "Project Manager",   "base": 8},
        {"title": "Design",                     "owner_role": "Designer",          "base": 12},
        {"title": "Build",                      "owner_role": "Engineer",          "base": 28},
        {"title": "Test & release",             "owner_role": "QA",                "base": 12},
    ]

def _canon_team(team_raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    canon = []
    for m in team_raw:
        canon.append({
            "name": m["name"],
            "role": m["role"],
            "role_norm": norm_role(m["role"]),
            "weekly_hours": int(m.get("weekly_hours") or 20),  # default capacity if omitted
        })
    return canon

def _best_owner(canon_team: List[Dict[str, Any]], owner_role: str) -> Dict[str, Any]:
    on = norm_role(owner_role)
    for m in canon_team:
        if m["role_norm"] == on:
            return m
    if "engineer" in on:
        for m in canon_team:
            if "engineer" in m["role_norm"]:
                return m
    if "project manager" in on:
        for m in canon_team:
            if "project manager" in m["role_norm"]:
                return m
    return canon_team[0] if canon_team else {"name": "Owner", "role_norm": on, "weekly_hours": 20}

def run_planner(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    If estimate_hours=False: return tasks without 'hours' and resources without allocation.
    If estimate_hours=True: compute hours by base*complexity*role-fit and allocate by capacity over horizon.
    """
    team_raw = payload.get("team", [])
    objectives = payload.get("objectives", "") or ""
    reqs = payload.get("requirements", []) or []
    ptype = payload.get("project_type") or ""
    estimate_hours = bool(payload.get("estimate_hours", False))
    horizon_weeks = max(1, int(payload.get("horizon_weeks", 2)))

    team = _canon_team(team_raw)
    template = _template_for(ptype)
    cx = _complexity(objectives, reqs)

    # tasks
    tasks: List[Dict[str, Any]] = []
    for t in template:
        owner = _best_owner(team, t["owner_role"])
        fit = 1.0 if norm_role(t["owner_role"]) == owner["role_norm"] else 1.25
        rec = {"title": t["title"], "owner": owner["name"]}
        if estimate_hours:
            rec["hours"] = round(t["base"] * cx * fit, 1)
        tasks.append(rec)

    # milestones
    mid = max(1, len(tasks) // 2)
    milestones = [
        {"name": "MVP",  "due": date.today().isoformat(), "tasks": [t["title"] for t in tasks[:mid]]},
        {"name": "Beta", "due": date.today().isoformat(), "tasks": [t["title"] for t in tasks[mid:]]},
    ]

    # resources + allocation
    resources = [{"name": m["name"], "role": m["role"], "weekly_hours": m["weekly_hours"]} for m in team]
    if estimate_hours and resources:
        total_hours = sum(t.get("hours", 0) for t in tasks)
        capacity = {m["name"]: m["weekly_hours"] * horizon_weeks for m in team}
        cap_sum = max(1, sum(capacity.values()))
        for r in resources:
            share = capacity[r["name"]] / cap_sum
            r["allocated_hours"] = round(total_hours * share, 1)
            r["utilization_pct"] = round(100 * r["allocated_hours"] / max(1, capacity[r["name"]]), 1)

    return {
        "tasks": tasks,
        "milestones": milestones,
        "resources": resources,
        "token_cost": {"input": 0, "output": 0, "usd_estimate": 0.0},
        "meta": {
            "run_at": datetime.utcnow().isoformat() + "Z",
            "complexity": round(cx, 2),
            "horizon_weeks": horizon_weeks,
        },
    }
