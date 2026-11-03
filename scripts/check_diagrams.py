# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""Check the actual browser geometry of all chapter diagrams, or selected slugs."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def main():
    selected=set(sys.argv[1:]);js=(ROOT/'scripts/diagram_checks.js').read_text();failures=[];count=0;arrows=labels=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1800,'height':1200})
        for path in sorted(ROOT.glob('chapters/*/assets/*.html')):
            if selected and path.stem not in selected:continue
            count+=1;page.goto(path.as_uri());page.evaluate('document.fonts.ready');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');result=page.evaluate(js)
            arrows+=result['arrows'];labels+=result['labels']
            for suffix in ['', '-dark']:
                if not path.with_name(path.stem+suffix+'.png').exists():result['issues'].append(['missing-png',suffix])
            if result['issues']:failures.append((path.relative_to(ROOT),result['issues']))
        browser.close()
    for path,issues in failures:print(path,json.dumps(issues,ensure_ascii=False))
    if failures:raise SystemExit(f'FAIL: {len(failures)} of {count} diagrams have geometry or artifact issues.')
    print(f'PASS: {count} diagrams; {arrows} arrows; {labels} attached labels; no distant labels, crossing labels, overlapping labels, clipped text or missing PNGs.')
if __name__=='__main__':main()
