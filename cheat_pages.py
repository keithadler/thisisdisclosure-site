"""Cheat sheet pages and hub: poster-style one-pagers with a woodcut header, big numerals and pull-quote 'say' lines."""
import html, re, json, os

E = lambda s: html.escape(s, quote=True)
ART = {"everyone": "cs_everyone", "everyday": "cs_everyday", "elders": "cs_elders", "teens": "cs_teens", "parents": "cs_parents",
       "leaders": "cs_leaders", "inside": "cs_inside", "fallen": "cs_fallen", "meaning": "cs_meaning"}
ALT = {"everyone": "Strangers helping one another on a busy street.", "everyday": "A young man carries an older woman's groceries up the steps.",
       "elders": "A grandparent and a child look up at the Milky Way from a rooftop.", "teens": "Students and a teacher in a classroom, hands raised.",
       "parents": "A parent kneels to listen to a child.", "leaders": "A woman lays out plans for a table of colleagues.",
       "inside": "A man walks down a long hallway toward the light.", "fallen": "A man sits on a porch looking over his town at dusk.",
       "meaning": "A woman and a child climb a path up a hillside."}

STYLE = """<style>
.csw{width:min(1000px,calc(100vw - 44px));position:relative;left:50%;transform:translateX(-50%)}
.cseye{font:700 .72rem ui-monospace,Menlo,monospace;letter-spacing:.26em;text-transform:uppercase;opacity:.7;margin-bottom:.8rem}
.cstitle{font-size:clamp(2.4rem,9vw,4.6rem);line-height:.98;margin:0 0 .35em}
.cslede{font-size:1.2rem;max-width:36em;margin:0 0 1.6rem}
.cshero img{display:block;width:100%;height:auto;max-height:min(48vh,430px);object-fit:cover;object-position:center 35%;border:1px solid var(--ink)}
.cssteps{list-style:none;margin:2.4rem 0;padding:0;counter-reset:s}
.csstep{display:grid;grid-template-columns:3.6rem 1fr;gap:0 1rem;padding:1.3rem 0;border-top:1px solid color-mix(in srgb,var(--ink) 28%,transparent);counter-increment:s;break-inside:avoid}
.csstep:last-child{border-bottom:1px solid color-mix(in srgb,var(--ink) 28%,transparent)}
.csstep::before{content:counter(s);font:900 3.4rem/.9 "Playfair Display",Georgia,serif;grid-row:1/3}
.csdo{font:800 clamp(1.2rem,3.4vw,1.5rem)/1.2 "Playfair Display",Georgia,serif}
.cshow{margin-top:.4rem;font-size:1.05rem;max-width:40em}
.cssay{margin:.7rem 0 0;padding:.7rem .95rem;background:var(--ink);color:var(--bone);border-radius:8px;font:600 1rem/1.4 ui-monospace,Menlo,monospace}
.cssay b{display:block;font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;opacity:.6;margin-bottom:.2rem}
.csweek{margin:2.4rem 0;padding:1.6rem 1.5rem;background:var(--ink);color:var(--bone);border-radius:14px}
.csweek small{display:block;font:700 .68rem ui-monospace,Menlo,monospace;letter-spacing:.26em;text-transform:uppercase;opacity:.6;margin-bottom:.6rem}
.csweek div{font:800 clamp(1.5rem,5vw,2.2rem)/1.15 "Playfair Display",Georgia,serif}
.csnote{font-size:.95rem;opacity:.85;margin:1rem 0}
.csbar{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.6rem 0}
.csbar a,.csbar button{font:700 .78rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:inherit;border:2px solid var(--ink);background:transparent;padding:.65em 1em;border-radius:999px;cursor:pointer}
.csbar .pr{background:var(--ink);color:var(--bone)}
.csbar a:hover,.csbar button:hover{background:var(--ink);color:var(--bone)}
.csmore{margin:2rem 0 0;font-size:.95rem}.csmore a{margin-right:.9em}
.csgrid{display:grid;grid-template-columns:1fr;gap:1.4rem;margin:2rem 0}
@media (min-width:700px){.csgrid{grid-template-columns:1fr 1fr}.csgrid .big{grid-column:1/-1;display:grid;grid-template-columns:1.1fr 1fr;align-items:center}}
.cscard{display:block;text-decoration:none;color:inherit;border:2px solid var(--ink);border-radius:14px;overflow:hidden;background:var(--card);transition:transform .25s ease,box-shadow .25s ease}
.cscard:hover{transform:translateY(-3px);box-shadow:0 16px 30px -16px rgba(0,0,0,.55)}
.cscard img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover}
.cscard .cb{padding:1.1rem 1.2rem 1.3rem}
.cscard .ck{font:700 .64rem ui-monospace,Menlo,monospace;letter-spacing:.24em;text-transform:uppercase;opacity:.6}
.cscard b{display:block;font:800 1.45rem/1.15 "Playfair Display",Georgia,serif;margin:.3rem 0 .4rem}
.cscard span.d{display:block;font-size:.95rem;opacity:.85}
.cscard .go{display:inline-block;margin-top:.8rem;font:700 .74rem ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;border-bottom:2px solid var(--ink)}
.cscard.big b{font-size:1.9rem}
.cev{margin:2.6rem 0 1rem}
.cev h2{font-size:clamp(1.5rem,5vw,2.1rem);margin:0 0 .3em}
.cev .ci{font-size:1.05rem;max-width:42em}
.cevl{display:grid;gap:.7rem;margin:1.2rem 0}
.cevl a{display:block;text-decoration:none;color:inherit;border:2px solid var(--ink);border-radius:12px;padding:.9rem 1.1rem;background:var(--card);transition:transform .2s,box-shadow .2s}
.cevl a:hover{transform:translateY(-2px);box-shadow:0 12px 24px -14px rgba(0,0,0,.55)}
.cevl b{display:block;font:800 1.08rem/1.25 "Playfair Display",Georgia,serif}
.cevl span{display:block;font-size:.95rem;opacity:.85;margin-top:.25rem}
.cevl i{font-style:normal;font:700 .62rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.6;display:block;margin-top:.4rem}
.cevl a.skeptical{border-style:dashed}
.cev .lim{border-left:4px solid var(--ink);padding:.2rem 0 .2rem 1rem;margin-top:1rem;font-size:.97rem}
.cgpdf{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:0 1.6rem;margin:1rem 0 2rem}
.cgpdf a{display:flex;justify-content:space-between;align-items:baseline;text-decoration:none;color:inherit;padding:.6rem .1rem;border-bottom:1px solid color-mix(in srgb,var(--ink) 22%,transparent);font-size:1rem}
.cgpdf a:hover{border-bottom-color:var(--ink)}
.cgpdf i{font:700 .6rem ui-monospace,Menlo,monospace;letter-spacing:.2em;opacity:.55;font-style:normal}
.cgfind{width:100%;max-width:26rem;box-sizing:border-box;font:500 1.05rem "Playfair Display",Georgia,serif;color:var(--ink);background:var(--card);border:2px solid color-mix(in srgb,var(--ink) 45%,transparent);border-radius:999px;padding:.7rem 1.1rem;margin:.4rem 0 1rem}
.cgfind:focus{outline:3px solid var(--ink);outline-offset:2px;border-color:var(--ink)}
.cscard[hidden]{display:none}
@page{size:Letter;margin:.5in}
.csonly{display:none}
@media print{
html,body{background:#fff!important;color:#000}
.noprint,.csbar,.csmore,.cev{display:none!important}
.csonly{display:block}
.csw{width:auto;left:0;transform:none;zoom:.76}
.cseye{font-size:8pt;margin-bottom:4pt}
.cstitle{font-size:23pt;margin:0 0 3pt}
.cslede{font-size:10.5pt;margin:0 0 8pt;max-width:none}
.cshero img{max-height:1.15in;border:1pt solid #000}
.cssteps{margin:8pt 0}
.csstep{display:grid;grid-template-columns:.3in 1fr;gap:0 8pt;padding:3.5pt 0;border-top:.5pt solid #999}
.csstep:last-child{border-bottom:.5pt solid #999}
.csstep::before{content:"";width:.2in;height:.2in;border:1.5pt solid #000;border-radius:3pt;margin-top:2pt;grid-row:1/3}
.csdo{font-size:11.5pt}
.cshow{font-size:9pt;margin-top:1pt}
.cssay{background:none!important;color:#000!important;border:1pt solid #000;border-radius:4pt;padding:2pt 6pt;margin-top:2pt;font-size:8.5pt}.cssay b{display:inline;margin-right:6pt}
.csweek{background:none!important;color:#000!important;border:2pt solid #000;border-radius:6pt;padding:6pt 10pt;margin:6pt 0}
.csweek div{font-size:13pt}
.csnote{font-size:8.5pt;margin:4pt 0}
.cs-print-foot{font:700 8pt ui-monospace,Menlo,monospace;letter-spacing:.1em;text-transform:uppercase;margin-top:8pt}
}
</style>"""

def _how(how):
    """Split a 'Say: "..."' line out of the how-text so it can stand as a pull quote."""
    m = re.search(r'\s*(Say|Ask|Write|Text|Message them|Tell them): ?(".*?"|“.*?”)(?:\s|$)', how)
    if not m:
        return E(how), ""
    before, after = how[:m.start()].strip(), how[m.end():].strip()
    text = (before + (" " if before and after else "") + after).strip()
    return E(text), f'<div class="cssay"><b>{m.group(1)}</b>{E(m.group(2))}</div>'

def _evidence(slug):
    p = f"content/cheat_evidence/{slug}.json"
    if not os.path.exists(p): return ""
    d = json.load(open(p))
    cards = "".join(
        f'<a class="{E(i["kind"])}" href="{E(i["url"])}" target="_blank" rel="noopener"><b>{E(i["title"])}</b><span>{E(i["finding"])}</span><i>{E(i["kind"])} &middot; {E(i["publisher"])}</i></a>'
        for i in d["items"])
    return ('<div class="cev noprint"><h2>The evidence behind this sheet</h2>'
            f'<p class="ci">{E(d["intro"])}</p><div class="cevl">{cards}</div>'
            f'<div class="lim"><b>Where the evidence is thin.</b> {E(d["limits"])}</div></div>')

def sheet(slug, vals, pic, order):
    tab, title, lede, items, week, note = vals
    steps = ""
    for d, w in items:
        txt, say = _how(w)
        steps += f'<li class="csstep"><div class="csdo">{E(d)}</div><div class="cshow">{txt}{say}</div></li>'
    others = "".join(f'<a href="/cheat-sheet-{s}">{E(v[0])}</a>' for s, v in order.items() if s != slug)
    return (STYLE + '<div class="csw"><div class="cseye">Cheat sheet &middot; ' + E(tab) + '</div>'
            f'<h1 class="cstitle">{E(title)}.</h1><p class="cslede">{E(lede)}</p>'
            f'<div class="cshero">{pic(ART[slug], True, True, E(ALT[slug]), True)}</div>'
            f'<ol class="cssteps">{steps}</ol>'
            + _evidence(slug) +
            f'<div class="csweek"><small>If you only do one thing this week</small><div>{E(week)}</div></div>'
            + (f'<p class="csnote">{E(note)}</p>' if note else '') +
            '<p class="csnote">This is practical, not religious. I think what you show with your choices is what counts. Share it freely.</p>'
            '<div class="csonly cs-print-foot">thisisdisclosure.com/cheat-sheets &middot; For adults, 18 and over &middot; Share freely</div>'
            f'<div class="csbar noprint"><a class="pr" href="/pdf/cheat-sheet-{slug}.pdf" download>Download PDF</a><button type="button" onclick="window.print()">Print</button><a href="/cheat-sheets">All cheat sheets</a><a href="/how-to-cheat-on-the-test">The one question</a></div>'
            f'<div class="csmore noprint"><b>More:</b> {others}</div></div>')

def hub(order, pic):
    cards = ('<a class="cscard big" href="/how-to-cheat-on-the-test">' + pic(ART["everyone"], True, True, E(ALT["everyone"])) +
             '<div class="cb"><div class="ck">For everyone</div><b>The one question</b><span class="d">The whole answer key in a minute: <em>Is this what a human being does?</em></span><span class="go">Read it</span></div></a>')
    for s, v in order.items():
        cards += (f'<a class="cscard" href="/cheat-sheet-{s}">' + pic(ART[s], True, True, E(ALT[s])) +
                  f'<div class="cb"><div class="ck">{E(v[0])}</div><b>{E(v[1])}</b><span class="d">{E(v[2])}</span><span class="go">Open the sheet</span></div></a>')
    return (STYLE + '<div class="csw"><div class="cseye">Take one</div><h1 class="cstitle">Cheat sheets.</h1>'
            '<p class="cslede">If you only do one thing, take my cheat sheet. Pick the one that sounds most like you. Each is one page of plain, doable things, with nothing to believe first.</p>'
            f'<div class="csgrid">{cards}</div>'
            '<p class="csnote">Looking for your own tradition? <a href="/faith-guides">Guides by tradition</a> show where many faiths already hold this idea, in their own texts.</p>'
            '<h2>Download as PDF</h2><p class="csnote">Print them, pin them up, hand them out.</p><div class="cgpdf">'
            + ''.join(f'<a href="/pdf/cheat-sheet-{s}.pdf" download><span>{E(v[0])}</span><i>PDF</i></a>' for s, v in order.items()) + '</div></div>')
