"""The Evidence Room: documented cases with at least two independent sources each, on a map and as woodcut cards."""
import json, html, sys
sys.path.insert(0, "content")
from evidence_data import CASES

E = lambda s: html.escape(s, quote=True)
THEMES = {"rescue": "Rescue", "giving": "Giving", "everyday": "Everyday strangers"}
REGIONS = ["Europe", "Asia", "Americas", "Africa", "Oceania", "Everywhere"]
W, H = 1000, 395  # equirectangular, latitude 84N to 58S

def _xy(lon, lat):
    return (lon + 180) / 360 * W, (84 - lat) / 142 * H

def _land():
    d = json.load(open("content/land110.geojson"))
    out = []
    for f in d["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                pts, last = [], None
                for lon, lat in ring:
                    x, y = _xy(lon, lat)
                    if last and abs(x - last[0]) < 0.5 and abs(y - last[1]) < 0.5:
                        continue
                    pts.append((x, y)); last = (x, y)
                if len(pts) > 2:
                    out.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(out)

def _slug(n):
    return "c-" + "".join(ch.lower() if ch.isalnum() else "-" for ch in n).strip("-")[:40]

def _map():
    dots = ""
    for c in CASES:
        if c["lat"] is None: continue
        x, y = _xy(c["lon"], c["lat"])
        dots += (f'<a href="#{_slug(c["name"])}" class="evd {c["theme"]}" data-id="{_slug(c["name"])}">'
                 f'<title>{E(c["name"])}, {E(c["place"])}</title>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="transparent"/><circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="5"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="3.6"/></a>')
    return (f'<svg class="evmap" viewBox="0 0 {W} {H}" role="img" aria-label="World map with a point at each documented case">'
            f'<path class="land" d="{_land()}"/>{dots}</svg>')

def _card(c, i, pic):
    sid = _slug(c["name"])
    n = len(c["srcs"])
    img = pic(c["key"], True, True, E(c["label"])) if c["key"] else ""
    srcs = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a> <span class="pub">{E(p)}</span></li>' for t, u, p in c["srcs"])
    place = c["place"] + (", " + c["country"] if c["country"] else "")
    return (f'<article class="evc{" noimg" if not img else ""}" id="{sid}" data-theme="{c["theme"]}" data-region="{c["region"]}">'
            f'<div class="evi">{img}</div><div class="evb">'
            f'<div class="evtags"><span class="evt {c["theme"]}">{THEMES[c["theme"]]}</span> <span class="evp">{E(place)}</span></div>'
            f'<h3>{E(c["name"])}</h3><div class="evl">{E(c["label"])}</div>'
            f'<div class="evs">{E(c["summary"])}</div>'
            f'<div class="evg"><b>Grace to look for:</b> {E(c["grace"])}</div>'
            f'<details><summary><span class="evn">{n} independent sources</span> Check it yourself</summary>'
            f'<ul class="evsrc">{srcs}</ul><div class="evcav"><b>Where the sources differ:</b> {E(c["caveat"])}</div></details>'
            f'</div></article>')

SIGNS = [
 ("No audience.", "The act did not need to be seen to be worth doing.", ["Sir Nicholas Winton", "Larry Stewart, the original Secret Santa", "Chuck Feeney"]),
 ("Nothing coming back.", "The giver asked for no credit, no payment, no return.", ["Anonymous Kmart layaway donors, 2011", "Tiger Mask backpacks", "Ronald Read"]),
 ("A real cost.", "Time, money, safety or comfort was given up, not just spare change.", ["Irena Sendler", "Zura Karuhimbi", "Le Chambon-sur-Lignon"]),
 ("Strangers.", "The help went to people the giver would never meet again.", ["A stranger's kidney starts a chain of 60 operations", "Anonymous marrow and stem cell donors", "Las Patronas"]),
 ("It keeps going.", "It was not one gesture. It was years of it, often by whole communities.", ["Luis Soriano and the Biblioburro", "The Golden Temple langar", "Abdul Sattar Edhi"]),
]

def _signs():
    byname = {c["name"]: c for c in CASES}
    out = ""
    for t, d, names in SIGNS:
        links = ", ".join(f'<a href="#{_slug(n)}">{E(byname[n]["name"])}</a>' for n in names)
        out += f'<li><b>{E(t)}</b> {E(d)} <span class="evx">See {links}.</span></li>'
    return f'<ol class="evsigns">{out}</ol>'

STYLE = """<style>
.evh1{font-size:clamp(2.2rem,8vw,4.2rem);line-height:1.02;margin:0 0 .3em}
.evlede{font-size:1.15rem;max-width:40em}
.evstats{display:flex;flex-wrap:wrap;gap:1.2rem 2.4rem;margin:1.6rem 0 .6rem;padding:1.1rem 0;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink)}
.evstats div{font:700 .72rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase}
.evstats b{display:block;font:900 clamp(2rem,6vw,3rem) "Playfair Display",Georgia,serif;letter-spacing:0;line-height:1.1;margin-bottom:.3rem}
.evwide{width:min(1080px,calc(100vw - 44px));position:relative;left:50%;transform:translateX(-50%)}
.evrule{font-size:.95rem;opacity:.85;max-width:44em}
.evmapw{margin:1.6rem 0 .4rem;background:#0a0a0a;border:1px solid #2a2a28;padding:.6rem;border-radius:4px}
.evmap{display:block;width:100%;height:auto;overflow:hidden}
.evmap .land{fill:#2a2a28;stroke:none}
.evd{cursor:pointer}.evd .dot{stroke:#fff;stroke-width:.8}
.evd.rescue{--c:#e0705f}.evd.giving{--c:#59b8ae}.evd.everyday{--c:#e3c15a}
.evd .dot{fill:var(--c)}.evd .ring{fill:none;stroke:var(--c);stroke-width:1;transform-box:fill-box;transform-origin:center;animation:evp 3s ease-out infinite}
.evd:hover .dot,.evd:focus .dot{r:5}
@keyframes evp{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.2);opacity:0}}
@media (prefers-reduced-motion:reduce){.evd .ring{animation:none;opacity:.5}}
.evleg{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;font-size:.85rem;margin:.4rem 0 1.6rem}
.evleg i{display:inline-block;width:.8em;height:.8em;border-radius:50%;margin-right:.35em;vertical-align:-.05em}
.evleg .rescue i,.evt.rescue{background:#a33a2a}.evleg .giving i,.evt.giving{background:#1f6b63}.evleg .everyday i,.evt.everyday{background:#85660f}
.evfilt{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.2rem 0}
.evfilt button{font:700 .78rem ui-monospace,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;border:2px solid var(--ink);background:transparent;color:inherit;padding:.5em .9em;cursor:pointer}
.evfilt button[aria-pressed=true]{background:var(--ink);color:var(--bone)}
.evc{display:grid;grid-template-columns:1fr;gap:1rem 2rem;margin:0 0 3.2rem;padding-bottom:2.4rem;border-bottom:1px solid color-mix(in srgb,var(--ink) 25%,transparent);scroll-margin-top:1rem}
.evc[hidden]{display:none}.evnone{margin:2rem 0;font-style:italic}
.evi img{display:block;width:100%;height:auto;border:1px solid var(--ink)}
@media (min-width:860px){.evc{grid-template-columns:1.05fr 1fr;align-items:center}.evc:nth-of-type(even) .evi{order:2}.evc.noimg{grid-template-columns:1fr}}
.evc.hl{animation:evh 1.6s ease-out}@keyframes evh{0%{background:rgba(224,193,90,.45)}100%{background:transparent}}
.evtags{font:700 .7rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.5rem}
.evt{color:#fff;padding:.25em .6em;margin-right:.5em}
.evc h3{font-size:clamp(1.5rem,4.5vw,2.1rem);margin:.1em 0 .1em;line-height:1.1}
.evl{font-style:italic;opacity:.8;margin-bottom:.7rem}
.evs{margin-bottom:.8rem}
.evg{border-left:3px solid var(--ink);padding-left:.8rem;margin:.8rem 0}
.evc details{margin-top:.8rem}.evc summary{cursor:pointer;font-weight:700}
.evn{font:700 .7rem ui-monospace,Menlo,monospace;letter-spacing:.1em;text-transform:uppercase;background:var(--ink);color:var(--bone);padding:.25em .6em;margin-right:.6em}
.evsrc{padding-left:1.2em;margin:.7rem 0}.evsrc li{margin-bottom:.4em}.pub{opacity:.65;font-size:.88em}
.evcav{font-size:.9rem;opacity:.85}
.evsigns li{margin-bottom:.9em}.evx{display:block;font-size:.92rem;opacity:.85}
</style>"""

SCRIPT = """<script>(function(){
var cards=[].slice.call(document.querySelectorAll('.evc')),btns=[].slice.call(document.querySelectorAll('.evfilt button'));
var st={theme:'all',region:'all'};
function apply(){cards.forEach(function(c){c.hidden=!((st.theme=='all'||c.dataset.theme==st.theme)&&(st.region=='all'||c.dataset.region==st.region));});document.getElementById('evnone').hidden=cards.some(function(c){return !c.hidden;});}
btns.forEach(function(b){b.addEventListener('click',function(){var g=b.dataset.g;btns.forEach(function(o){if(o.dataset.g==g)o.setAttribute('aria-pressed',o==b?'true':'false');});st[g]=b.dataset.v;apply();});});
[].slice.call(document.querySelectorAll('.evd,.evsigns a')).forEach(function(a){a.addEventListener('click',function(e){
var id=(a.getAttribute('href')||'').slice(1),t=document.getElementById(id);if(!t)return;e.preventDefault();
st={theme:'all',region:'all'};btns.forEach(function(o){o.setAttribute('aria-pressed',o.dataset.v=='all'?'true':'false');});apply();
t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});t.classList.remove('hl');void t.offsetWidth;t.classList.add('hl');});});
})();</script>"""

def build(pic):
    n_src = len({u for c in CASES for _, u, _ in c["srcs"]})
    n_ctry = len({c["country"] for c in CASES if c["country"]})
    fb = lambda g, v, t, on=False: f'<button type="button" data-g="{g}" data-v="{v}" aria-pressed="{"true" if on else "false"}">{t}</button>'
    tb = "".join([fb("theme", "all", "All", True)] + [fb("theme", k, v) for k, v in THEMES.items()])
    rb = "".join([fb("region", "all", "Anywhere", True)] + [fb("region", r, r) for r in REGIONS])
    cards = "".join(_card(c, i, pic) for i, c in enumerate(CASES))
    return (STYLE +
     '<h1 class="evh1">The Evidence Room.</h1>\n'
     '<p class="evlede">People doing good without an audience and without taking credit, from every corner of the world. I think this is the clearest evidence of what humans are: they do it with nothing coming back.</p>\n'
     f'<div class="evstats"><div><b>{len(CASES)}</b>documented cases</div><div><b>{n_src}</b>sources</div><div><b>{n_ctry}</b>countries</div></div>\n'
     '<p class="evrule">The rule here: every case has at least two independent sources, and wire copies of one report do not count as two. Where the sources disagree, I show you how. Open &ldquo;Check it yourself&rdquo; on any card and read the sources before you believe me.</p>\n'
     '<h2>The map of unseen kindness</h2>\n'
     f'<div class="evwide"><div class="evmapw">{_map()}</div></div>\n'
     '<div class="evleg"><span class="rescue"><i></i>Rescue</span><span class="giving"><i></i>Giving</span><span class="everyday"><i></i>Everyday strangers</span><span>Tap a point to read the case. Three cases are everywhere and have no point.</span></div>\n'
     '<h2>How to recognize grace</h2>\n'
     '<p>You do not need a famous example to spot it. In every case below, look for these five things.</p>\n' + _signs() +
     '<h2>The cases</h2>\n'
     f'<div class="evfilt" role="group" aria-label="Filter by kind">{tb}</div><div class="evfilt" role="group" aria-label="Filter by region">{rb}</div>\n'
     '<div class="evwide">' + cards + '<div class="evnone" id="evnone" hidden>No case matches both filters yet. Try another combination.</div></div>\n'
     +
     '<p class="meta">Reports differ on small details such as dates and totals. Each case lists the sources so you can read them yourself. No person or organization named here has endorsed this site.</p>\n'
     + SCRIPT)


SUB_STYLE = """<style>
.evsub{margin:3.2rem 0 2rem}
.evband{background:var(--ink);color:var(--bone);border-radius:22px;padding:clamp(1.4rem,4vw,2.8rem)}
.evband a{color:inherit}
.evk{font:700 .7rem ui-monospace,Menlo,monospace;letter-spacing:.28em;text-transform:uppercase;opacity:.65}
.evband h2{font:900 clamp(2rem,7vw,3.6rem)/1 "Playfair Display",Georgia,serif;margin:.25em 0 .35em;letter-spacing:-.02em}
.evband .lede{font-size:clamp(1.05rem,2.6vw,1.3rem);line-height:1.5;max-width:38em;margin:0 0 1.4rem}
.evcrit{display:grid;gap:.8rem;margin:1.4rem 0 2rem}
@media(min-width:760px){.evcrit{grid-template-columns:repeat(3,1fr)}}
.evcrit div{border:1px solid color-mix(in srgb,var(--bone) 30%,transparent);border-radius:14px;padding:1rem 1.1rem}
.evcrit b{display:block;font:800 1.25rem/1.2 "Playfair Display",Georgia,serif;margin-bottom:.25rem}
.evcrit span{font-size:.95rem;opacity:.8}
.evform{background:var(--bone);color:var(--ink);border-radius:16px;padding:clamp(1rem,3vw,1.8rem);display:grid;gap:1.1rem}
.evform label,.evform legend{font:700 .72rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;display:block;margin-bottom:.4rem}
.evform textarea,.evform input[type=text],.evform input[type=url],.evform select{width:100%;box-sizing:border-box;font:500 1.05rem/1.45 "Playfair Display",Georgia,serif;color:var(--ink);background:var(--card);border:2px solid var(--ink);border-radius:10px;padding:.75rem .9rem}
.evform textarea{min-height:9rem;resize:vertical}
.evform textarea:focus,.evform input:focus,.evform select:focus{outline:3px solid var(--ink);outline-offset:2px}
.evrow{display:grid;gap:1.1rem}@media(min-width:760px){.evrow{grid-template-columns:1fr 1fr}}
.evform fieldset{border:0;padding:0;margin:0}
.evradio{display:flex;flex-wrap:wrap;gap:.5rem}
.evradio label{display:inline-flex;align-items:center;gap:.5rem;font:600 .95rem "Playfair Display",Georgia,serif;letter-spacing:0;text-transform:none;border:2px solid var(--ink);border-radius:999px;padding:.5em 1em;cursor:pointer;margin:0}
.evradio input{accent-color:var(--ink)}
.evradio label:has(input:checked){background:var(--ink);color:var(--bone)}
.evchk{display:flex;gap:.7rem;align-items:flex-start;font:500 .98rem/1.45 "Playfair Display",Georgia,serif;letter-spacing:0;text-transform:none;margin:0}
.evchk input{margin-top:.25rem;width:1.2rem;height:1.2rem;accent-color:var(--ink);flex:none}
.evcnt{font:700 .7rem ui-monospace,Menlo,monospace;letter-spacing:.1em;opacity:.65;text-align:right;margin-top:.25rem}
.evacts{display:flex;flex-wrap:wrap;gap:.7rem;align-items:center}
.evacts a,.evacts button{font:700 .8rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--bone);background:var(--ink);border:2px solid var(--ink);border-radius:999px;padding:.85em 1.4em;cursor:pointer}
.evacts button.sec{background:transparent;color:var(--ink)}
.evacts [aria-disabled=true],.evacts button:disabled{opacity:.35;cursor:not-allowed;pointer-events:none}
.evhint{font-size:.9rem;opacity:.75;margin:0}
.evpre{white-space:pre-wrap;font:500 .9rem/1.55 ui-monospace,Menlo,monospace;background:var(--card);border:1px dashed var(--ink);border-radius:10px;padding:1rem;max-height:16rem;overflow:auto;margin:0}
.evprom{display:grid;gap:.8rem;margin:2rem 0 0}
@media(min-width:760px){.evprom{grid-template-columns:repeat(3,1fr)}}
.evprom div{border:1px solid color-mix(in srgb,var(--bone) 30%,transparent);border-radius:14px;padding:1rem 1.1rem;font-size:.97rem;line-height:1.45}
.evprom b{display:block;font:700 .7rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.65;margin-bottom:.4rem}
.evsteps{list-style:none;counter-reset:s;padding:0;margin:2rem 0 0;display:grid;gap:.9rem}
.evsteps li{counter-increment:s;display:grid;grid-template-columns:3rem 1fr;gap:.8rem;align-items:start}
.evsteps li::before{content:counter(s);font:900 2.2rem/1 "Playfair Display",Georgia,serif}
.evsteps b{display:block;font:800 1.15rem/1.25 "Playfair Display",Georgia,serif}
.evsteps span{opacity:.8;font-size:.97rem}
.evsafe{font-size:.9rem;opacity:.8;margin-top:1.8rem}
@media print{.evsub{display:none}}
</style>"""

def submit():
    return (SUB_STYLE + """
<section class="evsub evwide" id="send" aria-labelledby="evsh">
<div class="evband">
<div class="evk">Add to the map</div>
<h2 id="evsh">Send us what you saw.</h2>
<p class="lede">If you have seen, or done, something good that nobody knew about and nobody took credit for, I would like to hear it. A stranger who paid a bill and left. A neighbor who quietly fixed something. A gift nobody traced. The small ones count most.</p>
<div class="evcrit">
<div><b>Unseen</b><span>It did not need an audience, and there was no camera or crowd to reward it.</span></div>
<div><b>Unrewarded</b><span>Nothing came back: no credit, no payment, no thanks.</span></div>
<div><b>Real</b><span>You did it, you saw it, or you can point to where it was reported.</span></div>
</div>
<div class="evform" id="evform">
<div><label for="evstory">What happened</label><textarea id="evstory" placeholder="Tell it plainly: who did what, and why it stayed unseen." aria-describedby="evcount"></textarea><div class="evcnt" id="evcount" aria-live="polite">0 words</div></div>
<div class="evrow">
<div><label for="evwhere">Where, and roughly when</label><input type="text" id="evwhere" placeholder="A city or town, and a month or year"></div>
<div><label for="evhow">How I know</label><select id="evhow"><option>I did it</option><option selected>I saw it</option><option>I heard it from someone involved</option><option>It was reported (I will add a link)</option></select></div>
</div>
<div><label for="evlink">A link, if there is one (optional)</label><input type="url" id="evlink" placeholder="https://"></div>
<fieldset><legend>Credit</legend><div class="evradio">
<label><input type="radio" name="evcr" value="anon" checked> Keep me anonymous</label>
<label><input type="radio" name="evcr" value="first"> Use my first name</label>
<label><input type="radio" name="evcr" value="full"> Use my full name</label></div>
<input type="text" id="evname" placeholder="Name to use" style="margin-top:.6rem;display:none"></fieldset>
<label class="evchk"><input type="checkbox" id="evc1"> I understand this may be published on thisisdisclosure.com, in my words or lightly edited for length and clarity, without my name or email unless I chose credit above.</label>
<label class="evchk"><input type="checkbox" id="evc2"> I have not included private details about anyone else, such as medical or financial information, unless they said it is fine.</label>
<div class="evacts"><a id="evmail" href="#" role="button" aria-disabled="true">Open in my email app</a><button type="button" class="sec" id="evcopy" disabled>Copy the message</button><button type="button" class="sec" id="evdl" disabled>Download as a text file</button></div>
<p class="evhint" id="evhint">Write at least a couple of sentences and tick both boxes. Nothing is sent from this page: your email app opens with the message filled in, and you press send. Your draft stays on this device only.</p>
<details><summary class="evhint" style="cursor:pointer">Preview the message</summary><pre class="evpre" id="evpre"></pre></details>
<noscript><p class="evhint">Turn on JavaScript to build the message here, or write to evidence at thisisdisclosure dot com and tell us what happened, where and when, and how you know.</p></noscript>
</div>
<div class="evprom">
<div><b>Your words</b>Anything you send may be published in your words or lightly edited. Not everything will be, and I cannot promise it will be.</div>
<div><b>Your name</b>By default I publish without your name or email. If you want credit, you choose how you are named.</div>
<div><b>Others' privacy</b>Do not send anything that identifies another person, or private medical or financial details, unless they have said it is fine.</div>
<div><b>Take it back</b>Ask me to take your story down and I will, and I will delete your email.</div>
<div><b>Your email</b>I will not sell it, share it, or add it to any list. I do not pay for stories.</div>
<div><b>Your consent</b>Sending the message means you understand all of this. The message repeats it.</div>
</div>
<ol class="evsteps">
<li><div><b>You send it.</b><span>It arrives in one inbox. I read every message.</span></div></li>
<li><div><b>I check what can be checked.</b><span>Cases on this page each have two or more independent sources. A personal story is a different thing, and if I publish one I will say it is a reader's account.</span></div></li>
<li><div><b>You stay in control.</b><span>Change your mind at any time and write back: I will take it down.</span></div></li>
</ol>
<p class="evsafe">This is not for emergencies. If you are in crisis, in the US you can call or text 988. Elsewhere, <a href="https://findahelpline.com/" target="_blank" rel="noopener">findahelpline.com</a> lists services by country.</p>
</div>
</section>
<script>(function(){
var $=function(i){return document.getElementById(i)};
var u=['evidence','thisisdisclosure.com'].join('@');
var st=$('evstory'),wh=$('evwhere'),hw=$('evhow'),lk=$('evlink'),nm=$('evname'),c1=$('evc1'),c2=$('evc2'),mail=$('evmail'),cp=$('evcopy'),dl=$('evdl'),pre=$('evpre'),cnt=$('evcount'),hint=$('evhint');
var KEY='disclosure-ev-draft';
function credit(){var r=document.querySelector('input[name=evcr]:checked');return r?r.value:'anon';}
function words(t){t=t.trim();return t?t.split(/\\s+/).length:0;}
function build(){
 var c=credit(),who=c==='anon'?'Keep me anonymous.':(c==='first'?'Use my first name: ':'Use my full name: ')+nm.value.trim();
 return 'What happened:\\n'+st.value.trim()+'\\n\\nWhere and roughly when:\\n'+wh.value.trim()+'\\n\\nHow I know:\\n'+hw.value+'\\n\\nA link, if there is one:\\n'+lk.value.trim()+'\\n\\nCredit:\\n'+who+'\\n\\nI understand you may publish this on thisisdisclosure.com, in my words or lightly edited, without my name or email unless I chose credit above. I have not included private details about anyone else. I can ask you to take it down at any time.\\n';
}
function save(){try{localStorage.setItem(KEY,JSON.stringify({s:st.value,w:wh.value,h:hw.selectedIndex,l:lk.value,c:credit(),n:nm.value}));}catch(e){}}
function refresh(){
 var n=words(st.value);cnt.textContent=n+(n===1?' word':' words');
 nm.style.display=credit()==='anon'?'none':'block';
 var ok=n>=8&&c1.checked&&c2.checked&&(credit()==='anon'||nm.value.trim());
 var text=build();pre.textContent=text;
 var href='mailto:'+u+'?subject='+encodeURIComponent('Evidence Room story')+'&body='+encodeURIComponent(text);
 mail.setAttribute('aria-disabled',ok?'false':'true');mail.href=ok?href:'#';
 cp.disabled=!ok;dl.disabled=!ok;
 hint.textContent=ok?(href.length>1900?'This one is long. If your email app does not open with the whole message, use Copy the message and paste it into an email to '+u+'.':'Ready. Your email app opens with the message filled in, addressed to '+u+'. You press send.'):'Write at least a couple of sentences, choose how you want to be credited, and tick both boxes. Nothing is sent from this page.';
 save();
}
try{var d=JSON.parse(localStorage.getItem(KEY)||'null');if(d){st.value=d.s||'';wh.value=d.w||'';hw.selectedIndex=d.h||0;lk.value=d.l||'';nm.value=d.n||'';var r=document.querySelector('input[name=evcr][value='+(d.c||'anon')+']');if(r)r.checked=true;}}catch(e){}
[st,wh,hw,lk,nm,c1,c2].forEach(function(e){e.addEventListener('input',refresh);e.addEventListener('change',refresh);});
document.querySelectorAll('input[name=evcr]').forEach(function(e){e.addEventListener('change',refresh);});
mail.addEventListener('click',function(e){if(mail.getAttribute('aria-disabled')==='true')e.preventDefault();});
cp.addEventListener('click',function(){var t=build();(navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(t):Promise.reject()).then(function(){hint.textContent='Copied. Paste it into an email to '+u+'.';},function(){pre.parentNode.open=true;var rg=document.createRange();rg.selectNodeContents(pre);var s=window.getSelection();s.removeAllRanges();s.addRange(rg);hint.textContent='Select and copy the message in the preview, then paste it into an email to '+u+'.';});});
dl.addEventListener('click',function(){var b=new Blob([build()],{type:'text/plain'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='evidence-room-story.txt';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);});
refresh();
})();</script>
""")
