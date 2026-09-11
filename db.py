from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone

import streamlit as st

logger = logging.getLogger(__name__)


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
        logger.exception("Failed to load action overlay for %s", workstream)
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
        logger.exception("Failed to save action overlay for %s", workstream)
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
        logger.exception("Failed to clear action overlay for %s", workstream)
        return False


# ── User visits ──


def load_user_visit(username: str) -> str | None:
    client = _get_client()
    if not client:
        return None
    try:
        resp = (
            client.table("user_visits")
            .select("last_visit")
            .eq("username", username)
            .execute()
        )
        if resp.data:
            return resp.data[0]["last_visit"]
    except Exception:
        logger.exception("Failed to load visit for %s", username)
    return None


def save_user_visit(username: str) -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.table("user_visits").upsert(
            {
                "username": username,
                "last_visit": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()
        return True
    except Exception:
        logger.exception("Failed to save visit for %s", username)
        return False


# ── Workstream notes ──


def load_workstream_notes(
    workstream: str | None = None, limit: int = 50
) -> list[dict]:
    client = _get_client()
    if not client:
        return []
    try:
        q = (
            client.table("workstream_notes")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
        )
        if workstream:
            q = q.eq("workstream", workstream)
        resp = q.execute()
        return resp.data or []
    except Exception:
        logger.exception("Failed to load workstream notes")
        return []


def save_workstream_note(
    workstream: str, author: str, content: str, category: str = "Update"
) -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.table("workstream_notes").insert(
            {
                "workstream": workstream,
                "author": author,
                "content": content,
                "category": category,
            }
        ).execute()
        return True
    except Exception:
        logger.exception("Failed to save note for %s/%s", workstream, author)
        return False


def mark_notes_synced() -> int:
    client = _get_client()
    if not client:
        return 0
    try:
        resp = (
            client.table("workstream_notes")
            .update({"synced_at": datetime.now(timezone.utc).isoformat()})
            .is_("synced_at", "null")
            .execute()
        )
        return len(resp.data) if resp.data else 0
    except Exception:
        logger.exception("Failed to mark notes as synced")
        return 0


def count_new_notes_since(since: str) -> dict[str, int]:
    client = _get_client()
    if not client:
        return {}
    try:
        resp = (
            client.table("workstream_notes")
            .select("workstream")
            .gt("created_at", since)
            .execute()
        )
        counts: dict[str, int] = {}
        for row in resp.data or []:
            ws = row["workstream"]
            counts[ws] = counts.get(ws, 0) + 1
        return counts
    except Exception:
        logger.exception("Failed to count new notes since %s", since)
        return {}


def get_overlay_timestamps() -> dict[str, str]:
    client = _get_client()
    if not client:
        return {}
    try:
        resp = (
            client.table("action_edits")
            .select("workstream, updated_at")
            .execute()
        )
        return {r["workstream"]: r["updated_at"] for r in (resp.data or [])}
    except Exception:
        logger.exception("Failed to load overlay timestamps")
        return {}
