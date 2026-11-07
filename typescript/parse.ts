// Minimal TypeScript client. Node >= 18. Usage: REPLY_INTEL_KEY=ri_live_... BASE=http://localhost:8787 node parse.ts
const BASE = process.env.BASE ?? "https://reply-intel.pages.dev";

export async function parseReply(email: { from: string; subject?: string; text?: string; html?: string; message_id?: string }) {
  const res = await fetch(`${BASE}/v1/parse`, {
    method: "POST",
    headers: { authorization: `Bearer ${process.env.REPLY_INTEL_KEY}`, "content-type": "application/json", "idempotency-key": email.message_id ?? crypto.randomUUID() },
    body: JSON.stringify(email),
  });
  if (!res.ok) throw new Error(`reply-intel ${res.status}: ${JSON.stringify(await res.json())}`);
  return res.json();
}

const ev = await parseReply({ from: "Jordan <jordan@example.com>", subject: "Re: pilot", text: "Can you do 20% off for 300 seats?", message_id: "<demo-1@x>" });
if (ev.requires_human_review) console.log("Send to a person:", ev.review_reasons);
else console.log("Automate:", ev.classification.primary_intent, "→", ev.recommended_action);
