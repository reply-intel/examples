# Reply Intel examples and benchmark

Examples for [Reply Intel](https://reply-intel.pages.dev), an API that turns an inbound email reply into versioned JSON: one of 15 intents (interested, pricing question, out-of-office, bounce, unsubscribe, needs human review…), extracted entities (quantity, discount, meeting times, return date) and a recommended next action.

Status: private beta, free, no paying customers yet. Built and run by one developer.

## What's here

| Path | What it is |
|---|---|
| `n8n/reply-intel-triage.json` | Gmail Trigger → Reply Intel → Switch (Human review / Hot lead / Pause / Stop). Import into n8n and add a Header Auth credential. Not yet tested by the author on a live n8n; please open an issue if a field differs. |
| `typescript/parse.ts`, `python/parse.py` | Minimal clients, including webhook signature verification in Python. |
| `openapi.yaml` | API reference. |
| `benchmark/` | The independent test set and per-email results, so the numbers below can be checked. |

## Benchmark (2026-11-07)

80 synthetic replies written by a separate author who never saw the rules (`benchmark/blind-v1.jsonl`). Every non-automated reply is sent to the model; bounces and auto-replies are caught by rules first.

| Configuration (Cloudflare Workers AI) | Correct primary intent |
|---|---|
| Rules + Llama 3.3 70B fp8-fast (production) | 85.0% (68/80) |
| Rules + GPT-OSS 20B | 78.8% |
| Rules + Qwen3 30B A3B | 70.0% |
| Rules + Granite 4.0 Micro | 67.5% |
| Rules only | 53.8% |

Reproduce: `python3 benchmark/score.py benchmark/results-*.csv`. 80 replies is a small sample (roughly ±8 points). This set is now public, so future versions will be measured on a new blind set.

## Getting access

Beta keys are free. Email replyintel@agentmail.to with what you're building and roughly how many replies a month you handle.

## License

MIT for the examples and benchmark files in this repository.
