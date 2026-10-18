"""Build the CNSC Member Activity Radar page.

Usage:
  python3 tools/build.py [--from <radar.html>] [out.html]

Data source, in order of preference:
  --from <html>  the embedded <script type="application/json" id="radar-data"> block of an existing page
                 (for example the editorial artifact), so the weekly run can carry the data forward
  data/*.json    meta.json, taxonomy.json, members.json, news.json, events.json, sources.json

Output: a single self-contained HTML page (default radar.html in the repo root). GitHub Pages serves
index.html, so publish with: python3 tools/build.py index.html (only after the owner's go-ahead).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'tools', 'template.html')
args = sys.argv[1:]
src_html = None
if '--from' in args:
    i = args.index('--from'); src_html = args[i + 1]; del args[i:i + 2]
out = args[0] if args else os.path.join(ROOT, 'radar.html')

def load(name):
    with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
        return json.load(f)

if src_html:
    raw = open(src_html, encoding='utf-8').read()
    m = re.search(r'<script type="application/json" id="radar-data">\n?(.*?)\n?</script>', raw, re.S)
    d = json.loads(m.group(1).replace('<\\/', '</'))
else:
    tax = load('taxonomy.json')
    d = {"meta": load('meta.json'), **tax, "members": load('members.json'),
         "news": load('news.json'), "events": load('events.json'), "sources": load('sources.json')}

# sanity checks the weekly run relies on
ids = {m['id'] for m in d['members']}
for n in d['news']:
    for mid in n.get('m', []):
        assert mid in ids, f"news item {n['d']} names unknown member {mid}"
    assert n['ty'] in {t['id'] for t in d['types']}, f"unknown type {n['ty']}"
    assert re.match(r'^\d{4}-\d{2}-\d{2}$', n['d']), f"bad date {n['d']}"
segs = {s['id'] for s in d['segments']}
for m in d['members']:
    assert m['s'] in segs, f"member {m['id']} has unknown segment {m['s']}"

dump = lambda v: json.dumps(v, ensure_ascii=False)
parts = []
keys = list(d.keys())
for i, k in enumerate(keys):
    v = d[k]; end = ',' if i < len(keys) - 1 else ''
    if isinstance(v, list):
        parts.append(f'  {dump(k)}: [\n' + ',\n'.join(f'    {dump(x)}' for x in v) + f'\n  ]{end}')
    else:
        parts.append(f'  {dump(k)}: {dump(v)}{end}')
body = ('{\n' + '\n'.join(parts) + '\n}').replace('</', '<\\/')
html = open(TPL, encoding='utf-8').read().replace('/*__DATA__*/', body)
open(out, 'w', encoding='utf-8').write(html)
print(out, len(html), 'members', len(d['members']), 'news', len(d['news']), 'events', len(d['events']))
