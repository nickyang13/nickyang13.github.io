#!/usr/bin/env python3
"""Static checks for the portfolio page. No network. Run: python3 tests/portfolio_smoke.py"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

STORE_URLS = [
    "https://apps.apple.com/jp/app/brandnewday/id6766146214",
    "https://apps.apple.com/us/app/brandnewstudy/id6766146214",
    "https://apps.apple.com/hk/app/brandnewday/id6766146214",
    "https://apps.apple.com/tw/app/brandnewday/id6766146214",
    "https://apps.apple.com/us/app/opennote-ai-local-assistant/id6776658629",
    "https://apps.apple.com/hk/app/opennote-ai-local-assistant/id6776658629",
    "https://apps.apple.com/tw/app/opennote-ai-local-assistant/id6776658629",
]

check("fonts.googleapis.com" not in html, "Google Fonts stylesheet host is still referenced")
check("fonts.gstatic.com" not in html, "Google font file host is still referenced")
check(html.count("font-display:swap") >= 2, "self-hosted faces must use font-display:swap")
check('href="fonts/inter-latin.woff2"' in html, "Inter latin file is not referenced")
check('href="fonts/source-serif-4-latin.woff2"' in html, "Source Serif latin file is not referenced")
check("国区上架手续办理中，暂仅提供海外版本。" in html, "mainland availability note was removed")
check("美国区商店名称为 BrandNewStudy。" in html, "US listing name note was removed")
for url in STORE_URLS:
    check(html.count(url) == 1, f"store URL missing or duplicated: {url}")
check('rel="icon"' in html, "favicon link is missing")

for rel in ["fonts/inter-latin.woff2", "fonts/source-serif-4-latin.woff2", "favicon.ico", "favicon.svg"]:
    path = ROOT / rel
    check(path.is_file() and path.stat().st_size > 0, f"missing file {rel}")

for rel in ["fonts/inter-latin.woff2", "fonts/source-serif-4-latin.woff2"]:
    magic = (ROOT / rel).read_bytes()[:4]
    check(magic == b"wOF2", f"{rel} is not a woff2 file")

# Keep the visible project facts that the page already states.
for fact in ["BrandNewDay", "OpenNote AI", "TruthSeeking", "约 5 万"]:
    check(fact in html, f"existing copy is missing: {fact}")

if errors:
    print("FAILED")
    for err in errors:
        print("-", err)
    sys.exit(1)
print(f"ok {len(STORE_URLS)} store links, self-hosted fonts, favicon")
