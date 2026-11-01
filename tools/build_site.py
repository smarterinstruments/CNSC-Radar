"""Prototype of the multi-page CNSC website built from the radar's data.

Usage: python3 tools/build_site.py <out_dir>

Reuses the radar template (tools/template.html): its CSS and its rendering code (member cards with offers,
news items, events, centres) are extracted verbatim, so the pages look and behave like the radar. Page
texts live in tools/site/texts.json (cs/en). Yellow ".todo" boxes mark texts the cluster has to supply.

Output: <out_dir>/index.html (a fragment, published as the artifact page), the other pages as full HTML
documents, plus shared site.css, site.js and data.js.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'site')
os.makedirs(out, exist_ok=True)

def load(name):
    with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
        return json.load(f)

tax = load('taxonomy.json')
D = {"meta": load('meta.json'), **tax, "members": load('members.json'),
     "centres": load('centres.json'), "news": load('news.json'), "events": load('events.json'), "sources": load('sources.json')}
TX = json.load(open(os.path.join(ROOT, 'tools', 'site', 'texts.json'), encoding='utf-8'))
tpl = open(os.path.join(ROOT, 'tools', 'template.html'), encoding='utf-8').read()

css = re.search(r'<style>\n(.*?)</style>', tpl, re.S).group(1)
app = tpl.split('<script>\n', 1)[1].split('\nrenderAll();', 1)[0]
# the app code reads the data from the page; here it comes from data.js
app = app.replace("const D = JSON.parse(document.getElementById('radar-data').textContent.replace(/<\\\\\\//g, '</'));", "const D = window.RADAR_DATA;")
assert 'window.RADAR_DATA' in app, 'data hook not replaced'
# elements of panels that are not on this page: write into a detached node instead of throwing
app = app.replace("const $ = id => document.getElementById(id);",
                  "const _void = document.createElement('div');\nconst $ = id => document.getElementById(id) || _void;")
app = app.replace("try { LANG = localStorage.getItem('cnsc-radar-lang') === 'en' ? 'en' : 'cs'; } catch (e) {}",
                  "try { LANG = localStorage.getItem('cnsc-site-lang') === 'en' ? 'en' : 'cs'; } catch (e) {}")
app = app.replace("function setLang(l) { LANG = l; try { localStorage.setItem('cnsc-radar-lang', l); } catch (e) {} renderAll(); }",
                  "function setLang(l) { LANG = l; try { localStorage.setItem('cnsc-site-lang', l); } catch (e) {} renderAll(); }")

site_css = css + r"""
/* ---- site chrome (prototype) ---- */
.sitehead{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.sitehead .hd{display:flex;align-items:center;gap:18px;height:66px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
.brand .mark{width:34px;height:34px;border-radius:8px;background:var(--blue);display:grid;place-items:center;color:#fff;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:13px;letter-spacing:.04em}
.brand .nm{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:14px;line-height:1.15}
.brand .sb{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
nav.site{display:flex;gap:4px;flex-wrap:wrap;margin-left:auto}
nav.site a{font-size:13px;font-weight:500;color:var(--muted);text-decoration:none;padding:7px 9px;border-radius:8px;white-space:nowrap}
nav.site a:hover{color:var(--blue);background:var(--panel)}
nav.site a.on{color:var(--blue);background:var(--blue-soft)}
.sitehead .lang{margin-left:6px}
.proto{background:var(--warn-bg);color:var(--warn);font-family:"IBM Plex Mono",monospace;font-size:11.5px;padding:7px 0;border-bottom:1px solid var(--line)}
.todo{background:var(--warn-bg);border:1px dashed var(--warn);border-radius:10px;padding:10px 14px;margin:14px 0;font-size:13px;color:var(--ink)}
.todo b{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--warn);display:block;margin-bottom:3px}
.page{padding:28px 0 40px}
.page h1{font-size:clamp(28px,4vw,40px);line-height:1.08;margin-bottom:8px}
.page>.sub,.page .sub{color:var(--muted);max-width:76ch}
.home-hero{padding:44px 0 26px;display:grid;grid-template-columns:1.2fr .8fr;gap:30px;align-items:end}
.home-hero h1{font-size:clamp(34px,5.2vw,58px);line-height:1.04;max-width:16ch}
.home-hero h1 .sheen{background:linear-gradient(100deg,#3FB0E8,#0066B5 55%,#123C6E);-webkit-background-clip:text;background-clip:text;color:transparent}
.home-hero .lead{margin-top:18px;font-size:16px;color:var(--muted);max-width:60ch}
.cta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:22px 0 10px}
.cta a{display:block;background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--ink)}
.cta a b{display:block;font-family:"Space Grotesk",sans-serif;font-size:15.5px;margin-bottom:4px}
.cta a span{font-size:13px;color:var(--muted)}
.cta a:hover{border-color:var(--blue)}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.svc{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;min-width:0}
.svc h3{font-size:16px;margin-bottom:6px}
.svc p{font-size:13.5px;color:var(--muted)}
.svc .lk{display:inline-block;margin-top:10px;font-family:"IBM Plex Mono",monospace;font-size:12px}
.facts{display:grid;grid-template-columns:180px 1fr;gap:6px 18px;font-size:14px;margin:10px 0 18px}
.facts dt{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding-top:3px}
.facts dd{margin:0}
.search{display:flex;align-items:center;gap:10px;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:9px 16px;max-width:520px;margin:14px 0 18px}
.search input{border:0;outline:0;background:transparent;font:inherit;font-size:14px;width:100%;color:var(--ink)}
.sec{margin-top:34px}
.sec h2{font-size:22px;margin-bottom:6px}
footer.site{border-top:1px solid var(--line);padding:26px 0 40px;font-size:12.5px;color:var(--muted)}
footer.site .row{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:900px){.home-hero,.cta,.grid3{grid-template-columns:1fr}.grid2{grid-template-columns:1fr}.facts{grid-template-columns:1fr}nav.site{display:none}}
"""

site_js = app + r"""

// ---- site layer (prototype) ----
const S = window.SITE_TEXTS;
const PAGE = document.body.dataset.page;
// cross-page navigation for links the radar code binds (member cards, centre cards)
const PAGE_OF = {members: 'clenove.html', centres: 'centra.html', news: 'novinky.html', events: 'akce.html'};
function showTab(id) { const p = PAGE_OF[id]; if (p && !document.getElementById('p-' + id)) { const h = (event && event.currentTarget && event.currentTarget.getAttribute('href')) || ''; location.href = p + (h.startsWith('#') ? h : ''); } }
const todo = t => t ? `<div class="todo"><b>${esc(L(S.todoLabel))}</b>${esc(L(t))}</div>` : '';
const sec = (h, inner) => `<section class="sec"><h2>${esc(L(h))}</h2>${inner}</section>`;

function renderChrome() {
  document.documentElement.lang = LANG;
  $('nav').innerHTML = S.nav.map(([href, label, id]) => `<a href="${href}" class="${id === PAGE ? 'on' : ''}">${esc(L(label))}</a>`).join('');
  $('brandNm').textContent = L(S.brand); $('brandSb').textContent = L(S.brandSub);
  $('proto').textContent = L(S.proto); $('footNote').textContent = L(S.footerNote);
  document.querySelectorAll('.lang button').forEach(b => b.classList.toggle('on', b.dataset.l === LANG));
}

function renderHome() {
  const h = S.home;
  $('heroEyebrow').textContent = L(h.eyebrow);
  $('heroH1').innerHTML = `${esc(L(h.h1a))}<br><span class="sheen">${esc(L(h.h1b))}</span><br>${esc(L(h.h1c))}`;
  $('heroLead').textContent = L(h.lead);
  const month = D.members.filter(m => ringOf(m.id) <= 2).length;
  const vals = [D.members.length, D.segments.length, (D.centres || []).length, month];
  $('homeStats').innerHTML = h.tiles.map(([l, s], i) => `<div class="st"><div class="v">${vals[i]}</div><div class="l">${esc(L(l))}</div><div class="s">${esc(L(s))}</div></div>`).join('');
  $('cta').innerHTML = h.cta.map(([href, b, s]) => `<a href="${href}"><b>${esc(L(b))}</b><span>${esc(L(s))}</span></a>`).join('');
  $('topH').textContent = L(h.topH); $('topSub').textContent = L(h.topSub); $('evH').textContent = L(h.evH);
  renderTop(); renderEvents();
}
function renderMembersPage() {
  renderMembers();
  $('memH').textContent = L(S.members.h); $('memSub').textContent = L(S.members.sub);
  $('memTodo').innerHTML = todo(S.members.todo);
  const inp = $('q');
  inp.placeholder = L(S.members.search);
  inp.oninput = () => { const q = inp.value.trim().toLowerCase();
    document.querySelectorAll('#memberList .card').forEach(c => c.style.display = !q || c.textContent.toLowerCase().includes(q) ? '' : 'none');
    document.querySelectorAll('#memberList .stage').forEach(s => s.style.display = [...s.querySelectorAll('.card')].some(c => c.style.display !== 'none') ? '' : 'none'); };
}
function renderCentresPage() {
  renderCentres();
  const c = S.centres;
  $('projH').textContent = L(c.projH); $('projSub').textContent = L(c.projSub);
  $('projList').innerHTML = c.projects.map(([n, p, u, t]) => `<div class="svc"><h3>${esc(L(n))}</h3><p>${esc(L(p))}</p>${u ? `<a class="lk" href="${esc(u)}" target="_blank" rel="noopener">${esc(T().web)} ↗</a>` : ''}${todo(t)}</div>`).join('');
}
function renderServices() {
  const s = S.services;
  $('h1').textContent = L(s.h); $('sub').textContent = L(s.sub);
  $('svcList').innerHTML = s.items.map(([n, p]) => `<div class="svc"><h3>${esc(L(n))}</h3><p>${esc(L(p))}</p></div>`).join('');
  $('catH').textContent = L(s.catH);
  $('catList').innerHTML = s.cats.map(([n, p]) => `<div class="svc"><h3>${esc(L(n))}</h3><p>${esc(L(p))}</p></div>`).join('');
  $('svcTodo').innerHTML = todo(s.todo);
}
function renderRadars() {
  const r = S.radars;
  $('h1').textContent = L(r.h); $('sub').textContent = L(r.sub);
  $('radList').innerHTML = r.items.map(([n, p, u]) => `<div class="svc"><h3>${esc(L(n))}</h3><p>${esc(L(p))}</p><a class="lk" href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace('https://',''))} ↗</a></div>`).join('');
  $('radTodo').innerHTML = todo(r.todo);
}
function renderAboutPage() {
  const a = S.about;
  $('h1').textContent = L(a.h); $('mission').textContent = L(a.mission);
  $('facts').innerHTML = a.facts.map(([k, v]) => `<dt>${esc(L(k))}</dt><dd>${esc(L(v))}</dd>`).join('');
  $('bodiesH').textContent = L(a.bodiesH); $('bodies').textContent = L(a.bodies); $('bodiesTodo').innerHTML = todo(a.bodiesTodo);
  $('membH').textContent = L(a.membH); $('membTodo').innerHTML = todo(a.membTodo);
  $('docsH').textContent = L(a.docsH); $('docsTodo').innerHTML = todo(a.docsTodo);
}
function renderContact() {
  const c = S.contact;
  $('h1').textContent = L(c.h);
  $('facts').innerHTML = c.rows.map(([k, v]) => `<dt>${esc(L(k))}</dt><dd>${esc(L(v))}</dd>`).join('');
  $('cTodo').innerHTML = todo(c.todo);
}
function renderAll() {
  renderChrome(); renderStatic();
  if (PAGE === 'home') renderHome();
  if (PAGE === 'members') renderMembersPage();
  if (PAGE === 'centres') renderCentresPage();
  if (PAGE === 'news') { renderNews(); $('pgTodo').innerHTML = todo(S.news.todo); }
  if (PAGE === 'events') { renderEvents(); $('pgTodo').innerHTML = todo(S.events.todo); }
  if (PAGE === 'services') renderServices();
  if (PAGE === 'radars') renderRadars();
  if (PAGE === 'about') renderAboutPage();
  if (PAGE === 'contact') renderContact();
}
renderAll();
const hash = (location.hash || '').replace('#', '');
if (hash) { const el = document.getElementById(hash); if (el) setTimeout(() => el.scrollIntoView({block: 'center'}), 50); }
"""

head = """<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
"""
chrome_top = """<header class="sitehead"><div class="wrap hd">
  <a class="brand" href="./"><span class="mark">CZ</span><span><span class="nm" id="brandNm"></span><br><span class="sb" id="brandSb"></span></span></a>
  <nav class="site" id="nav"></nav>
  <div class="lang" role="group" aria-label="Language"><button data-l="cs" onclick="setLang('cs')">CZ</button><button data-l="en" onclick="setLang('en')">EN</button></div>
</div></header>
<div class="proto"><div class="wrap" id="proto"></div></div>
<main class="wrap">
"""
chrome_bottom = """</main>
<footer class="site"><div class="wrap row"><span id="footNote"></span><span class="mono">SILICON EUROPE · SEMI · EU CHIPS ACT</span></div></footer>
<script src="data.js"></script><script src="site.js"></script>
"""

pages = {
 'index.html': ('home', 'Czech National Semiconductor Cluster', 'Czech National Semiconductor Cluster: members, centres, news, events and services of the Czech semiconductor cluster.', """
<section class="home-hero"><div><div class="eyebrow" id="heroEyebrow"></div><h1 id="heroH1"></h1><p class="lead" id="heroLead"></p></div><div class="stats" id="homeStats" style="grid-template-columns:repeat(2,minmax(0,1fr));margin:0"></div></section>
<div class="cta" id="cta"></div>
<div class="top"><h2 id="topH"></h2><p class="sub" id="topSub"></p><div id="topList"></div></div>
<section class="sec"><h2 id="evH"></h2><div id="evList"></div></section>
"""),
 'clenove.html': ('members', 'Členové – CNSC', 'Members of the Czech National Semiconductor Cluster by value-chain segment, with their public offer.', """
<div class="page"><h1 id="memH"></h1><p class="sub" id="memSub"></p>
<label class="search"><input id="q" type="search" aria-label="Search"></label>
<div id="memTodo"></div><div id="memberList"></div></div>
"""),
 'centra.html': ('centres', 'Centra a projekty – CNSC', 'Centres led by cluster members and the cluster\'s projects and initiatives.', """
<div class="page"><h1 id="cenH"></h1><p class="sub" id="cenSub"></p><div id="centreList"></div>
<section class="sec"><h2 id="projH"></h2><p class="sub" id="projSub"></p><div class="grid2" id="projList" style="margin-top:14px"></div></section></div>
"""),
 'novinky.html': ('news', 'Novinky – CNSC', 'News log of the Czech National Semiconductor Cluster members.', """
<div class="page"><h1 id="newsH"></h1><p class="sub" id="newsSub"></p><div id="pgTodo"></div>
<div class="filters" id="filters"></div><p class="count" id="newsCount"></p><div id="newsList"></div></div>
"""),
 'akce.html': ('events', 'Akce – CNSC', 'Upcoming events and deadlines of the Czech semiconductor ecosystem.', """
<div class="page"><h1 id="evH"></h1><p class="sub" id="evSub"></p><div id="pgTodo"></div><div id="evList"></div></div>
"""),
 'sluzby.html': ('services', 'Služby klastru – CNSC', 'Services of the Czech National Semiconductor Cluster.', """
<div class="page"><h1 id="h1"></h1><p class="sub" id="sub"></p><div class="grid3" id="svcList" style="margin-top:18px"></div>
<section class="sec"><h2 id="catH"></h2><div class="grid2" id="catList"></div></section><div id="svcTodo"></div></div>
"""),
 'radary.html': ('radars', 'Radary – CNSC', 'Weekly radars compiled by the Czech National Semiconductor Cluster.', """
<div class="page"><h1 id="h1"></h1><p class="sub" id="sub"></p><div class="grid3" id="radList" style="margin-top:18px"></div><div id="radTodo"></div></div>
"""),
 'o-klastru.html': ('about', 'O klastru – CNSC', 'About the Czech National Semiconductor Cluster: mission, facts, governing bodies, membership, documents.', """
<div class="page"><h1 id="h1"></h1><p class="sub" id="mission" style="font-size:16px"></p><dl class="facts" id="facts"></dl>
<section class="sec"><h2 id="bodiesH"></h2><p id="bodies" style="font-size:14.5px"></p><div id="bodiesTodo"></div></section>
<section class="sec" id="clenstvi"><h2 id="membH"></h2><div id="membTodo"></div></section>
<section class="sec"><h2 id="docsH"></h2><div id="docsTodo"></div></section></div>
"""),
 'kontakt.html': ('contact', 'Kontakt – CNSC', 'Contact the Czech National Semiconductor Cluster.', """
<div class="page"><h1 id="h1"></h1><dl class="facts" id="facts"></dl><div id="cTodo"></div></div>
"""),
}

dump = lambda v: json.dumps(v, ensure_ascii=False)
open(os.path.join(out, 'data.js'), 'w', encoding='utf-8').write('window.RADAR_DATA = ' + dump(D).replace('</', '<\\/') + ';\nwindow.SITE_TEXTS = ' + dump(TX).replace('</', '<\\/') + ';\n')
open(os.path.join(out, 'site.css'), 'w', encoding='utf-8').write(site_css)
open(os.path.join(out, 'site.js'), 'w', encoding='utf-8').write(site_js)
for fn, (pid, title, desc, body) in pages.items():
    inner = head.format(title=title, desc=desc) + chrome_top + body + chrome_bottom
    if fn == 'index.html':
        # the artifact page is a fragment; the publisher adds the document skeleton
        html = inner.replace('<main class="wrap">', f'<main class="wrap" data-page="{pid}">')
        html = html.replace('<script src="data.js"></script><script src="site.js"></script>',
                            f'<script>document.body.dataset.page="{pid}";</script><script src="data.js"></script><script src="site.js"></script>')
    else:
        html = ('<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                + head.format(title=title, desc=desc) + f'</head><body data-page="{pid}">\n' + chrome_top + body + chrome_bottom + '</body></html>')
    open(os.path.join(out, fn), 'w', encoding='utf-8').write(html)
print(out, 'pages', len(pages), 'members', len(D['members']), 'news', len(D['news']), 'centres', len(D['centres']))
