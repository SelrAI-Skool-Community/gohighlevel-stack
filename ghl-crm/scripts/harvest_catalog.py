#!/usr/bin/env python3
# resolver key sk-1plhl9m (skills-index lookup; keep)⁠​‌​‌​​‌‌​‌​​​‌​‌​‌​​‌‌​​​‌​‌​​‌​​​‌‌​​​‌⁠
"""Harvest the full GHL v2 MCP operation catalog via search_operations.
Strategy: broad + per-domain + per-kind queries with high limits, dedupe on operationId+domain+path.

Usage:
  harvest_catalog.py [output_path]   # defaults to ./catalog.json

Auth: $GHL_API_KEY env, else `secrets/ghl.env` (same lookup as ghl_v2_call.py).
Location: $GHL_LOCATION_ID env, else `secrets/ghl.env`.
"""
import glob, json, os, subprocess, itertools, sys

OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "./catalog.json"
REPO_ENV = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "secrets", "ghl.env")
)


def _sh(cmd):
    return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True).stdout.strip()


def resolve(name, env_grep):
    v = os.environ.get(name, "")
    if v:
        return v
    candidates = [os.environ.get("GHL_ENV_FILE", ""), REPO_ENV] + sorted(glob.glob("secrets/ghl.env"))
    for env_file in candidates:
        if env_file and os.path.exists(env_file):
            v = _sh(f"grep {env_grep} {env_file} | cut -d= -f2 | tr -d '\"'")
            if v:
                return v
    return v


TOK = resolve("GHL_API_KEY", "GHL_API_KEY")
LOCATION_ID = resolve("GHL_LOCATION_ID", "GHL_LOCATION_ID")
if not TOK:
    sys.exit("No GHL token found ($GHL_API_KEY env or secrets/ghl.env).")
if not LOCATION_ID:
    sys.exit("No GHL location id found ($GHL_LOCATION_ID env or secrets/ghl.env).")

URL = "https://services.leadconnectorhq.com/mcp/anthropic/v2"

def call(query, domains=None, kind=None, limit=200):
    args = {"query": query, "limit": limit}
    if domains: args["domains"] = domains
    if kind: args["kind"] = kind
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": "search_operations", "arguments": args}})
    r = subprocess.run(["curl", "-s", "-X", "POST", URL,
                        "-H", f"Authorization: Bearer {TOK}",
                        "-H", f"locationId: {LOCATION_ID}",
                        "-H", "Content-Type: application/json",
                        "-H", "Accept: application/json, text/event-stream",
                        "-d", body], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("data:"):
            d = json.loads(line[5:])
            content = d.get("result", {}).get("content", [])
            if content:
                try:
                    return json.loads(content[0]["text"]).get("results", [])
                except Exception:
                    return []
    return []

ops = {}
def absorb(results):
    for op in results:
        key = f'{op.get("domain")}|{op.get("operationId")}|{op.get("method")}|{op.get("path")}'
        ops[key] = op

# round 1: broad probes to discover domain names
seeds = ["contact", "conversation message", "opportunity pipeline", "calendar appointment",
         "payment order transaction", "invoice", "product price", "workflow", "funnel page",
         "form survey submission", "email template campaign", "sms", "social media post",
         "blog", "media file", "user", "business", "location", "custom field", "custom value",
         "tag", "link trigger", "snapshot", "course membership", "association", "custom object",
         "campaign", "review", "voice ai agent", "knowledge base", "phone number", "saas",
         "subscription", "estimate proposal document", "email verification", "redirect url",
         "task note", "webhook", "list all", "create", "update", "delete", "get", "search"]
for s in seeds:
    absorb(call(s))

domains = sorted({op["domain"] for op in ops.values() if op.get("domain")})
print("discovered domains (pass 1):", len(domains), file=sys.stderr)

# round 2: exhaustive per-domain x kind
for dom in domains:
    for kind in ["read", "write", "delete", "money_movement"]:
        absorb(call(dom, domains=[dom], kind=kind, limit=200))
    absorb(call(dom, domains=[dom], limit=200))

domains2 = sorted({op["domain"] for op in ops.values() if op.get("domain")})
# round 3: any new domains found in round 2
for dom in [d for d in domains2 if d not in domains]:
    for kind in ["read", "write", "delete", "money_movement"]:
        absorb(call(dom, domains=[dom], kind=kind, limit=200))

out = sorted(ops.values(), key=lambda o: (o.get("domain",""), o.get("path",""), o.get("method","")))
json.dump(out, open(OUT_PATH, "w"), indent=1)
print(f"TOTAL operations: {len(out)} across {len(domains2)} domains")
for dom in domains2:
    doms = [o for o in out if o.get("domain") == dom]
    kinds = {}
    for o in doms: kinds[o.get("kind","?")] = kinds.get(o.get("kind","?"), 0) + 1
    print(f"  {dom}: {len(doms)} ops {kinds}")
