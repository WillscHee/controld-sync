#!/usr/bin/env python3
"""
Convert DoH blocklist (plain domains) to ControlD/HaGeZi JSON folder format.

Usage:
    python3 convert-doh.py <input.txt> <output.json>

The input is a plain domain list (one domain per line).
The output is a HaGeZi JSON folder with action do=0 (block).
"""
import json
import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.txt> <output.json>", file=sys.stderr)
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    # Read the plain domain list
    domains = []
    seen = set()
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('!'):
                continue
            if line not in seen:
                seen.add(line)
                domains.append(line)

    # Convert to HaGeZi JSON folder format
    hagezi_json = {
        "group": {
            "group": "DoH Blocklist",
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
