"""Country guides: what each government and legal system actually does that supports or promotes helping strangers."""
import html, json, glob
from cheat_pages import STYLE as CS_STYLE

E = lambda s: html.escape(s, quote=True)
ORDER = ["usa", "canada", "uk", "australia", "france", "germany", "netherlands", "israel", "japan", "china", "india",
         "singapore", "uae", "rwanda", "southafrica", "brazil"]
ART = "grace"
STATUS = {"none": "No general duty found", "limited": "Limited", "yes": "Yes", "varies": "Varies by region"}

STYLE = CS_STYLE.replace("</style>", """
.cgb{margin:1.4rem 0;padding:1.2rem 1.3rem;border:2px solid var(--ink);border-radius:14px;background:var(--card)}
.cgb h2{margin:0 0 .4rem;font-size:clamp(1.3rem,4vw,1.7rem)}
.cgs{display:inline-block;font:700 .66rem ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;background:var(--ink);color:var(--bone);padding:.3em .7em;border-radius:999px;margin-bottom:.6rem}
.cgb p{margin:.3rem 0}
.cgsrc{margin:.6rem 0 0;font-size:.88rem}.cgsrc a{margin-right:.9em}
.cgp{display:grid;gap:.7rem;margin:.8rem 0}
.cgp a{display:block;text-decoration:none;color:inherit;border:2px solid var(--ink);border-radius:12px;padding:.85rem 1rem;background:var(--card2)}
.cgp a:hover{box-shadow:0 12px 24px -14px rgba(0,0,0,.55)}
.cgp b{display:block;font:800 1.08rem/1.25 "Playfair Display",Georgia,serif}
.cgp span{display:block;font-size:.95rem;opacity:.85;margin-top:.2rem}
.cgp i{font-style:normal;font:700 .62rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.6;display:block;margin-top:.4rem}
@media print{.cgb{background:none;break-inside:avoid}}
</style>""")

import re as _re
def _fix(x):
    """The research notes were written in the first person by the researcher; keep the guides in a neutral voice."""
    if isinstance(x, dict): return {k: _fix(v) for k, v in x.items()}
    if isinstance(x, list): return [_fix(v) for v in x]
    if not isinstance(x, str): return x
    x = _re.sub(r"I found no (.+?) in the sources I (?:opened|could open|reviewed|checked)", r"No \1 was found in the sources reviewed", x)
    x = x.replace("I found no ", "No ").replace("I could not ", "It was not possible to ").replace("I did not ", "This guide did not ")
    x = x.replace("the translation here is mine", "the translation here is this guide's own").replace("my own translation", "this guide's own translation").replace("is my translation", "is this guide's own translation")
    for a, b in [("my own English renderings", "this guide's own English renderings"), ("my renderings", "this guide's renderings"), ("are my own", "are this guide's own"),
                 ("my own", "this guide's own"), ("the version I fetched", "the version consulted"), ("the sources I could verify", "the sources that could be verified"),
                 ("source I could open", "source that could be opened"), ("I relied on", "This guide relied on"), ("I read the 2018 Gazette text and did not check", "The 2018 Gazette text was read, and the guide did not check"),
                 ("the official PDF I read", "the official PDF consulted"), ("is mine", "is this guide's own"), ("I read ", "The guide read ")]:
        x = x.replace(a, b)
    return x

def load():
    out = {}
    for f in glob.glob("content/countries/*.json"):
        d = _fix(json.load(open(f))); out[d["slug"]] = d
    return dict(sorted(out.items(), key=lambda kv: kv[1]["name"]))

def _srcs(lst):
    return '<div class="cgsrc">' + "".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["title"])} ({E(s["publisher"])})</a>' for s in lst) + "</div>"

def page(slug, d, pic, all_):
    dt, gs = d["duty_to_help"], d["good_samaritan"]
    promo = "".join(f'<a href="{E(p["url"])}" target="_blank" rel="noopener"><b>{E(p["title"])}</b><span>{E(p["detail"])}</span><i>{E(p["publisher"])}</i></a>' for p in d["promotion"])
    more = "".join(f'<a href="/country-{s}">{E(v["name"])}</a>' for s, v in all_.items() if s != slug)
    return (STYLE + '<div class="csw"><div class="cseye">Country guide</div>'
            f'<h1 class="cstitle">{E(d["name"])}.</h1><p class="cslede">{E(d["summary"])}</p>'
            f'<div class="cgb"><h2>Is there a legal duty to help a stranger?</h2><span class="cgs">{E(STATUS.get(dt["status"], dt["status"]))}</span><p>{E(dt["detail"])}</p>{_srcs(dt["sources"])}</div>'
            f'<div class="cgb"><h2>Are people who help protected?</h2><span class="cgs">{E(STATUS.get(gs["status"], gs["status"]))}</span><p>{E(gs["detail"])}</p>{_srcs(gs["sources"])}</div>'
            f'<h2 class="fgh" style="font-size:clamp(1.5rem,5vw,2rem);margin:2rem 0 .4rem">How the government promotes giving and service</h2><div class="cgp">{promo}</div>'
            f'<div class="cgb"><h2>One thing worth knowing</h2><p>{E(d["notable"])}</p></div>'
            f'<div class="cgb"><h2>What this does not mean</h2><p>{E(d["caveat"])} This is a plain-language summary of public sources, not legal advice, and it does not rank countries. No government named here has endorsed this site.</p></div>'
            '<div class="cev"><h2>Read more</h2><div class="cevl">' + "".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener"><b>{E(s["title"])}</b><i>{E(s["publisher"])}</i></a>' for s in d["sources"]) + '</div></div>'
            f'<div class="csbar noprint"><a class="pr" href="/pdf/country-{slug}.pdf" download>Download PDF</a><button type="button" onclick="window.print()">Print</button><a href="/country-guides">All countries</a><a href="/evidence-room">Evidence Room</a></div>'
            f'<div class="csmore noprint"><b>More:</b> {more}</div></div>')

def hub(all_, pic):
    cards = "".join(
        f'<a class="cscard" href="/country-{s}"><div class="cb"><div class="ck">Country guide</div><b>{E(d["name"])}</b><span class="d">{E(d["summary"][:170].rsplit(" ", 1)[0])}...</span><span class="go">Open the guide</span></div></a>'
        for s, d in all_.items())
    pdfs = "".join(f'<a href="/pdf/country-{s}.pdf" download><span>{E(d["name"])}</span><i>PDF</i></a>' for s, d in all_.items())
    return (STYLE + '<div class="csw"><div class="cseye">By country</div><h1 class="cstitle">Country guides.</h1>'
            '<p class="cslede">What each government and legal system actually does about helping strangers: whether the law asks you to help, whether it protects you when you do, and how the state promotes giving and service.</p>'
            '<p class="csnote">Plain-language summaries of public sources, with links to the laws and official pages. Not legal advice. They do not rank countries, and no government has endorsed this site.</p>'
            '<label for="cgf" class="csnote" style="display:block;margin-bottom:0">Find a country</label><input class="cgfind" id="cgf" type="search" placeholder="Type a country" autocomplete="off">'
            f'<div class="csgrid" id="cgrid">{cards}</div><p class="csnote" id="cgnone" hidden>No country matches that yet.</p><h2>Download as PDF</h2><div class="cgpdf">{pdfs}</div></div>'
            '<script>(function(){var i=document.getElementById("cgf"),c=[].slice.call(document.querySelectorAll("#cgrid .cscard")),n=document.getElementById("cgnone");i.addEventListener("input",function(){var q=i.value.trim().toLowerCase(),s=0;c.forEach(function(a){var m=!q||a.textContent.toLowerCase().indexOf(q)>-1;a.hidden=!m;if(m)s++;});n.hidden=s>0;});})();</script>')
