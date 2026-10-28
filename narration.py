"""Slide narration in Keith's own cloned voice (ElevenLabs eleven_v4, emotion set per slide with an audio tag).
spoken(): the words to say; tag(): the emotion; digest(): the cache key. Audio lives in public/n (public slides) and public/sn (gated slides)."""
import hashlib, html, os, re

VOICE = "ovhtdSwgJphPalSlEHij"   # the account's cloned voice named "Keith Adler"
MODEL = "eleven_v4"

def spoken(txt_html):
    if "mailhd" in txt_html or ("From" in txt_html and "Humanity" in txt_html and "Higher Intelligence" in txt_html):
        return "This Is Disclosure. From Keith Adler, to Humanity, with a copy to the Higher Intelligence."
    t = re.sub(r"<br\s*/?>", ". ", txt_html)
    t = re.sub(r"</p>\s*<p", ".</p><p", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("—", ", ").replace("–", " to ")
    t = re.sub(r"A question you may have . (\d+) of 10", lambda m: f"Question {m.group(1)} of 10.", t)
    t = re.sub(r"\s+", " ", t).strip()
    for _ in range(3): t = re.sub(r"\.\s*\.", ".", t)
    t = t.replace(" ,", ",")
    return t

RULES = [
 (r"not a joke|not some social media", "[firmly]"),
 (r"more intelligent than us", "[quietly, with wonder]"),
 (r"weren't ready|came after .not ready", "[softly, with a touch of sadness]"),
 (r"test, not a punishment", "[reassuringly]"),
 (r"Not every hardship", "[gently, with care]"),
 (r"^The pack ", "[evenly]"),
 (r"Why not just prove it|Why would a higher|Why is it almost", "[thoughtfully]"),
 (r"prove me wrong", "[steadily, honestly]"),
 (r"redeem|still time|door is still open|written off|test is still running|almost midnight|almost through the test", "[gently, hopefully]"),
 (r"catastrophic disclosure", "[reassuringly, calmly]"),
 (r"human being like you|treat each other like humans|brothers|You're in the case|You.re in the case", "[warmly]"),
 (r"^Humans of the world", "[warmly, with quiet gravity]"),
 (r"hypothesis|I'm not a scientist|not a prophet|keystone", "[thoughtfully]"),
 (r"In 19\d\d|In 20\d\d|In December 1914|researchers began|In the 1950s|paid one group", "[matter-of-factly]"),
 (r"^Question \d+ of 10", "[conversationally]"),
 (r"hold the door|cheat on the test|Pay for a stranger", "[warmly, encouragingly]"),
 (r"war between Russia and Ukraine|Gender, race", "[calmly, carefully]"),
 (r"Are we animals|Is this what a human being does|Why is this the question", "[quietly, with weight]"),
]

def tag(text):
    for pat, tg in RULES:
        if re.search(pat, text, re.I): return tg
    return "[calmly, sincerely]"

def line(text):
    return f"{tag(text)} {text}"

def digest(text):
    return hashlib.md5((MODEL + VOICE + line(text)).encode()).hexdigest()[:12]

def path(h, secret):
    return f"public/{'sn' if secret else 'n'}/{h}.mp3"

def attr(txt_html, secret):
    """Attribute for a section tag, only when its audio exists."""
    sp = spoken(txt_html)
    if len(sp) < 8: return ""
    h = digest(sp)
    return f' data-n="{h}"' + (' data-ns="1"' if secret else "") if os.path.exists(path(h, secret)) else ""
