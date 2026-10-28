#!/usr/bin/env python3
"""Builds public/index.html and public/art/*.webp from art/*.png. Run from ~/thisisdisclosure."""
import re, hashlib, glob, os
from PIL import Image
import numpy as np

LAT="U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
EXT="U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"
FONTFACE="".join(f'''  @font-face {{ font-family: "Playfair Display"; font-style: {st}; font-weight: 400 900; font-display: swap;
    src: url(/fonts/{pre}-{sub}.woff2) format("woff2"); unicode-range: {rng}; }}\n'''
    for st,pre in (("normal","pf"),("italic","pf-italic")) for sub,rng in (("latin",LAT),("latinext",EXT)))

# (size class, html, image key, alt, framed)
S=[
 ("xl title","<div class=\"mailhd\"><div class=\"mrow\"><span>From</span><b>Keith Adler</b></div><div class=\"mrow\"><span>To</span><b>Humanity</b></div><div class=\"mrow\"><span>Cc</span><b>Higher Intelligence</b></div><div class=\"msub\"><span>Subject</span><p class=\"ttl\">This Is Disclosure</p></div></div><button class=\"cta\" type=\"button\">Click to advance</button><a class=\"cta2\" href=\"/cheat-sheets\"><span class=\"c2k\">Start here</span><span class=\"c2t\">If you only do one thing, take my cheat sheet</span><span class=\"c2s\">Plain, practical one-pagers for elders, teens, parents, everyday life and more.</span><span class=\"c2a\" aria-hidden=\"true\">&rarr;</span></a>",None,"",False),
 ("l","<p>Humans of the world.</p><p class=\"sm\">And that means you.</p>","world","A great crowd of people from every culture, facing the sunrise together.",True),
 ("xl rev","<h1>My name is <em>Keith Adler.</em></h1>","keith","Woodcut portrait of Keith Adler.",True),
 ("l","<p>This isn&rsquo;t about me.</p><p class=\"sm\">It&rsquo;s about every single one of us, me included.</p>","crowd","A crowd of ordinary people of every age, looking out.",False),
 ("t","<p>In one sentence: I believe how we treat each other is being measured.</p><p class=\"sm\">This is a hypothesis and my interpretation, not a scientific result. Nothing is for sale, there is no group to join, and no one will ask you for money.</p>","nosale","A man sits at a bare table with open empty hands while passersby slow down.",True),
 ("l three","<p>I am not a prophet.</p><p>Not an alien.</p><p>Not an idiot.</p><p class=\"sm\">Though I&rsquo;ve done stupid things, as we all have.</p>","table","A man laughing warmly in his workshop.",False),
 ("l three","<p>I&rsquo;m not a scientist.</p><p>I&rsquo;m not a theologian.</p>","rooms","A woman walking a hall of open doors, each room different.",True),
 ("t ","<p>This isn&rsquo;t recruiting for a religion or an argument against yours or against none.</p>","religion","People of many kinds share a long meal at one table.",True),
 ("m","<p>I am a human being like you.</p>","hands","Two hands of different skin tones gripping each other's forearms.",True),
 ("t","<p>Once I saw this, I could never see the world the same way again.</p><p class=\"sm\">Through this lens, everything starts to make sense on a global scale. I believe.</p>","face","A young woman at a window, seeing the city as if new.",True),
 ("t","<p>What I&rsquo;m about to tell you is <em>not</em> a joke.</p><p>This is <em>not</em> some social media trope.</p>","candle","An older woman alone at her kitchen table at night, reading a letter.",True),
 ("t","<p>It&rsquo;s something that, if you believed strongly yourself, I would want you to tell me.</p>","whisper","Two friends, one telling the other something important.",False),
 ("m","<p>That is why I am telling you.</p>","pass","A mother crouching to tell her child something important.",False),
 ("t","<p>I ask that you consider a hypothesis. It may explain not just the recent decade plus, but <em>all of human history.</em></p>","procession","Ordinary people from every age of history walking a road toward the sunrise.",False),
 ("t","<p>I am very confident that once I give you the keystone, the rest will fall into place.</p>","keystone","Stonemasons lowering the keystone into an arch.",False),
 ("t","<p>I gave and will answer a bunch of FAQs to make sure this doesn&rsquo;t get misinterpreted and to frame it.</p>","circle","Neighbors around a library table, asking questions and getting answers.",False),
 ("t","<p>I will only tell you things that I can strongly defend as my theory.</p>","carve","Hands carving a line into a block of wood.",False),
]
SECRET=[]  # the gated slides are not published in this repository
GATE_IMG=("gate","A person pausing at an open door, light spilling through.",False)
SRC={"door":"01","crowd":"02","table":"workshop","hands":"grip","candle":"letter2","whisper":"friends","pass":"mother","procession":"road","keystone":"09","circle":"library","carve":"11","gate":"12",
     "world":"world","params":"params","bench":"bench","rings":"rings","layers":"layers","refuse":"refuse","medics":"medics","treaty":"treaty","finish":"finish","contract":"contract","masks":"masks","grace":"grace","unseen":"unseen","kindtest":"kindtest","bridge":"bridge","nosale":"nosale","comfort":"comfort","ukraine":"ukraine","midnight":"midnight","tajfel":"tajfel","fehr":"fehr","whitehall":"whitehall","peace":"peace","redeem":"redeem","asch":"asch","milgram":"milgram","robbers":"robbers","bystander":"bystander","truce":"truce","religion":"religion","porch":"porch","classroom":"classroom","courtroom":"courtroom","wallet":"wallet","lab":"lab","peace":"peace","harvest":"harvest","sign":"sign","hallway":"hallway","hiring":"hiring","writer":"writer","market":"market","telescope":"telescope","tell":"tell","subway":"subway","stones":"stones","elder":"elder","window":"window","exam":"exam","fork":"fork","climb":"climb","stop":"stop","bus":"bus","nurse":"nurse","runner":"runner","keith":"keith_a","cosmos":"cosmos","test":"test","wall":"wall","clock":"clock","chain":"chain","rooms":"rooms","face":"dawn"}


import sys as _sys; _sys.path.insert(0,"content")
from evidence_data import CASES as _EVC
import faith_guides as _FG
import country_guides as _CG
import share_page as _SH
import narration as _NA
SRC.update(_SH.ART)
SRC.update({"fg_"+s:a for s,a in _FG.ART.items()})
SRC.update({"cs_everyone":"grace","cs_everyday":"bench","cs_elders":"elder","cs_teens":"classroom","cs_parents":"mother","cs_leaders":"hiring","cs_inside":"hallway","cs_fallen":"porch","cs_meaning":"climb"})
SRC.update({c["key"]:c["key"] for c in _EVC if c["key"]})
import html as _html, quotes as QD, quotes2 as QD2
ALL={**QD.Q,**QD2.Q2}
try:
    import quotes3 as QD3
    ALL.update(QD3.Q3)
except ImportError:
    pass
import quotes4 as QD4
ALL.update(QD4.Q4)
def _one(qid,cls):
    text,who,work,date,url,basis=ALL[qid]
    t=_html.escape(text,quote=False).replace("|","<br>").replace("--","\u2013")
    if not t.startswith("\u201c"): t="\u201c"+t+"\u201d"
    c=_html.escape(who+", "+work+", "+date,quote=False)
    return f'<div class="q {cls}"><blockquote>{t}</blockquote><cite>{c}</cite></div>'
def qt(pair):
    if not pair: return ''
    a,b2=pair
    return f'<aside class="qt">{_one(a,"q1")}{_one(b2,"q2")}</aside>'

INK=np.array([10,10,10],float); BONE=np.array([241,237,228],float)
os.makedirs("public/art",exist_ok=True); os.makedirs("public/s",exist_ok=True)
for f in glob.glob("public/art/*"): os.remove(f)
WIDTHS=(640,1100)
SIZES="(min-width: 900px) 50vw, 92vw"
def pic(key,dark,framed,alt,eager=False):
    """Bake one woodcut into AVIF + WebP at two widths and return a <picture> element."""
    framed = framed or dark   # images on black slides always sit on white paper
    im=Image.open(f"art/{SRC[key]}.png").convert("L")
    a=np.asarray(im,float)/255
    if not framed:
        ys,xs=np.where(a<0.8); m=int(0.02*im.width)
        im=im.crop((max(xs.min()-m,0),max(ys.min()-m,0),min(xs.max()+m,im.width),min(ys.max()+m,im.height)))
    inv = dark and not framed
    files={"avif":[],"webp":[]}; dims=None; digest=hashlib.md5()
    for W in WIDTHS:
        r=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS)
        g=np.clip((np.asarray(r,float)/255-0.12)/0.70,0,1)[...,None]
        PAPER=np.array([255,255,255],float) if (dark or key in ("candle","pass")) else BONE
        out = BONE*(1-g)+INK*g if inv else INK*(1-g)+PAPER*g
        img=Image.fromarray(out.astype("uint8")); dims=dims or {}; dims[W]=img.size
        for fmt,kw in (("avif",dict(quality=48,speed=6)),("webp",dict(quality=68,method=6))):
            tmp=f"/tmp/{key}.{W}.{fmt}"; img.save(tmp,**kw); data=open(tmp,"rb").read(); digest.update(data)
            files[fmt].append((W,tmp))
    h=digest.hexdigest()[:8]; srcs={}
    for fmt in files:
        parts=[]
        for W,tmp in files[fmt]:
            name=f"{key}.{h}.{W}.{fmt}"; os.replace(tmp,f"public/art/{name}"); parts.append(f"/art/{name} {W}w")
        srcs[fmt]=", ".join(parts)
    w,h2=dims[WIDTHS[-1]]
    fallback=srcs["webp"].split(", ")[-1].split(" ")[0]
    PCLS=' class="paper"' if (dark or key in ("candle","pass")) else ""
    return (f'<picture><source type="image/avif" srcset="{srcs["avif"]}" sizes="{SIZES}">'
            f'<img{PCLS} src="{fallback}" srcset="{srcs["webp"]}" sizes="{SIZES}" width="{w}" height="{h2}" alt="{alt}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async"></picture>')

secs=""
for n,(sz,txt,key,alt,framed) in enumerate(S,1):
    c="b" if n%2==1 else "k"
    cue='<div class="cue" aria-hidden="true"></div>' if n==1 else ''
    q=qt(QD.PUBLIC[n-2]) if 2<=n<=len(QD.PUBLIC)+1 else ''
    if key is None:
        secs+=f'<section class="{c} {sz}{" in" if n==1 else ""}"{_NA.attr(txt,False)}><div class="txt">{txt}</div>{q}{cue}</section>\n'
        continue
    fr=" framed" if c=="k" else ""
    secs+=f'<section class="{c} {sz}{" in" if n==1 else ""}"{_NA.attr(txt,False)}><div class="txt">{txt}</div><figure class="{fr.strip()}">{pic(key,c=="k",framed,alt,eager=False)}</figure>{q}{cue}</section>\n'
n=len(S)+1; c="b" if n%2==1 else "k"; oc="b" if c=="k" else "k"
gpic=pic("gate",c=="k",False,GATE_IMG[1])
gate=f'''<section class="{c} t gate" id="gate" aria-labelledby="gate-h"><div class="txt"><p id="gate-h">Before you go further, please read the disclaimers.</p>
  <p class="sm">This site is for adults, 18 and over. It contains nothing graphic, sexual, or otherwise inappropriate for work. What follows is one person&rsquo;s hypothesis, not fact, advice or a promise.</p>
  <div class="links"><a href="/disclaimer" target="_blank" rel="noopener">Disclaimers<span class="vh"> (opens in a new tab)</span></a></div>
  <div role="group" aria-label="Confirm to continue">
  <label class="chk"><input type="checkbox" id="adult"><span>Yes, I&rsquo;m an adult (18 or over).</span></label>
  <label class="chk"><input type="checkbox" id="read"><span>I have read the disclaimers. I understand this is a hypothesis, not advice, and that I use this site at my own risk.</span></label></div>
  <button id="ack" type="button" disabled aria-describedby="ack-hint">Continue</button><span id="ack-hint" class="vh">Tick both boxes to continue.</span></div>
  <figure>{gpic}</figure></section>'''

# --- secret slides: shown only after the visitor agrees; fetched from an unlisted path ---
import shutil
shutil.rmtree("public/s",ignore_errors=True); os.makedirs("public/s")
sec=""
for j,(sz,txt,key,alt,framed) in enumerate(SECRET,1):
    pos=len(S)+1+j
    col="b" if pos%2==1 else "k"
    q=qt(QD.SECRET[j-1])
    if key is None:
        sec+=f'<section class="{col} {sz}"{_NA.attr(txt,True)}><div class="txt">{txt}</div>{q}</section>\n'
        continue
    fr=" framed" if col=="k" else ""
    sec+=f'<section class="{col} {sz}"{_NA.attr(txt,True)}><div class="txt">{txt}</div><figure class="{fr.strip()}">{pic(key,col=="k",framed,alt)}</figure>{q}</section>\n'
last=len(S)+1+len(SECRET)
oc="k" if last%2==1 else "b"
sh=hashlib.md5(sec.encode()).hexdigest()[:10]
open("public/s/secret.txt","w").write(sec)
fpic=pic("door",oc=="k",False,"A figure standing in an open doorway at dawn.")
html=open("template.html").read().replace("%%FONTFACE%%",FONTFACE).replace("%%SECTIONS%%",secs+gate).replace("%%AFTERCLASS%%",oc).replace("%%SECRETURL%%","/s/secret.txt").replace("%%FINALPIC%%",fpic).replace("%%AUDIO%%","/audio/loop."+open("audio/hash.txt").read().strip()+".mp3")
open("public/index.html","w").write(html)
print("built",len(S)+1,"public sections +",len(SECRET),"secret; after is",oc,"; fragment /s/"+sh+".txt")

# --- FAQ: adults only. The page is a shell; the questions load after the 18+ gate has been agreed. ---
body=open("content/faq-body.html").read()
import datetime as _dt
_td=_dt.date.today()
body=body.replace("%%TODAY_ISO%%",_td.isoformat()).replace("%%TODAY%%",_td.strftime("%B ")+str(_td.day)+_td.strftime(", %Y"))
# Stable question numbers: a question keeps its number forever (people will cite them); new questions take the next number.
import json as _fj, re as _fre, html as _fh2
_reg_path="content/faq-numbers.json"
try: _reg=_fj.load(open(_reg_path))
except OSError: _reg={}
_nxt=max(_reg.values(),default=0)
_items=[]
def _num_h2(m):
    global _nxt
    raw=m.group(1); key=_fh2.unescape(_fre.sub(r"<[^>]+>","",raw)).strip()
    if key not in _reg:
        _nxt+=1; _reg[key]=_nxt
    n=_reg[key]; _items.append((n,raw))
    return f'<h2 id="q{n}"><a class="qn" href="#q{n}" title="Link to question {n}">Q{n}</a>{raw}</h2>'
body=_fre.sub(r"<h2>(.*?)</h2>",_num_h2,body)
_fj.dump(_reg,open(_reg_path,"w"),ensure_ascii=False,indent=1)
# Scientific support blocks (content/faq_science.json: {"15": {"claim","support":[...],"note"}}); only questions with real support get one.
def _sci_block(n):
    try: d=_fj.load(open("content/faq_science.json")).get(str(n))
    except OSError: return ""
    if not d or not d.get("support"): return ""
    fit={"supports":"supports","analogy":"analogy","tests part":"tests one part","skeptical":"skeptical"}
    lis="".join(f'<li><a href="{_fh2.escape(s["url"],quote=True)}" target="_blank" rel="noopener">{_fh2.escape(s["title"])}</a> <span class="tg">{fit.get(s["fit"],s["fit"])}</span><br><span class="fnd">{_fh2.escape(s["finding"])}</span></li>' for s in d["support"])
    claim=f'<p class="scc">{_fh2.escape(d["claim"])}</p>' if d.get("claim") else ""
    note=f'<p class="scn">{_fh2.escape(d["note"])}</p>' if d.get("note") else ""
    return f'<div class="rd sci"><p class="rdh">Scientific support for this answer</p>{claim}<ul>{lis}</ul>{note}</div>\n'
_parts=_fre.split(r'(?=<h2 id="q\d+")',body)
body="".join(p+(_sci_block(int(_fre.match(r'<h2 id="q(\d+)"',p).group(1))) if _fre.match(r'<h2 id="q(\d+)"',p) else "") for p in _parts)
_idx='<details class="qidx"><summary>All '+str(len(_items))+' questions, by number</summary><ol>'+"".join(f'<li value="{n}"><a href="#q{n}">{raw}</a></li>' for n,raw in sorted(_items))+'</ol></details>\n'
body=_idx+body
fh=hashlib.md5(body.encode()).hexdigest()[:10]
open("public/s/faq.txt","w").write(body)
shell=open("content/faq-head.html").read()+f"""
<h1>FAQs</h1>
<div id="faq-body"></div>
<p id="faq-lock" hidden>The FAQs are for adults, 18 and over. Please go to the <a href="/">front page</a>, read the disclaimers and agree there, and they will open.</p>
<script>
(function(){{
  var ok=false; try{{ ok=localStorage.getItem('disclosure-ack')==='v2'; }}catch(e){{}}
  var box=document.getElementById('faq-body'), lock=document.getElementById('faq-lock');
  if(!ok){{ lock.hidden=false; return; }}
  fetch('/s/faq.txt',{{credentials:'omit'}}).then(function(r){{return r.ok?r.text():'';}}).then(function(t){{ if(t){{ box.innerHTML=t; var h=location.hash; if(h){{ var e=document.getElementById(h.slice(1)); if(e){{ e.scrollIntoView(); e.classList.add('qhl'); }} }} }} else lock.hidden=false; }}).catch(function(){{ lock.hidden=false; }});
}})();
</script>
</main></body></html>
"""
open("public/faq.html","w").write(shell)
print("faq fragment /s/faq."+fh+".txt")

# --- Sources page: every quotation used, in order of appearance, plus the research cited ---
seen=[]; 
for pair in list(QD.PUBLIC)+[p for p in QD.SECRET if p]:
    for qid in pair:
        if qid and qid not in seen: seen.append(qid)
rows=""
for qid in seen:
    text,who,work,date,url,basis=ALL[qid]
    t=_html.escape(text,quote=False).replace("|"," / ").replace("--","\u2013").strip("\u201c\u201d")
    rows+=(f'<blockquote>\u201c{t}\u201d</blockquote>\n<p class="meta">{_html.escape(who,quote=False)}, {_html.escape(work,quote=False)}, {_html.escape(date,quote=False)}.<br>'
           f'Status: {_html.escape(basis,quote=False)}.<br><a href="{_html.escape(url)}" target="_blank" rel="noopener">Source text</a></p>\n')
intro=("<h1>Sources</h1>\n<p>Every quotation on this site is a short excerpt from a work in the public domain in the United States "
 "(or a United States government work, or a United Nations document). Each is shown with who said or wrote it, in what work, and when, "
 "and with the translator where there is one. The wording was checked against the source linked below.</p>\n"
 "<p><strong>No endorsement.</strong> Every person, author, scholar, institution, government body, religion and tradition named or quoted here appears only for attribution or reference. None of them has reviewed, approved, sponsored or endorsed this site or my ideas, and none is affiliated with it. The one exception is me: I am Keith Adler, I wrote this site, and I endorse it. A quotation shows what someone wrote or said, not that they agree with me. The studies, documents and events cited are shown as public facts and records; the interpretations and conclusions drawn from them are mine alone.</p>\n"
 "<p>If you think anything is misattributed, or you hold rights in something shown here, please tell me through the address at the end of the site, and I will look at it.</p>\n")
open("public/sources.html","w").write(open("content/sources-head.html").read()+"\n"+intro+rows+open("content/sources-research.html").read()+"</main></body></html>\n")

# --- the shareable page: "How to cheat on the test" (no gate, no countdown, no claims about anything else) ---
_ch=open("content/sources-head.html").read()
_ch=_ch.replace("<title>Sources | This Is Disclosure</title>","<title>How to cheat on the test | This Is Disclosure</title>")
_ch=_ch.replace('<meta name="description" content="Sources for the quotations on This Is Disclosure.">','<meta name="description" content="One question, and the whole answer key: Is this what a human being does? Treat each other like humans.">\n<meta property="og:title" content="How to cheat on the test">\n<meta property="og:description" content="One question, and the whole answer key: Is this what a human being does? Treat each other like humans.">\n<meta property="og:type" content="website">\n<meta property="og:url" content="https://thisisdisclosure.com/how-to-cheat-on-the-test">\n<meta property="og:image" content="https://thisisdisclosure.com/og-card.png?v=2">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="https://thisisdisclosure.com/og-card.png?v=2">')
_ch=_ch.replace('<link rel="canonical" href="https://thisisdisclosure.com/sources">','<link rel="canonical" href="https://thisisdisclosure.com/how-to-cheat-on-the-test">')
assert "how-to-cheat-on-the-test" in _ch
_body=("<h1>How to cheat on the test.</h1>\n"
 "<p>There is one question. Ask it before you speak, before you reply, before you click, before you decide.</p>\n"
 "<p style=\"font-size:clamp(1.8rem,6vw,3rem);line-height:1.1;font-weight:900;margin:1.2em 0\">Is this what a human being does?</p>\n"
 "<p>Not the pack. Not what is easy, or what pays, or what everyone else is doing. A human being thinks for themselves, treats people fairly, and gives with nothing expected back.</p>\n"
 "<p>That is the whole answer key. If I held a sign on a street corner, it would say: <em>Treat each other like humans.</em></p>\n"
 "<p class=\"meta\" style=\"margin-top:3rem\">You do not have to believe anything else on this site to use it. Share it freely. <a href=\"/\">Read the rest at thisisdisclosure.com</a>. Or take a cheat sheet made for you: <a href=\"/cheat-sheets\">elders, teenagers, everyday life, people in charge, people building meaning</a>.</p>\n")
open("public/how-to-cheat-on-the-test.html","w").write(_ch+"\n"+_body+"</main></body></html>\n")

# --- predictions page: the exact text, its SHA-256, and how anyone can check it ---
import html as _h2
_pt=open("content/predictions.txt","rb").read()
_ph=hashlib.sha256(_pt).hexdigest()
_pa1=open("content/predictions-added-1.txt","rb").read()
_pah1=hashlib.sha256(_pa1).hexdigest()
_pa2=open("content/predictions-added-2.txt","rb").read()
_pah2=hashlib.sha256(_pa2).hexdigest()
_pa3=open("content/predictions-added-3.txt","rb").read()
_pah3=hashlib.sha256(_pa3).hexdigest()
_pg=open("content/sources-head.html").read()
_pg=_pg.replace("<title>Sources | This Is Disclosure</title>","<title>Predictions | This Is Disclosure</title>")
_pg=_pg.replace('<meta name="description" content="Sources for the quotations on This Is Disclosure.">','<meta name="description" content="Predictions written down in advance, with a SHA-256 fingerprint of the exact text so no one can say they were changed later.">')
_pg=_pg.replace('<link rel="canonical" href="https://thisisdisclosure.com/sources">','<link rel="canonical" href="https://thisisdisclosure.com/predictions">')
assert "thisisdisclosure.com/predictions" in _pg
_pbody=("<h1>Predictions.</h1>\n<p>Written down in advance so nobody can say they were changed afterward. If I am wrong, this page will still be here.</p>\n"
 "<p class=\"meta\">This website will become substantially more populated with information and predictions. New predictions are added below with their own date and fingerprint.</p>\n"
 "<pre style=\"white-space:pre-wrap;font:600 1rem/1.7 ui-monospace,Menlo,monospace;background:color-mix(in srgb,var(--ink) 6%,transparent);padding:1.2rem;margin:1.6rem 0\">"+_h2.escape(_pt.decode())+"</pre>\n"
 "<p class=\"meta\">SHA-256 of the text above, exactly as written, with a single line break after the last line:<br><span style=\"word-break:break-all\">"+_ph+"</span></p>\n"
 "<p class=\"meta\">To check it, copy the box above into a plain text file and run <code>shasum -a 256 file.txt</code>. The same fingerprint should appear. A snapshot of this page is also saved at the Internet Archive.</p>\n"
 "<p class=\"meta\">Any correction will be added below with its date. Nothing above will be edited.</p>\n"
 "<h2>Added later</h2>\n<p class=\"meta\">New predictions are added here with their own date and fingerprint. The text above stays as it was.</p>\n<pre style=\"white-space:pre-wrap;font:600 1rem/1.7 ui-monospace,Menlo,monospace;background:color-mix(in srgb,var(--ink) 6%,transparent);padding:1.2rem;margin:1.2rem 0\">"+_h2.escape(_pa1.decode())+"</pre>\n<p class=\"meta\">SHA-256 of the box above:<br><span style=\"word-break:break-all\">"+_pah1+"</span></p>\n"
 "<pre style=\"white-space:pre-wrap;font:600 1rem/1.7 ui-monospace,Menlo,monospace;background:color-mix(in srgb,var(--ink) 6%,transparent);padding:1.2rem;margin:1.2rem 0\">"+_h2.escape(_pa2.decode())+"</pre>\n<p class=\"meta\">SHA-256 of the box above:<br><span style=\"word-break:break-all\">"+_pah2+"</span></p>\n"
 "<pre style=\"white-space:pre-wrap;font:600 1rem/1.7 ui-monospace,Menlo,monospace;background:color-mix(in srgb,var(--ink) 6%,transparent);padding:1.2rem;margin:1.2rem 0\">"+_h2.escape(_pa3.decode())+"</pre>\n<p class=\"meta\">SHA-256 of the box above:<br><span style=\"word-break:break-all\">"+_pah3+"</span></p>\n<p class=\"meta\"><a href=\"/prove-me-wrong\">Where to check it</a></p>\n"
 "<h2>Evidence I am pointing to</h2>\n"
 "<p class=\"meta\">For the liquid or mist speculation. This is a pointer, not proof.</p>\n"
 "<p class=\"meta\">In November 2014 a Chilean Navy helicopter&rsquo;s infrared camera recorded an object that appeared to release two plumes of gas or vapor, visible only in infrared. In 2017 Chile&rsquo;s CEFAA classified it as an unidentified aerial phenomenon. It said the object could not have been a military or civilian aircraft and that the plumes were not waste water. This was Chile&rsquo;s investigation, not the U.S. AARO&rsquo;s, and I found no AARO statement on it.<br><a href=\"https://www.twz.com/6852/the-chilean-military-has-no-idea-what-this-flying-object-is\" target=\"_blank\" rel=\"noopener\">The War Zone report</a> &middot; <a href=\"https://www.theblackvault.com/casefiles/documents-released-on-the-november-11-2014-chilean-navy-helicopter-ufo-encounter/amp/\" target=\"_blank\" rel=\"noopener\">Documents released on the case</a></p>\n"
 "<p class=\"meta\">Skeptics, including Metabunk and Skeptoid, think it was a passenger airliner leaving Santiago&rsquo;s airport, with the plumes being exhaust or condensation. I list that so you can weigh both.<br><a href=\"https://skeptoid.com/episodes/4838\" target=\"_blank\" rel=\"noopener\">Skeptoid</a></p>\n"
 '<h2>Public record on GitHub</h2>\n<p class="meta">The exact text of every prediction is also kept in this site&rsquo;s public source repository, so anyone can read it, compare it with the fingerprints above, and see when each version was committed.</p>\n<ul class="meta" style="list-style:none;padding:0"><li><b>The predictions as first written</b><br><a href="https://github.com/keithadler/thisisdisclosure-site/blob/main/content/predictions.txt" target="_blank" rel="noopener">The file</a> &middot; <a href="https://raw.githubusercontent.com/keithadler/thisisdisclosure-site/main/content/predictions.txt" target="_blank" rel="noopener">Raw text</a> &middot; <a href="https://github.com/keithadler/thisisdisclosure-site/commits/main/content/predictions.txt" target="_blank" rel="noopener">Commit history</a></li><li><b>Added later, 1</b><br><a href="https://github.com/keithadler/thisisdisclosure-site/blob/main/content/predictions-added-1.txt" target="_blank" rel="noopener">The file</a> &middot; <a href="https://raw.githubusercontent.com/keithadler/thisisdisclosure-site/main/content/predictions-added-1.txt" target="_blank" rel="noopener">Raw text</a> &middot; <a href="https://github.com/keithadler/thisisdisclosure-site/commits/main/content/predictions-added-1.txt" target="_blank" rel="noopener">Commit history</a></li><li><b>Added later, 2</b><br><a href="https://github.com/keithadler/thisisdisclosure-site/blob/main/content/predictions-added-2.txt" target="_blank" rel="noopener">The file</a> &middot; <a href="https://raw.githubusercontent.com/keithadler/thisisdisclosure-site/main/content/predictions-added-2.txt" target="_blank" rel="noopener">Raw text</a> &middot; <a href="https://github.com/keithadler/thisisdisclosure-site/commits/main/content/predictions-added-2.txt" target="_blank" rel="noopener">Commit history</a></li><li><b>Added later, 3: the falsifier</b><br><a href="https://github.com/keithadler/thisisdisclosure-site/blob/main/content/predictions-added-3.txt" target="_blank" rel="noopener">The file</a> &middot; <a href="https://raw.githubusercontent.com/keithadler/thisisdisclosure-site/main/content/predictions-added-3.txt" target="_blank" rel="noopener">Raw text</a> &middot; <a href="https://github.com/keithadler/thisisdisclosure-site/commits/main/content/predictions-added-3.txt" target="_blank" rel="noopener">Commit history</a></li></ul>\n<p class="meta">To check one yourself: <code>curl -s RAW_URL | shasum -a 256</code> should print the same fingerprint shown above for that text. New predictions are committed there as they are added.</p>\n<p class="meta">The repository was recreated on 26 October 2026 to clean up its history, so its commit log starts then. The fingerprints on this page and the Internet Archive snapshots are the longer record.</p>\n'
 "<h2>Version history</h2>\n<p class=\"meta\">26 October 2026: this page was first posted a few minutes earlier with the last line reading &ldquo;I am giving no dates, and I do not expect either soon.&rdquo; (SHA-256 cab5588d43f37108a1f51c1cdb1361bade964582fcf303dc93954a8432e64ca8). That line misstated my meaning, so I replaced it with the text above, which says I expect all of it in the near term. Nothing else changed.</p>\n<p class=\"meta\">26 October 2026: prediction 3 was first posted a few minutes earlier as &ldquo;We will be told that we are a curated species.&rdquo; (SHA-256 6ea4eb20ce68bd3329b149dbf073797b49adc25b2c5d91c210235b06294a2cb3). I extended it to add &ldquo;on a managed preserve.&rdquo; The mist speculation below it was added at the same time and was not changed.</p>\n")
open("public/predictions.html","w").write(_pg+"\n"+_pbody+"</main></body></html>\n")

# --- cheat sheets: one hub and five practical one-pagers (secular, plain, no claims beyond "I think") ---
import html as _h3
_CS={
 "everyday":("Everyday life","Cheat sheet for everyday life","Most of the test is small, public and over in five seconds.",
  [("Move in the first five seconds.","When you see someone struggling (bags, a stroller, lost, crying), you have about five seconds before the moment passes. Go. Say: \"Can I help with that?\""),
   ("Pay for a stranger and leave.","Coffee, a meal, a bus fare. Be gone before they can thank you. Nothing comes back. That is the point."),
   ("Be the paramedic.","If someone is hurt in public, go toward them, call for help and stay until help arrives. Don't ask about the crime, the person or your training."),
   ("Return what isn't yours.","The wallet, the phone, the extra change. Leave a note: \"Found by someone who hoped you would get this back.\""),
   ("Let the other person finish.","With someone you disagree with, repeat back what they said before you answer. Say: \"So what you're saying is...\""),
   ("Treat the one who can do nothing for you like the one who can.","The waiter, the janitor, the intern, the stranger. Same voice, same eye contact, same patience."),
   ("Do one kindness a day that nobody sees.","Then notice what it does to your heart. That lift is the sign it was never for nothing.")],
  "One kindness a day that nobody sees.",""),
 "elders":("Elders","Cheat sheet for elders","You have time and stories, the two things everyone else is short of.",
  [("Be the one who notices.","Learn the name of the cashier, the bus driver, the neighbor's kid. Use it. Say: \"How is your day going, really?\" and wait for the whole answer."),
   ("Make the call nobody makes.","Every week, call one person who is alone. Say: \"I was thinking about you.\" Have no agenda."),
   ("Give the lesson away.","Offer a skill (cooking, fixing, saving money, getting through a bad year) to someone younger, free. Say: \"Want me to show you?\""),
   ("Tell the real story.","Share one time you were badly wrong and what it cost. Say: \"Here is what I would do differently.\" Honest beats impressive."),
   ("Give it now, not later.","Hand over the thing you are saving (a tool, a book, money) to someone who needs it today. Don't attach a story to it."),
   ("Stay with the grieving.","Don't fix it. Sit. Say: \"I'm here. I'm not going anywhere.\""),
   ("Close one old account.","Forgive or apologize for one old thing. Say it, or if saying it isn't safe, write it down and let the page take it.")],
  "One call, one gift, one apology.",""),
 "teens":("For your teens","Cheat sheet for your teens","Remember: this site is 18+ only. This sheet is for you to read and hand to your teens, not for them to browse the site. They are not too young for the practice. They may be the best at it, because they haven't learned to look away yet.",
  [("Sit with the one who is alone.","Lunch, the bus, a party. Say: \"Mind if I sit here?\" That is the whole move."),
   ("Be the \"that's enough.\"","When a group piles on someone, you don't have to win. Say: \"Okay, that's enough,\" or just don't laugh. One person not laughing changes the room."),
   ("Defend them in private if public is too hard.","Message them: \"That wasn't okay. I'm sorry nobody said it.\""),
   ("Do one invisible kindness.","No post, no screenshot. Do it, then notice what it does to your chest. That is data."),
   ("Give one conversation your whole attention.","Phone face down. Ask: \"What's the hardest part of this week?\" Listen to the end."),
   ("Say a specific thank-you.","To a teacher or a parent: \"When you ___, it changed ___.\""),
   ("Tell the truth when lying is free.","Say: \"Actually, that was me.\" Do it even when no one would ever know."),
   ("Give the credit away.","Say: \"That was her idea.\" Let it belong to the group.")],
  "Sit with someone, stand up for someone, thank someone.",
  "If someone is being hurt, tell a trusted adult. You do not have to handle it alone, and not every hardship is a test."),
 "parents":("Parents","Cheat sheet for parents","Children learn what humans are by watching you. The test starts at the kitchen table.",
  [("Be the example, out loud.","Narrate your kindness as you do it. Say: \"I'm giving this man my seat because his legs are tired.\" Kids copy what they see, not what you tell them."),
   ("Praise the kindness, not the child.","Say: \"That was kind of you to share.\" Not: \"You're so good.\" A kind act is something they did and can do again."),
   ("Make one unseen kindness a family habit.","Once a week, do something nobody will see: leave groceries, shovel a neighbor's walk. Don't post it. Talk about how it felt."),
   ("Teach them to be the \"that's enough.\"","Practice the line: \"Okay, that's enough.\" Role-play it. Tell them you will always back them up for using it."),
   ("Teach them to go toward the hurt person.","When someone falls, ask: \"What could we do?\" Then do it together. Make \"toward, not away\" the family rule."),
   ("Apologize first, and be specific.","When you lose your temper, say: \"I yelled, and that wasn't okay. I'm sorry.\" Kids who see repair learn repair."),
   ("Give chores that serve people outside your house.","Not only their own room. A neighbor's bins, a grandparent's groceries. Let them feel what it is to be needed."),
   ("Keep your small promises.","If you say \"in five minutes,\" mean five. Trust is built out of small promises kept."),
   ("Ask the question at dinner.","\"Where did you see someone being a human being today?\" And: \"Where did you get to be one?\""),
   ("Put their safety first.","Teach them to tell a trusted adult when someone is being hurt. Courage is not the same as handling it alone.")],
  "One unseen kindness together. One \"that's enough\" practiced. One apology said plainly.",
  "You don't have to do this perfectly. You will get it wrong. Repair counts more than perfection."),
 "leaders":("People in charge","Cheat sheet for people in charge","The test asks more of you: more people can see you, and fewer will tell you the truth.",
  [("Choose on merit, out loud.","Put the qualified person in the job, not your friend or relative. Be able to say to the runner-up's face: \"I chose them because...\""),
   ("Own the miss, publicly.","Say: \"That was my call. It was wrong. Here is the fix.\" Give the credit away in the same room."),
   ("Deliver bad news early.","Say: \"You would want to know this today, so I'm telling you today.\""),
   ("Hear the lowest-status person first.","Say: \"Before I weigh in, Sam, what are you seeing?\""),
   ("Share what you know.","Default to open. Ask: \"Who is hurt by not knowing this?\""),
   ("Reward the one who disagrees.","Say: \"Thank you for telling me I'm wrong.\" Then change something visible."),
   ("Pay fairly. Never profit from desperation.","If the deal only works because the other side has no choice, it's the wrong deal."),
   ("Offer the first step toward peace.","Say: \"I'll move first if you move second.\" Do it before you are forced to."),
   ("Run the stranger test.","Would you make this decision if the person it hurts could watch you make it?"),
   ("Know when to step aside.","If someone else would do it better, make room, and help them start.")],
  "One hard truth told early. One credit given away. One first step toward peace.",""),
 "inside":("Inside","Cheat sheet for people in prison","You can't control much in there. You can control what you show. Pick acts that are safe for you, and put your safety first.",
  [("Protect the new person.","The first week is the hardest. Show them where things are. Say: \"Here is how this place works. Ask me anything.\""),
   ("Don't join the pile-on.","When the block turns on someone, you don't have to speak up and you don't have to laugh. Walk away. A quiet refusal counts."),
   ("Share what you have.","A stamp, a soup, a phone minute. Give it without making it a debt. Say: \"You don't owe me anything.\""),
   ("Teach one thing.","Reading, math for the GED, a trade, a language. Say: \"Sit with me twenty minutes a day.\""),
   ("Write or read for someone who can't.","Letters, forms, appeals. Do it free, and keep what they tell you private."),
   ("Keep your word on small things.","Show up when you said you would. Return what you borrowed. Trust is built in inches."),
   ("Take responsibility without excuses.","Say what you did, in plain words, to yourself first. Use the programs that let you do this safely. Never contact a victim on your own."),
   ("Answer harm without more harm.","When someone disrespects you, take one breath. Say: \"We're good.\" Walk if you can. Revenge is the cheapest move there is."),
   ("Write the letter you'll send out.","To your family, or to the person you hurt if they have asked for contact through a program. Write it even if you never mail it.")],
  "One person helped, one word kept, one letter written.",
  "Safety comes first. Choose acts that won't put you at risk, and talk to a counselor or case manager if you can."),
 "fallen":("Second chance","Cheat sheet for people who haven't held up their end","Broken promises, unpaid debts, missing from someone's life. It isn't too late, and it starts smaller than you think.",
  [("Say it plainly.","Name what you didn't do. Say: \"I said I would, and I didn't. That's on me.\" No \"but.\""),
   ("Promise small, then keep it.","A text on Sunday. Five dollars a week. Pick something you can't fail at, and don't fail it."),
   ("Make a repayment plan, however tiny.","Five dollars a month is a plan. Silence isn't. Say: \"I can pay this much, starting on the first.\""),
   ("Show up when it's inconvenient.","The unglamorous hour counts: the pickup, the hospital, the funeral. Be early."),
   ("Ask what would help, then do that.","Not what you would like to give. Say: \"What would actually help?\" Then do the boring thing."),
   ("Take it without defending yourself.","If they are still angry, don't argue. Say: \"You have every right to be. I'm still here.\""),
   ("Let them set the pace.","Forgiveness belongs to them. Don't ask for it. Be someone it is safe to forgive."),
   ("Do one quiet good deed nobody will connect to you.","It rebuilds the part of you that believes you can do it."),
   ("Repeat for ninety days.","One missed day doesn't undo a streak. Stopping does.")],
  "One honest sentence. One small promise. One promise kept.",""),
 "meaning":("Building meaning","Cheat sheet for building a life that matters","Meaning is rarely found. It is built, one repeated act at a time, usually with other people.",
  [("Pick one person for a year.","Someone with less than you: a neighbor, a kid, a struggling colleague. Be reliably good to them for twelve months."),
   ("Show up weekly, locally.","A food bank, tutoring, hospice visits, a neighbor. Not a screen. The same place, the same hour."),
   ("Give one thing away unseen. Log how it felt.","One line in a notebook after each. After thirty days, read the log."),
   ("Make amends with one person.","Say: \"I was wrong, and I'm sorry. What would help?\""),
   ("Write three specific thank-yous a week.","Say what they did and what it changed. Send at least one."),
   ("Build something that outlives you.","Teach someone, mentor, plant something, write down what you know."),
   ("Don't start a movement. Start with your street.","Know your neighbors' names before you try to change the world."),
   ("End each week with two questions.","What did I give? What did I take? Adjust.")],
  "One person, one problem, one thing given away unseen.",""),
}
_hc=open("content/sources-head.html").read()
def _page(slug,title,desc,body):
    h=_hc.replace("<title>Sources | This Is Disclosure</title>","<title>"+_h3.escape(title)+" | This Is Disclosure</title>")
    h=h.replace('<meta name="description" content="Sources for the quotations on This Is Disclosure.">','<meta name="description" content="'+_h3.escape(desc,quote=True)+'">\n<meta property="og:title" content="'+_h3.escape(title,quote=True)+'">\n<meta property="og:description" content="'+_h3.escape(desc,quote=True)+'">\n<meta property="og:image" content="https://thisisdisclosure.com/og-card.png?v=2">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="https://thisisdisclosure.com/og-card.png?v=2">')
    h=h.replace('<link rel="canonical" href="https://thisisdisclosure.com/sources">','<link rel="canonical" href="https://thisisdisclosure.com/'+slug+'">')
    assert slug in h
    h=h.replace("</style></head>","  ol.cs { padding-left: 1.4em; } ol.cs li { margin-bottom: .75em; } .week { margin: 2rem 0 1rem; padding: 1.1rem 1.2rem; border-top: 2px solid var(--ink); border-bottom: 1px solid var(--ink); font-weight:700; } .week small { display:block; font: 700 .7rem ui-monospace,Menlo,monospace; letter-spacing:.22em; text-transform:uppercase; opacity:.65; margin-bottom:.3em; } .evbtn { display:inline-block; border:2px solid var(--ink); padding:.7em 1.2em; text-decoration:none; font: 700 1rem ui-monospace,Menlo,monospace; letter-spacing:.08em; word-break:break-all; } .evbtn:hover { background:var(--ink); color:var(--bone); } .hub a.card { display:block; text-decoration:none; padding: 1.1rem 0; border-top:1px solid color-mix(in srgb,var(--ink) 30%,transparent); } .hub a.card b { display:block; font-size: clamp(1.3rem,3.4vw,1.8rem); } .hub a.card span { opacity:.75; font-size: clamp(1rem,2.2vw,1.15rem); } @media print { header, .noprint { display:none; } body { background:#fff; } }\n</style></head>",1)
    open("public/"+slug+".html","w").write(h+"\n"+body+"</main></body></html>\n")
import cheat_pages
for slug,vals in _CS.items():
    _page("cheat-sheet-"+slug,vals[1],vals[2],cheat_pages.sheet(slug,vals,pic,_CS))
_hub=(cheat_pages.hub(_CS,pic)+
 "<h2>Why these</h2>\n<p class=\"meta\">Giving is not for nothing. In controlled studies, people who spent money on others reported more happiness than people who spent it on themselves, and a later cross-cultural study found the same pattern across many countries. That is the lift, measured.<br>"
 "<a href=\"https://doi.org/10.1126/science.1150952\" target=\"_blank\" rel=\"noopener\">Dunn, Aknin and Norton, Science, 2008</a> &middot; "
 "<a href=\"https://doi.org/10.1037/a0031578\" target=\"_blank\" rel=\"noopener\">Aknin and colleagues, Journal of Personality and Social Psychology, 2013</a> &middot; "
 "<a href=\"https://doi.org/10.1207/s15327558ijbm1202_4\" target=\"_blank\" rel=\"noopener\">Post, International Journal of Behavioral Medicine, 2005</a></p>\n"
 "<p class=\"meta\">Not every hardship is a test, and nothing here asks anyone to stay where they are being hurt. If you are struggling, please talk to someone you trust. In the US you can call or text 988. Elsewhere, <a href=\"https://findahelpline.com/\" target=\"_blank\" rel=\"noopener\">findahelpline.com</a> lists services by country.</p>\n")
_page("cheat-sheets","Cheat sheets","If you only do one thing, take the cheat sheet: plain, practical one-pagers for elders, your teens (18+ site, so for parents to hand over), everyday life, people in charge, and people building meaning.",_hub)

import prove_me_wrong
_page("prove-me-wrong","What would prove me wrong","If a higher intelligence is not acknowledged by a major world power by the end of 2028, I am wrong. Where to check.",prove_me_wrong.body())


_fg=_FG.load()
if _fg:
    for _s,_d in _fg.items():
        _page("guide-"+_s,"A guide for "+(_d["who"][0].lower()+_d["who"][1:] if _d["who"].startswith("People") else _d["who"]),_d["idea"],_FG.page(_s,_d,pic,_fg))
    _page("faith-guides","Guides by tradition","Where many traditions already hold ideas close to this one, in their own public-domain texts.",_FG.hub(_fg,pic))


_cg=_CG.load()
if _cg:
    for _s,_d in _cg.items():
        _page("country-"+_s,_d["name"]+": the law and helping strangers",_d["summary"],_CG.page(_s,_d,pic,_cg))
    _page("country-guides","Country guides","What each government and legal system does about helping strangers: duty to help, protection for helpers, and how giving is promoted.",_CG.hub(_cg,pic))


for _sl in [x[0] for x in _SH.SIGNS]:
    open("public/sign-"+_sl+".html","w").write(_SH.sign_page(_sl,pic))
_page("share","Share the message","Print a sign, send a line, start a ten-minute conversation: ways to carry the message a little further.",_SH.body(pic))

# --- the Evidence Room: documented anonymous good, and a call for stories (email assembled by script, not in the HTML) ---
import evidence_page
_ev=(evidence_page.build(pic)+evidence_page.submit()+
 "<p class=\"meta\"><a href=\"/cheat-sheets\">Cheat sheets</a> &middot; <a href=\"/faith-guides\">Guides by tradition</a> &middot; <a href=\"/country-guides\">Country guides</a> &middot; <a href=\"/\">thisisdisclosure.com</a></p>\n")
EVIDENCE_LIVE=os.path.exists("content/evidence-live")
if EVIDENCE_LIVE: _page("evidence-room","The Evidence Room","People doing good without being seen and without taking credit: documented cases, and a place to send yours.",_ev)

import json as _json
def _cs_img(s):
    m=re.search(r'srcset="([^"]*?(/art/[^ ",]+\.640\.webp)) 640w',pic(cheat_pages.ART[s],True,True,"")); return m.group(2) if m else ""
_cs_json=_json.dumps({s:{"tab":v[0],"title":v[1],"img":_cs_img(s),"lede":v[2],"items":[{"do":d,"how":w} for d,w in v[3]],"week":v[4],"note":v[5]} for s,v in _CS.items()},ensure_ascii=False).replace("</","<\\/")
_ix=open("public/index.html").read()
assert "%%CHEAT%%" in _ix
_ix=_ix.replace("%%CHEAT%%",_cs_json)
if not EVIDENCE_LIVE: _ix=_ix.replace('<a class="ft" href="/evidence-room">Evidence room</a>',"")
if not _fg: _ix=_ix.replace('<a class="ft" href="/faith-guides">Faith guides</a>',"")
if not _cg: _ix=_ix.replace('<a class="ft" href="/country-guides">Country guides</a>',"")
open("public/index.html","w").write(_ix)
if not EVIDENCE_LIVE and os.path.exists("public/evidence-room.html"): os.remove("public/evidence-room.html")
print("sources page:",len(seen),"quotations")
