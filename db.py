from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import streamlit as st


@st.cache_resource
def _get_client():
    url = st.secrets.get("supabase_url", "")
    key = st.secrets.get("supabase_key", "")
    if not url or not key:
        return None
    from supabase import create_client

    return create_client(url, key)


def is_connected() -> bool:
    return _get_client() is not None


def hash_items(items: list[dict]) -> str:
    canonical = json.dumps(items, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def load_action_overlay(workstream: str) -> dict | None:
    client = _get_client()
    if not client:
        return None
    try:
        resp = (
            client.table("action_edits")
            .select("items, base_hash")
            .eq("workstream", workstream)
            .execute()
        )
        if resp.data:
            return resp.data[0]
    except Exception:
        return None


def save_action_overlay(
    workstream: str, items: list[dict], base_hash: str
) -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.table("action_edits").upsert(
            {
                "workstream": workstream,
                "items": items,
                "base_hash": base_hash,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()
        return True
    except Exception:
        return False


def clear_action_overlay(workstream: str) -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.table("action_edits").delete().eq(
            "workstream", workstream
        ).execute()
        return True
    except Exception:
        return False
