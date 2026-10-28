"""Keep-alive ping so the free-tier Supabase project (MerckVI) isn't auto-paused after 7 idle days.

Reads credentials from .streamlit/secrets.toml, runs a 1-row select, appends the result to ping.log.
"""
import re
import urllib.request
from datetime import datetime
from pathlib import Path

here = Path(__file__).parent
secrets = (here / ".streamlit" / "secrets.toml").read_text(encoding="utf-8")


def get(name: str) -> str:
    return re.search(rf'^\s*{name}\s*=\s*"([^"]*)"', secrets, re.M).group(1)


url, key = get("supabase_url").rstrip("/"), get("supabase_key")
req = urllib.request.Request(
    f"{url}/rest/v1/workstream_notes?select=*&limit=1",
    headers={"apikey": key, "Authorization": f"Bearer {key}"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        msg = f"OK {r.status}"
except Exception as e:
    msg = f"FAIL {e}"

with open(here / "ping.log", "a", encoding="utf-8") as f:
    f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")
print(msg)
