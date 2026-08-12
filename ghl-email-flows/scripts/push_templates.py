#!/usr/bin/env python3
"""Lane A: push a chain's email masters into GHL as email templates via the builder API.

Usage:
  push_templates.py <masters-dir> [--prefix "quote-followup-v5"] [--updated-by claude] [--dry-run]
  push_templates.py <masters-dir> --delete-prefix "quote-followup-v4"   # remove an old set

masters-dir: a chain dir containing new-0N.html (or *.html) + manifest.json
             (e.g. ./email-masters/quote-followup-v1)

What it does per email:
  1. POST /emails/builder                     -> create template shell {name, type:html}
  2. POST /emails/builder/data                -> load the full HTML (updatedBy required)
  3. Prints the previewUrl                    -> EYEBALL EACH ONE before calling it done
The workflow email step still has to be pointed at the template in the GHL UI (browser
lane) — that is the only manual part left.

Auth: GHL_API_KEY / GHL_LOCATION_ID env, else secrets/ghl.env.
Rate-limited 0.6s between calls. Idempotent-ish: if a template with the exact target
name already exists, its content is updated instead of creating a duplicate.
"""
import argparse, glob, json, os, subprocess, sys, time

BASE = "https://services.leadconnectorhq.com"


def _sh(cmd):
    return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True).stdout.strip()


def resolve(name, env_grep):
    """Resolve a credential: environment variable first, then secrets/ghl.env."""
    v = os.environ.get(name, "")
    if v:
        return v
    for env_file in [os.environ.get("GHL_ENV_FILE", ""),
                     "secrets/ghl.env",
                     os.path.expanduser("~/.ghl/ghl.env")]:
        if env_file and os.path.exists(env_file):
            v = _sh(f"grep {env_grep} {env_file} | cut -d= -f2 | tr -d '\"'")
            if v:
                return v
    return ""


def api(method, path, tok, body=None):
    args = ["curl", "-s", "-X", method, f"{BASE}{path}",
            "-H", f"Authorization: Bearer {tok}", "-H", "Version: 2021-07-28",
            "-H", "Content-Type: application/json", "-H", "User-Agent: ghl-email-flows/2.0"]
    if body is not None:
        args += ["-d", json.dumps(body)]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"raw": r.stdout[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("masters_dir")
    ap.add_argument("--prefix", default=None, help="template name prefix; default = dir basename")
    ap.add_argument("--updated-by", default="selr-ai-automation")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delete-prefix", default=None, help="delete all templates whose name starts with this, then exit")
    a = ap.parse_args()

    tok = resolve("GHL_API_KEY", "GHL_API_KEY")
    loc = resolve("GHL_LOCATION_ID", "GHL_LOCATION_ID")
    if not (tok and loc):
        sys.exit("Missing GHL token/location. Ask Claude to run kp doctor — it self-heals.")

    existing = api("GET", f"/emails/builder?locationId={loc}&limit=100", tok).get("builders", [])
    by_name = {b.get("name"): (b.get("id") or b.get("templateId")) for b in existing}

    if a.delete_prefix:
        doomed = {n: i for n, i in by_name.items() if n and n.startswith(a.delete_prefix)}
        for n, tid in doomed.items():
            if a.dry_run:
                print("would delete:", n)
            else:
                r = api("DELETE", f"/emails/builder/{loc}/{tid}", tok)
                print("deleted:" if r.get("ok") else "FAILED delete:", n, r if not r.get("ok") else "")
                time.sleep(0.6)
        print(f"{len(doomed)} template(s) matched")
        return

    d = os.path.abspath(os.path.expanduser(a.masters_dir))
    prefix = a.prefix or os.path.basename(d.rstrip("/"))
    manifest = {}
    mpath = os.path.join(d, "manifest.json")
    if os.path.exists(mpath):
        manifest = {m["n"]: m for m in json.load(open(mpath))}
    files = sorted(glob.glob(os.path.join(d, "new-0*.html"))) or sorted(glob.glob(os.path.join(d, "*.html")))
    files = [f for f in files if "preview" not in os.path.basename(f)]
    if not files:
        sys.exit(f"no email HTML files in {d}")

    results = []
    for f in files:
        n = None
        base = os.path.basename(f)
        if base.startswith("new-"):
            n = int(base[4:6])
        meta = manifest.get(n, {})
        subj = meta.get("subject", base)
        name = f"{prefix} - E{n or '?'} - {subj[:60]}"
        html = open(f, encoding="utf-8").read()

        if a.dry_run:
            print("would push:", name, f"({len(html)} bytes)")
            continue

        tid = by_name.get(name)
        if not tid:
            r = api("POST", "/emails/builder", tok, {"locationId": loc, "name": name, "type": "html"})
            tid = r.get("id")
            if not tid:
                print("FAILED create:", name, r)
                continue
            time.sleep(0.6)
        r2 = api("POST", "/emails/builder/data", tok, {
            "locationId": loc, "templateId": tid, "html": html,
            "editorType": "html", "previewText": meta.get("preview", ""),
            "updatedBy": a.updated_by})
        ok = r2.get("ok")
        results.append((name, tid, r2.get("previewUrl", ""), ok))
        print(("OK   " if ok else "FAIL "), name, "| template:", tid)
        if ok:
            print("      preview:", r2.get("previewUrl", "")[:110])
        else:
            print("      error:", str(r2)[:200])
        time.sleep(0.6)

    if results:
        print(f"\n{sum(1 for r in results if r[3])}/{len(results)} pushed."
              " Open every previewUrl and eyeball before pointing workflow steps at them.")


if __name__ == "__main__":
    main()
