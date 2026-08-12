#!/usr/bin/env python3
"""Call the GHL v2 per-client MCP endpoint directly (no MCP client needed).

Usage:
  ghl_v2_call.py search_operations '{"query":"email template","limit":50}'
  ghl_v2_call.py describe_operation '{"operationId":"create-email-template","domain":"emails"}'
  ghl_v2_call.py execute_operation '{"operationId":"...","domain":"...","idempotencyKey":"...","params":{"path":{},"query":{},"body":{}}}'
  ghl_v2_call.py tools/list '{}'

Auth resolution order: $GHL_API_KEY env → secrets/ghl.env.
Location: $GHL_LOCATION_ID env → secrets/ghl.env.
"""
import glob, json, os, subprocess, sys

ENDPOINT = "https://services.leadconnectorhq.com/mcp/anthropic/v2"


def _sh(cmd):
    r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    return r.stdout.strip()


def resolve(name, env_grep):
    v = os.environ.get(name, "")
    if v:
        return v
    candidates = [os.environ.get("GHL_ENV_FILE", "")] + sorted(glob.glob("secrets/ghl.env"))
    for env_file in candidates:
        if env_file and os.path.exists(env_file):
            v = _sh(f"grep {env_grep} {env_file} | cut -d= -f2 | tr -d '\"'")
            if v:
                return v
    return v


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    tool, args = sys.argv[1], json.loads(sys.argv[2])
    token = resolve("GHL_API_KEY", "GHL_API_KEY")
    loc = resolve("GHL_LOCATION_ID", "GHL_LOCATION_ID")
    if not token:
        sys.exit("No GHL token found ($GHL_API_KEY env or secrets/ghl.env).")

    if tool == "tools/list":
        body = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    else:
        body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                "params": {"name": tool, "arguments": args}}

    r = subprocess.run(
        ["curl", "-s", "-X", "POST", ENDPOINT,
         "-H", f"Authorization: Bearer {token}",
         "-H", f"locationId: {loc}",
         "-H", "Content-Type: application/json",
         "-H", "Accept: application/json, text/event-stream",
         "-d", json.dumps(body)],
        capture_output=True, text=True)

    for line in r.stdout.splitlines():
        if line.startswith("data:"):
            d = json.loads(line[5:])
            content = d.get("result", {}).get("content", [])
            print(content[0]["text"] if content else json.dumps(d, indent=1))
            return
    print(r.stdout or f"no response (curl stderr: {r.stderr[:200]})")


if __name__ == "__main__":
    main()
