"""The Share page: printable signs with a QR code, ready-to-send words, share links, social images and a way to talk about it."""
import html, os

E = lambda s: html.escape(s, quote=True)
SITE = "https://thisisdisclosure.com"
SIGNS = [
 ("treat", "Treat each other like humans.", "If I held a sign on a street corner, this is what it would say.", "sign", "A person holds a sign on a street corner."),
 ("question", "Is this what a human being does?", "Carry one question into everything you do.", "stop", "A man turns back to help an old man sitting against a wall."),
 ("paramedic", "We are all paramedics.", "We do not care about the crime, the person, or our training. We help.", "medics", "A ring of ordinary people kneel around a person on the pavement and help."),
 ("unseen", "Do one good thing when no one is watching.", "Then notice that nothing came back, and that it was never for nothing.", "unseen", "A passerby leaves bread on a stranger's doorstep at night and walks away unseen."),
 ("case", "You're in the case. You always were.", "There is still time. The test is still running.", "subway", "A woman in a crowded subway car."),
 ("door", "Hold the door. Pay for a stranger. Give up your seat.", "Small, public, and over in five seconds.", "grace", "Strangers helping one another on a busy street."),
]
ART = {f"sg_{s}": a for s, _, _, a, _ in SIGNS}

SIGN_CSS = """<style>
@page{size:Letter;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#f1ede4;color:#0a0a0a;font-family:"Playfair Display",Georgia,serif}
.sg{width:8.5in;min-height:11in;margin:0 auto;padding:.55in .6in .45in;display:flex;flex-direction:column;background:#f1ede4}
.sk{font:700 11pt ui-monospace,Menlo,monospace;letter-spacing:.34em;text-transform:uppercase;text-align:center;margin-bottom:.25in}
.sh{font:900 52pt/1.0 "Playfair Display",Georgia,serif;letter-spacing:-.02em;text-align:center;margin:0 0 .2in}
.sg picture img{display:block;width:100%;height:auto;border:1.5pt solid #0a0a0a}
.sh.long{font-size:42pt}.sh.xl{font-size:36pt}
.ss{font:600 19pt/1.35 "Playfair Display",Georgia,serif;text-align:center;margin:.22in .3in 0}
.sf{margin-top:auto;padding-top:.3in;display:flex;align-items:center;justify-content:space-between;gap:.3in;border-top:2pt solid #0a0a0a}
.sf img.qr{width:1.35in;height:1.35in;border:0}
.sf .u{font:900 26pt/1.1 "Playfair Display",Georgia,serif}
.sf .d{font:700 11pt ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;margin-top:.08in}
@media screen{body{background:#ddd7c8}.sg{margin:1rem auto;box-shadow:0 10px 40px -12px rgba(0,0,0,.5)}}
@media (max-width:8.6in) and (screen){.sg{width:100%;min-height:0;padding:1.2rem}.sh{font-size:2.4rem}.ss{font-size:1.1rem}.sf .u{font-size:1.3rem}.sf img.qr{width:6rem;height:6rem}}
</style>"""

def sign_page(slug, pic):
    s = next(x for x in SIGNS if x[0] == slug)
    _, head, sub, art, alt = s
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<meta name="robots" content="noindex"><title>{E(head)} | This Is Disclosure</title>'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
            '<style>@font-face{font-family:"Playfair Display";font-style:normal;font-weight:400 900;font-display:swap;src:url(/fonts/pf-latin.woff2) format("woff2")}</style>'
            + SIGN_CSS + '</head><body><div class="sg">'
            '<div class="sk">This Is Disclosure</div>'
            f'<h1 class="sh{" xl" if len(head)>46 else (" long" if len(head)>28 else "")}">{E(head)}</h1>'
            + pic(f"sg_{slug}", True, True, E(alt), True) +
            f'<p class="ss">{E(sub)}</p>'
            '<div class="sf"><div><div class="u">thisisdisclosure.com</div><div class="d">November 13th &middot; For adults, 18 and over</div></div>'
            '<img class="qr" src="/share/qr.svg" alt="QR code for thisisdisclosure.com"></div>'
            '</div></body></html>\n')

MESSAGES = [
 ("One line", "Treat each other like humans. thisisdisclosure.com"),
 ("Short", "A message for everyone, 18 and over: how we treat each other may be what counts most, especially when nobody is watching and nothing comes back. One person's hypothesis, not a demand. thisisdisclosure.com"),
 ("Longer", "I came across a site with one question on it: Is this what a human being does? It argues that how we treat each other, especially strangers and especially unseen, may be what is being measured. It is a hypothesis, it asks for nothing, and it has plain cheat sheets for elders, teens, parents and everyone else. Take a look when you have ten minutes: https://thisisdisclosure.com"),
]

STYLE = """<style>
.shw{width:min(1000px,calc(100vw - 44px));position:relative;left:50%;transform:translateX(-50%)}
.shw h1{font-size:clamp(2.4rem,9vw,4.6rem);line-height:.98;margin:0 0 .3em}
.shw h2{font-size:clamp(1.5rem,5vw,2.1rem);margin:2.8rem 0 .4rem}
.shw .lede{font-size:1.2rem;max-width:36em}
.shb{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0}
.shb a,.shb button{font:700 .78rem ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--ink);background:transparent;border:2px solid var(--ink);border-radius:999px;padding:.7em 1.1em;cursor:pointer}
.shb .pr{background:var(--ink);color:var(--bone)}
.shb a:hover,.shb button:hover{background:var(--ink);color:var(--bone)}
.shl{display:flex;gap:.7rem;align-items:center;flex-wrap:wrap;border:2px solid var(--ink);border-radius:14px;padding:1rem 1.2rem;background:var(--card)}
.shl code{font:700 1.2rem ui-monospace,Menlo,monospace;word-break:break-all}
.sgg{display:grid;gap:1.2rem;grid-template-columns:1fr}
@media(min-width:760px){.sgg{grid-template-columns:1fr 1fr}}
.sgc{border:2px solid var(--ink);border-radius:14px;overflow:hidden;background:var(--card);display:flex;flex-direction:column}
.sgc img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;background:#fff}
.sgc .cb{padding:1rem 1.2rem 1.2rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
.sgc b{font:900 1.4rem/1.15 "Playfair Display",Georgia,serif}
.sgc span.d{opacity:.8;font-size:.95rem}
.msg{border-left:4px solid var(--ink);padding:.2rem 0 .2rem 1rem;margin:1rem 0}
.msg .k{font:700 .66rem ui-monospace,Menlo,monospace;letter-spacing:.22em;text-transform:uppercase;opacity:.65}
.msg p{margin:.3rem 0 .6rem}
.shim{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:1rem 0}
.shim figure{margin:0;border:2px solid var(--ink);border-radius:12px;overflow:hidden;background:var(--card)}
.shim img{display:block;width:100%;height:auto;background:#fff}
.shim figcaption{padding:.7rem .9rem;font:700 .72rem ui-monospace,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase}
.shim figcaption a{color:inherit}
.shr{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin:1rem 0}
.shr a{display:block;text-decoration:none;color:inherit;border:2px solid var(--ink);border-radius:12px;padding:.9rem 1.1rem;background:var(--card)}
.shr a:hover{box-shadow:0 12px 24px -14px rgba(0,0,0,.55)}
.shr b{display:block;font:800 1.15rem/1.25 "Playfair Display",Georgia,serif}
.shr span{display:block;font-size:.95rem;opacity:.8;margin-top:.2rem}
.shq{margin:1.6rem 0;padding:1.4rem 1.5rem;background:var(--ink);color:var(--bone);border-radius:16px}
.shq div{font:800 clamp(1.3rem,4vw,1.9rem)/1.25 "Playfair Display",Georgia,serif}
.shq small{display:block;margin-top:.7rem;font:700 .68rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.65}
.shn{font-size:.95rem;opacity:.85}
.shw ol.talk li{margin:.6em 0}
</style>"""

def body(pic):
    cards = ""
    for slug, head, sub, art, alt in SIGNS:
        cards += (f'<div class="sgc">{pic("sg_" + slug, True, True, E(alt))}<div class="cb"><b>{E(head)}</b><span class="d">{E(sub)}</span>'
                  f'<div class="shb"><a class="pr" href="/pdf/sign-{slug}.pdf" download>Download PDF</a><a href="/sign-{slug}" target="_blank" rel="noopener">Open and print</a></div></div></div>')
    msgs = "".join(f'<div class="msg"><div class="k">{E(k)}</div><p id="m{i}">{E(t)}</p><div class="shb"><button type="button" data-copy="m{i}">Copy</button></div></div>' for i, (k, t) in enumerate(MESSAGES))
    return (STYLE + '<div class="shw"><div class="cseye" style="font:700 .72rem ui-monospace,Menlo,monospace;letter-spacing:.26em;text-transform:uppercase;opacity:.7">Share the message</div>'
      '<h1>Carry it a little further.</h1>'
      '<p class="lede">Nothing here asks you to join anything. If it rings true, tell one person. Print a sign, send a line, start a ten-minute conversation, and let the message do the rest.</p>'
      '<h2>The link</h2>'
      f'<div class="shl"><code id="shlink">{SITE}</code><div class="shb" style="margin:0"><button type="button" class="pr" id="shcopy">Copy link</button><button type="button" id="shnative" hidden>Share&hellip;</button></div></div>'
      '<div class="shb" id="shfallback">'
      f'<a href="mailto:?subject={E("Is this what a human being does?")}&body={E("Treat each other like humans. " + SITE)}">Email</a>'
      f'<a href="sms:?&body={E("Treat each other like humans. " + SITE)}">Text message</a>'
      f'<a href="https://wa.me/?text={E("Treat each other like humans. " + SITE)}" target="_blank" rel="noopener">WhatsApp</a>'
      f'<a href="https://twitter.com/intent/tweet?text={E("Treat each other like humans.")}&amp;url={E(SITE)}" target="_blank" rel="noopener">Post on X</a>'
      f'<a href="https://www.facebook.com/sharer/sharer.php?u={E(SITE)}" target="_blank" rel="noopener">Facebook</a></div>'
      '<h2>Print a sign</h2>'
      '<p>Six one-page signs, each with a woodcut, the line, and a QR code that opens this site. Print them at home or at a library, post them on a bulletin board, a window or a classroom wall, and hand them out. Ask permission where it is needed.</p>'
      f'<div class="sgg">{cards}</div>'
      '<h2>Words to send</h2><p>Use them as they are, or say it your way.</p>' + msgs +
      '<h2>Pictures for your feed</h2><p>Three sizes of the same card.</p>'
      '<div class="shim">'
      '<figure><img src="/share/card-square.png" alt="Square card: This Is Disclosure" loading="lazy"><figcaption><a href="/share/card-square.png" download>Square, 1080 x 1080</a></figcaption></figure>'
      '<figure><img src="/share/card-story.png" alt="Story card: This Is Disclosure" loading="lazy"><figcaption><a href="/share/card-story.png" download>Story, 1080 x 1920</a></figcaption></figure>'
      '<figure><img src="/og-card.png" alt="Wide card: This Is Disclosure" loading="lazy"><figcaption><a href="/og-card.png" download>Wide, 1200 x 630</a></figcaption></figure></div>'
      '<h2>Start a ten-minute conversation</h2>'
      '<p>For a kitchen table, a classroom, a staff meeting or a congregation. You do not need to believe the hypothesis to have this conversation.</p>'
      '<ol class="talk"><li>Ask the group the one question: <i>Is this what a human being does?</i></li>'
      '<li>Ask for one real example from the last week, big or small, of someone doing good with nothing expected back.</li>'
      '<li>Read one of the <a href="/cheat-sheets">cheat sheets</a> that fits the room, and let each person pick one thing to do this week.</li>'
      '<li>Next time, ask how it went. Do not rank anyone or keep score.</li></ol>'
      '<h2>Resources to hand out</h2><div class="shr">'
      '<a href="/cheat-sheets"><b>Cheat sheets</b><span>Plain one-pagers, each with a PDF checklist.</span></a>'
      '<a href="/faith-guides"><b>Guides by tradition</b><span>Where many faiths and philosophies already hold the idea.</span></a>'
      '<a href="/country-guides"><b>Country guides</b><span>What the law and the government do about helping strangers.</span></a>'
      '<a href="/evidence-room"><b>The Evidence Room</b><span>Documented cases of unseen kindness, each with sources.</span></a>'
      '<a href="/how-to-cheat-on-the-test"><b>How to cheat on the test</b><span>The whole answer key in a minute.</span></a>'
      '<a href="/prove-me-wrong"><b>What would prove me wrong</b><span>The honest test of the whole idea.</span></a></div>'
      '<h2>The collective destiny</h2>'
      '<div class="shq"><div>Nobody has been written off, and the door is still open.</div><small>My belief, from the FAQ: we are almost through the test and passing it</small></div>'
      '<p>That is what the message is for: not fear, and not a club, but a shared direction. Every person who treats a stranger like a human being moves it a little. Share it in a way you would be proud of, never to pressure or frighten anyone.</p>'
      '<h2>Share it well</h2><ul class="shn">'
      '<li>This site is for adults, 18 and over. Do not share it with children; the page for teens is written for a parent to hand over.</li>'
      '<li>It is a hypothesis, not a demand and not a prediction you should act on. Say so when you share it.</li>'
      '<li>Nothing is for sale and there is nothing to join. Be wary of anyone who says otherwise in this name. The only official site is thisisdisclosure.com.</li>'
      '<li>No named person or institution has endorsed it. Please do not say they have.</li></ul>'
      '<p class="meta"><a href="/disclaimer">Disclaimers</a> &middot; <a href="/">thisisdisclosure.com</a></p></div>'
      '<script>(function(){var L="' + SITE + '",c=document.getElementById("shcopy"),n=document.getElementById("shnative");'
      'function cp(t,b){var d=function(){var o=b.textContent;b.textContent="Copied";setTimeout(function(){b.textContent=o;},1500);};'
      'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(d,function(){});}else{var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");d();}catch(e){}a.remove();}}'
      'c.addEventListener("click",function(){cp(L,c);});'
      'document.querySelectorAll("[data-copy]").forEach(function(b){b.addEventListener("click",function(){cp(document.getElementById(b.dataset.copy).textContent,b);});});'
      'if(navigator.share){n.hidden=false;n.addEventListener("click",function(){navigator.share({title:"This Is Disclosure",text:"Treat each other like humans.",url:L}).catch(function(){});});}'
      '})();</script>')
