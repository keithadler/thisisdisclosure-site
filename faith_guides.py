"""Guides by tradition: where a tradition's own texts already hold related ideas, with verified public-domain quotations."""
import html, json, os, glob
from cheat_pages import STYLE as CS_STYLE

E = lambda s: html.escape(s, quote=True)
ORDER = ["christianity", "islam", "atheist", "nonspecific", "hinduism", "buddhism", "sikhism", "judaism", "taoism", "bahai", "jainism",
         "shinto", "zoroastrianism", "unitarian", "confucianism", "sufism", "ubuntu"]  # largest first by the estimates in content/faith_followers.json; the last three have no reliable count
ART = {"judaism": "bread", "christianity": "comfort", "islam": "market", "sufism": "midnight", "hinduism": "road",
       "buddhism": "elder", "jainism": "hands", "sikhism": "bridge", "bahai": "library", "zoroastrianism": "dawn",
       "taoism": "runner", "confucianism": "courtroom", "shinto": "face", "ubuntu": "finish", "unitarian": "rooms", "atheist": "lab", "nonspecific": "porch"}
ALT = "A quiet scene of people helping one another."

STYLE = CS_STYLE.replace("</style>", """
.fgq{margin:1.2rem 0;padding:1.1rem 1.3rem;border-left:4px solid var(--ink);background:var(--card);border-radius:0 12px 12px 0}
.fgq blockquote{margin:0;font:600 clamp(1.15rem,3.6vw,1.45rem)/1.4 "Playfair Display",Georgia,serif}
.fgq cite{display:block;margin-top:.5rem;font:700 .74rem ui-monospace,Menlo,monospace;letter-spacing:.1em;text-transform:uppercase;font-style:normal;opacity:.75}
.fgq cite a{color:inherit}
.fgh{margin:2.4rem 0 .6rem;font-size:clamp(1.5rem,5vw,2rem)}
.fgask li{margin:.5em 0}
.fgnote{margin:1.6rem 0;padding:1rem 1.2rem;border:2px solid var(--ink);border-radius:12px;font-size:.95rem}
@media print{.fgq{background:none;break-inside:avoid}.fgsrc{display:none}}
</style>""")

def followers():
    try: return {e["slug"]: e for e in json.load(open("content/faith_followers.json"))["entries"]}
    except OSError: return {}

def _fol(slug, long=False):
    e = followers().get(slug)
    if not e: return ""
    disp = e["display"][0].upper() + e["display"][1:]
    if e.get("estimate"):
        tail = '' if any(w in disp for w in ('(', 'members', 'self-identified')) else ' people worldwide'
        txt = f'{disp}{tail}' + (f' ({e["year"]})' if e.get("year") else '')
    else:
        txt = disp
    if long and e.get("source_url"):
        txt += f' &middot; <a href="{E(e["source_url"])}" target="_blank" rel="noopener">{E(e["publisher"])}</a>'
        txt += f' &middot; {E(e["solidity"])}'
    return E(txt) if not long else txt.replace(E(e["display"][0].upper()+e["display"][1:]), E(e["display"][0].upper()+e["display"][1:]), 1)

def load():
    out = {}
    for f in glob.glob("content/faith/*.json"):
        d = json.load(open(f))
        out[d["slug"]] = d
    return {s: out[s] for s in ORDER if s in out}

def page(slug, d, pic, all_):
    steps = "".join(f'<li class="csstep"><div class="csdo">{E(p["do"])}</div><div class="cshow">{E(p["how"])}</div></li>' for p in d["practices"])
    quotes = "".join(
        f'<div class="fgq"><blockquote>&ldquo;{"&hellip;" if p["text"][:1].islower() else ""}{E(p["text"])}&rdquo;</blockquote><cite>{E(p["ref"])} &middot; {E(p["translation"])} &middot; <a href="{E(p["url"])}" target="_blank" rel="noopener">read it in context</a></cite></div>'
        for p in d["passages"])
    ask = "".join(f"<li>{E(q)}</li>" for q in d["ask"])
    src = "".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener"><b>{E(s["title"])}</b><span>{E(s["publisher"])}</span></a>' for s in d["sources"])
    others = "".join(f'<a href="/guide-{s}">{E(v["name"])}</a>' for s, v in all_.items() if s != slug)
    return (STYLE + '<div class="csw"><div class="cseye">Guide &middot; ' + E(d["name"]) + '</div>'
            f'<div class="csnote noprint" style="margin:-.4rem 0 1rem">{_fol(slug, True)}</div>'
            f'<h1 class="cstitle">A guide for {E(d["who"][0].lower() + d["who"][1:] if d["who"].startswith("People") else d["who"])}.</h1>'
            f'<p class="cslede">{E(d["idea"])}</p>'
            f'<div class="cshero">{pic("fg_" + slug, True, True, E(ALT), True)}</div>'
            + ('<h2 class="fgh">In your own tradition</h2>' + quotes if quotes else '') +
            '<h2 class="fgh">Five things to do this week</h2>'
            f'<ol class="cssteps">{steps}</ol>'
            '<h2 class="fgh">Questions to bring to your own teacher</h2>'
            f'<ul class="fgask">{ask}</ul>'
            f'<div class="fgnote"><b>What this guide is not claiming.</b> {E(d["caveat"])} I am not a scholar of your tradition, and no tradition or its leaders have endorsed this site. Ask your own teachers and community what these passages mean to them.</div>'
            '<div class="csonly cs-print-foot">thisisdisclosure.com/faith-guides &middot; For adults, 18 and over &middot; Share freely</div>'
            '<div class="fgsrc"><h2 class="fgh">Read more</h2><div class="pwl">' + src + '</div></div>'
            f'<div class="csbar noprint"><a class="pr" href="/pdf/guide-{slug}.pdf" download>Download PDF</a><button type="button" onclick="window.print()">Print</button><a href="/faith-guides">All guides</a><a href="/cheat-sheets">Cheat sheets</a></div>'
            f'<div class="csmore noprint"><b>More:</b> {others}</div></div>')

def hub(all_, pic):
    cards = "".join(
        f'<a class="cscard" href="/guide-{s}">' + pic("fg_" + s, True, True, E(ALT)) +
        f'<div class="cb"><div class="ck">Guide &middot; {_fol(s)}</div><b>{E(d["name"])}</b><span class="d">{E(d["idea"][:150].rsplit(" ", 1)[0])}...</span><span class="go">Open the guide</span></div></a>'
        for s, d in all_.items())
    pdfs = "".join(f'<a href="/pdf/guide-{s}.pdf" download><span>{E(d["name"])}</span><i>PDF</i></a>' for s, d in all_.items())
    return (STYLE + '<div class="csw"><div class="cseye">By tradition</div><h1 class="cstitle">Guides by tradition.</h1>'
            '<p class="cslede">Many traditions already hold ideas close to this one: that what you do for strangers, unseen and for nothing, matters most. Find yours and see it in your own texts, in your own words.</p>'
            '<p class="csnote">These guides do not say a religion agrees with me. They point to the tradition\'s own public-domain texts and teaching so you can judge for yourself. If your tradition is missing, tell me at keith at thisisdisclosure dot com and I will research it with the same rules.</p>'
            f'<div class="csgrid">{cards}</div><h2>Download as PDF</h2><div class="cgpdf">{pdfs}</div></div>')
