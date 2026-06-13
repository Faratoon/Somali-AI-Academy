"""
utils/firebase.py  –  Firebase / Firestore helper
"""
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone
import pytz
import config

_db = None

def get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    "databaseURL": config.FIREBASE_DATABASE_URL
                })
            except Exception as e:
                print(f"[Firebase] Error initializing: {e}")
                return None
        _db = firestore.client()
    return _db

# ── User helpers ──────────────────────────────────────────────────────────────
def get_user(user_id: int) -> dict:
    db = get_db()
    if not db:
        return {}
    doc = db.collection("users").document(str(user_id)).get()
    return doc.to_dict() if doc.exists else {}

def create_or_update_user(user_id: int, data: dict):
    db = get_db()
    if not db:
        return
    ref = db.collection("users").document(str(user_id))
    doc = ref.get()
    if not doc.exists:
        data["created_at"]     = datetime.now(timezone.utc)
        data["trial_start"]    = datetime.now(timezone.utc)
        data["is_premium"]     = False
        data["daily_count"]    = 0
        data["last_msg_date"]  = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        data["channels"]       = []
        data["groups"]         = []
        ref.set(data)
    else:
        ref.update(data)

def is_premium(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False
    if user.get("is_premium"):
        return True
    # Check trial
    trial_start = user.get("trial_start")
    if trial_start:
        if hasattr(trial_start, "timestamp"):
            diff = datetime.now(timezone.utc) - trial_start.replace(tzinfo=timezone.utc)
        else:
            return False
        if diff.days <= config.TRIAL_DAYS:
            return True
    return False

def get_trial_days_left(user_id: int) -> int:
    user = get_user(user_id)
    if not user:
        return 0
    if user.get("is_premium"):
        return 999
    trial_start = user.get("trial_start")
    if trial_start:
        if hasattr(trial_start, "timestamp"):
            diff = datetime.now(timezone.utc) - trial_start.replace(tzinfo=timezone.utc)
        else:
            return 0
        remaining = config.TRIAL_DAYS - diff.days
        return max(0, remaining)
    return 0

# ── Message limit helpers ─────────────────────────────────────────────────────
def check_and_increment_msg(user_id: int) -> tuple[bool, int]:
    """Returns (allowed, count). Resets daily counter if new day."""
    db = get_db()
    if not db:
        return True, 0  # allow if DB unavailable
    ref  = db.collection("users").document(str(user_id))
    doc  = ref.get()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not doc.exists:
        ref.set({
            "daily_count":   1,
            "last_msg_date": today,
            "created_at":    datetime.now(timezone.utc),
            "trial_start":   datetime.now(timezone.utc),
            "is_premium":    False,
        })
        return True, 1

    data = doc.to_dict()
    last_date  = data.get("last_msg_date", "")
    daily_cnt  = data.get("daily_count", 0)

    if last_date != today:
        # New day → reset
        ref.update({"daily_count": 1, "last_msg_date": today})
        return True, 1

    if daily_cnt >= config.DAILY_MSG_LIMIT:
        return False, daily_cnt

    ref.update({"daily_count": firestore.Increment(1)})
    return True, daily_cnt + 1

# ── Channel / Group helpers ───────────────────────────────────────────────────
def add_channel(user_id: int, channel_id: str, channel_name: str, channel_type: str = "channel"):
    db = get_db()
    if not db:
        return
    ref  = db.collection("users").document(str(user_id))
    doc  = ref.get()
    key  = "channels" if channel_type == "channel" else "groups"
    entry = {"id": channel_id, "name": channel_name, "added_at": datetime.now(timezone.utc).isoformat()}
    if doc.exists:
        existing = doc.to_dict().get(key, [])
        if not any(c["id"] == channel_id for c in existing):
            existing.append(entry)
            ref.update({key: existing})
    else:
        ref.set({key: [entry], "created_at": datetime.now(timezone.utc)})

def get_channels(user_id: int, ctype: str = "channel") -> list:
    user = get_user(user_id)
    key  = "channels" if ctype == "channel" else "groups"
    return user.get(key, [])

def remove_channel(user_id: int, channel_id: str, ctype: str = "channel"):
    db = get_db()
    if not db:
        return
    key  = "channels" if ctype == "channel" else "groups"
    ref  = db.collection("users").document(str(user_id))
    doc  = ref.get()
    if doc.exists:
        existing = doc.to_dict().get(key, [])
        updated  = [c for c in existing if c["id"] != channel_id]
        ref.update({key: updated})

# ── Scheduled posts ───────────────────────────────────────────────────────────
def save_scheduled_post(user_id: int, post_data: dict) -> str:
    db = get_db()
    if not db:
        return ""
    ref  = db.collection("scheduled_posts").add({
        **post_data,
        "user_id":    user_id,
        "created_at": datetime.now(timezone.utc),
        "status":     "pending"
    })
    return ref[1].id

def get_pending_posts() -> list:
    db = get_db()
    if not db:
        return []
    docs = db.collection("scheduled_posts").where("status", "==", "pending").stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

def mark_post_sent(post_id: str):
    db = get_db()
    if not db:
        return
    db.collection("scheduled_posts").document(post_id).update({"status": "sent"})

# ── AI conversation memory ────────────────────────────────────────────────────
def get_conversation(user_id: int) -> list:
    db = get_db()
    if not db:
        return []
    doc = db.collection("conversations").document(str(user_id)).get()
    return doc.to_dict().get("messages", []) if doc.exists else []

def save_conversation(user_id: int, messages: list):
    db = get_db()
    if not db:
        return
    # Keep last 20 messages only
    messages = messages[-20:]
    db.collection("conversations").document(str(user_id)).set({
        "messages":   messages,
        "updated_at": datetime.now(timezone.utc)
    })

def clear_conversation(user_id: int):
    db = get_db()
    if not db:
        return
    db.collection("conversations").document(str(user_id)).delete()
