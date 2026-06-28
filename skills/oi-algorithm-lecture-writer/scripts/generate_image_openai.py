#!/usr/bin/env python3
import argparse
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"config not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"invalid json config: {e}")

    missing = []
    for key in ("api_key", "base_url", "model"):
        val = str(cfg.get(key, "")).strip()
        if not val or val.startswith("填写"):
            missing.append(key)
    if missing:
        raise SystemExit("missing config field(s): " + ", ".join(missing))
    return cfg


def build_body(cfg, prompt):
    body = {
        "model": cfg["model"],
        "prompt": prompt,
    }
    for key in ("size", "quality", "output_format", "response_format", "background", "n"):
        if cfg.get(key):
            body[key] = cfg[key]
    if isinstance(cfg.get("extra_body"), dict):
        body.update(cfg["extra_body"])
    return body


def request_image(cfg, prompt):
    endpoint = cfg["base_url"].rstrip("/") + "/images/generations"
    data = json.dumps(build_body(cfg, prompt), ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": "Bearer " + cfg["api_key"],
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=int(cfg.get("timeout", 120))) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"image api error {e.code}: {detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"image api request failed: {e}")


def save_image(result, output):
    data = result.get("data") or []
    if not data:
        raise SystemExit("image api response has no data")

    item = data[0]
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if item.get("b64_json"):
        output.write_bytes(base64.b64decode(item["b64_json"]))
        return output

    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as resp:
            output.write_bytes(resp.read())
        return output

    raise SystemExit("image api response has neither b64_json nor url")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a lecture image with an OpenAI-compatible Images API."
    )
    parser.add_argument("--config", default="config/image_api.local.json")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    result = request_image(cfg, args.prompt)
    path = save_image(result, args.output)
    print(path)


if __name__ == "__main__":
    sys.exit(main())
