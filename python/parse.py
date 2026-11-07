"""Minimal Python client (standard library only).
Usage: REPLY_INTEL_KEY=ri_live_... BASE=http://localhost:8787 python3 parse.py
"""
import hashlib, hmac, json, os, time, urllib.request

BASE = os.environ.get("BASE", "https://reply-intel.pages.dev")

def parse_reply(email: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE}/v1/parse", data=json.dumps(email).encode(), method="POST",
        headers={"Authorization": f"Bearer {os.environ['REPLY_INTEL_KEY']}", "Content-Type": "application/json",
                 "Idempotency-Key": email.get("message_id", str(time.time()))})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def verify_webhook(secret: str, header: str, raw_body: bytes, tolerance: int = 300) -> bool:
    """Verify X-Reply-Intel-Signature on events we POST to you."""
    parts = dict(p.split("=", 1) for p in header.split(","))
    t = int(parts["t"])
    if abs(time.time() - t) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{t}.".encode() + raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, parts.get("v1", ""))

if __name__ == "__main__":
    ev = parse_reply({"from": "Jordan <jordan@example.com>", "subject": "Re: pilot",
                      "text": "Can you do 20% off for 300 seats?", "message_id": "<demo-py@x>"})
    print(ev["classification"]["primary_intent"], ev["recommended_action"], ev["requires_human_review"])
