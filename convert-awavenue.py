#!/usr/bin/env python3
"""
Convert AWAvenue AdGuard-format blocklist to ControlD/HaGeZi JSON folder format.

Usage:
    python3 convert-awavenue.py <input.txt> <output.json>

The input is an AdGuard-format list (lines like ||domain^).
The output is a HaGeZi JSON folder with action do=0 (block).
"""
import json
import sys
import urllib.request


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.txt> <output.json>", file=sys.stderr)
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    # Read the AdGuard format list
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the AdGuard format
    domains = []
    seen = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('!'):
            continue
        # Handle ||domain^ format (domain-only rules)
        if line.startswith('||') and line.endswith('^'):
            domain = line[2:-1]
            if domain and domain not in seen:
                seen.add(domain)
                domains.append(domain)
        # Skip other rule types (regex, URL filters, etc.)

    # Convert to HaGeZi JSON folder format
    hagezi_json = {
        "group": {
            "group": "AWAvenue No.Unwelcome",
            "action": {
                "do": 0,
                "status": 1
            }
        },
        "rules": [
            {
                "PK": domain,
                "action": {
                    "do": 0,
                    "status": 1
                }
            }
            for domain in domains
        ]
    }

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(hagezi_json, f, indent=2)

    print(f"Converted {len(domains)} domains to {output_path}")


if __name__ == "__main__":
    main()
