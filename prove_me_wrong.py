"""/prove-me-wrong: the falsifier in plain words, and a short, grouped list of places to check it."""
import html
E = lambda s: html.escape(s, quote=True)

GROUPS = [
 ("Official sources", "Where an acknowledgment would appear first. Start here.", "official", [
  ("War Department UFO files", "https://www.war.gov/UFO/", "The U.S. government's own release page for declassified UAP records."),
  ("AARO, the Pentagon's UAP office", "https://www.aaro.mil/", "The office that investigates UAP reports for the Department of Defense."),
  ("NASA's UAP page", "https://science.nasa.gov/uap/", "NASA's independent study and what it says about the data."),
  ("NASA UAP Independent Study Team final report (PDF)", "https://science.nasa.gov/wp-content/uploads/2023/09/uap-independent-study-team-final-report.pdf", "The full 2023 report."),
  ("National Archives: UAP records", "https://www.archives.gov/research/topics/uaps", "Federal records on UAP, kept by the National Archives."),
  ("House Oversight hearing on UAP (July 2023)", "https://oversight.house.gov/hearing/unidentified-anomalous-phenomena-implications-on-national-security-public-safety-and-government-transparency/", "Sworn testimony before Congress."),
  ("Congressional Record: UAP Disclosure Act text (July 2023)", "https://www.congress.gov/118/crec/2023/07/13/169/120/CREC-2023-07-13-pt1-PgS2953.pdf", "The bill as introduced in the Senate."),
 ]),
 ("What has happened so far", "The trail up to now, in news reports. None of it is an acknowledgment.", "news", [
  ("Navy officially releases the infamous UFO videos", "https://www.twz.com/33179/navy-officially-releases-infamous-ufo-videos", "The Navy confirmed three videos were real and calls the objects unidentified."),
  ("NASA UAP report: what it found", "https://www.cbsnews.com/news/nasa-ufo-report-uap-study/", "A news summary of the 2023 NASA study."),
  ("The UAP Disclosure Act of 2023", "https://thedebrief.org/the-uap-disclosure-act-of-2023-what-we-know-about-chuck-schumer-and-the-senates-new-push-for-uap-transparency/", "The Senate proposal to require release of UAP records."),
  ("Congress dives into UFOs in a hearing with eyewitness testimony", "https://techcrunch.com/2023/07/26/congress-dives-into-ufos-in-a-hearing-featuring-eyewitness-testimony/", "A report on the 2023 hearing."),
  ("War Department declassifies UAP documents", "https://www.washingtonexaminer.com/news/white-house/4560458/war-department-declassifies-uap-documents-after-long-fueled-justified-speculation.", "The release of UAP files by the Department of War."),
  ("Trump UFO file dump includes military footage", "https://www.foxnews.com/politics/trump-ufo-file-dump-includes-military-footage-mysterious-star-shaped-object", "A report on one batch of released files."),
 ]),
 ("The skeptics", "Read these too. If they are right, I get no credit for it.", "skeptic", [
  ("Director of Pentagon's UAP investigations challenges hearing claims", "https://thedebrief.org/director-of-pentagons-uap-investigations-challenges-claims-made-in-recent-uap-hearing/", "AARO's director on what the 2023 testimony did not show."),
  ("Metabunk: the Gimbal UFO claims", "https://www.metabunk.org/threads/the-gimbal-ufo-marik-claims-new-findings-falsify-prosaic-explanations.14839/", "A skeptical analysis of one of the Navy videos."),
 ]),
]

STYLE = """<style>
.pw{width:min(900px,calc(100vw - 44px));position:relative;left:50%;transform:translateX(-50%)}
.pwt{font-size:clamp(2.4rem,9vw,4.4rem);line-height:1;margin:0 0 .3em}
.pwbox{background:var(--ink);color:var(--bone);border-radius:14px;padding:1.5rem 1.6rem;margin:1.4rem 0}
.pwbox small{display:block;font:700 .68rem ui-monospace,Menlo,monospace;letter-spacing:.26em;text-transform:uppercase;opacity:.6;margin-bottom:.6rem}
.pwbox div{font:800 clamp(1.4rem,4.6vw,2.1rem)/1.2 "Playfair Display",Georgia,serif}
.pwp{font-size:1.15rem;max-width:38em}
.pwg{margin:2.6rem 0 1rem}
.pwg h2{margin:0 0 .15em;font-size:clamp(1.6rem,5vw,2.2rem)}
.pwg .d{opacity:.8;margin:0 0 1rem}
.pwl{display:grid;gap:.7rem}
.pwl a{display:block;text-decoration:none;color:inherit;border:2px solid var(--ink);border-radius:12px;padding:.95rem 1.1rem;background:var(--card);transition:transform .2s,box-shadow .2s}
.pwl a:hover{transform:translateY(-2px);box-shadow:0 12px 24px -14px rgba(0,0,0,.55)}
.pwl b{display:block;font:800 1.15rem/1.25 "Playfair Display",Georgia,serif}
.pwl span{display:block;font-size:.95rem;opacity:.8;margin-top:.2rem}
.pwl i{font-style:normal;font:700 .62rem ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.55;display:block;margin-top:.4rem}
</style>"""

def body():
    out = STYLE + '<div class="pw"><h1 class="pwt">What would prove me wrong.</h1>'
    out += ('<div class="pwbox"><small>The test, in my words</small><div>If a higher intelligence is not acknowledged by a major world power by the end of 2028, I&rsquo;m wrong.</div></div>'
            '<p class="pwp">This whole website is a disclosure of what you should ask and what you should know once that is confirmed. I&rsquo;m telling you the obvious, after it is acknowledged.</p>'
            '<p class="pwp">To keep myself honest, here is the plain reading I will hold myself to: an official, on-the-record statement by the government of a major world power. Not a leak, not an anonymous source, not a rumor. The date is written down on the <a href="/predictions">predictions page</a>, with a fingerprint of the exact text, so it cannot be changed later.</p>')
    for title, desc, tag, items in GROUPS:
        out += f'<div class="pwg"><h2>{E(title)}</h2><p class="d">{E(desc)}</p><div class="pwl">'
        for t, u, d in items:
            host = u.split("/")[2].replace("www.", "")
            out += f'<a href="{E(u)}" target="_blank" rel="noopener"><b>{E(t)}</b><span>{E(d)}</span><i>{E(host)}</i></a>'
        out += '</div></div>'
    out += '<p class="meta" style="margin-top:2.4rem"><a href="/predictions">Predictions</a> &middot; <a href="/evidence-room">Evidence Room</a> &middot; <a href="/">thisisdisclosure.com</a>. No person or institution named on this site has endorsed it.</p></div>'
    return out
