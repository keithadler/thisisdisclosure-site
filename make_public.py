"""Build a sanitized public copy of the source: everything except the gated slides, the gated FAQ answers and the art used only by gated slides.
Usage: python3 make_public.py OUTDIR   (OUTDIR is emptied first, except .git)"""
import os, re, shutil, sys, glob, json

out = sys.argv[1]
assert out and out not in ("/", os.path.expanduser("~")), "bad OUTDIR"
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f == ".git": continue
    p = os.path.join(out, f)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

b = open("build.py").read()
L = b.split("\n")
s0 = next(i for i, l in enumerate(L) if l.startswith("S=["))
k0 = next(i for i, l in enumerate(L) if l.startswith("SECRET=["))
k1 = next(i for i in range(k0 + 1, len(L)) if L[i].startswith("]"))
def keys(lines):
    return {m.group(1) for l in lines for m in [re.match(r' \("[^"]*",".*","([a-z_0-9]+)","', l)] if m}
pub_keys = keys(L[s0:k0]); sec_keys = keys(L[k0:k1])
# SRC mapping
srcmap = {}
m = re.search(r"\nSRC=\{(.*?)\}\n", b, re.S)
srcmap.update(eval("{" + m.group(1) + "}"))
for m2 in re.finditer(r'SRC\.update\(\{(.*?)\}\)', b):
    inner = m2.group(1)
    if ":" in inner and '"' in inner and "for" not in inner:
        srcmap.update(eval("{" + inner + "}"))
gated = {srcmap.get(k, k) for k in sec_keys}
sys.path.insert(0, "."); sys.path.insert(0, "content")
keep = {srcmap.get(k, k) for k in pub_keys}
from evidence_data import CASES
keep |= {c["key"] for c in CASES if c["key"]}
import faith_guides, cheat_pages, country_guides
keep |= set(faith_guides.ART.values()) | {cheat_pages.ART[k] and {"cs_everyone": "grace", "cs_everyday": "bench", "cs_elders": "elder", "cs_teens": "classroom", "cs_parents": "mother", "cs_leaders": "hiring", "cs_inside": "hallway", "cs_fallen": "porch", "cs_meaning": "climb"}[cheat_pages.ART[k]] for k in cheat_pages.ART}
keep |= {country_guides.ART}
exclude = gated - keep
print("gated-only art files:", len(exclude))

# sanitized build.py
san = L[:k0] + ["SECRET=[]  # the gated slides are not published in this repository"] + L[k1 + 1:]
open(os.path.join(out, "build.py"), "w").write("\n".join(san))

def cp(src, dst=None):
    dst = os.path.join(out, dst or src); os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    if os.path.isdir(src): shutil.copytree(src, dst)
    else: shutil.copy2(src, dst)
for f in ["template.html", "evidence_page.py", "cheat_pages.py", "faith_guides.py", "country_guides.py", "prove_me_wrong.py", "share_page.py", "narration.py",
          "make_pdfs.py", "verify_faith.py", "make_public.py", "wrangler.jsonc", ".gitignore",
          "quotes.py", "quotes2.py", "quotes3.py", "quotes4.py",
          "email/announcement.html", "email/announcement.txt", "email/reply.txt", "audio/hash.txt"]:
    if os.path.exists(f): cp(f)
for f in glob.glob("audio/loop96.mp3"): cp(f)
for d in ["content/faith", "content/countries", "content/cheat_evidence", "content/evidence_extra"]:
    if os.path.isdir(d): cp(d)
for f in ["evidence_data.py", "ev_cases_base.py", "land110.geojson", "predictions.txt", "predictions-added-1.txt", "predictions-added-2.txt",
          "predictions-added-3.txt", "sources-head.html", "faq-head.html", "sources-research.html", "evidence-live"]:
    if os.path.exists("content/" + f): cp("content/" + f)
os.makedirs(os.path.join(out, "content"), exist_ok=True)
open(os.path.join(out, "content/faq-body.html"), "w").write(
    "<h2>Gated FAQs are not published in this repository.</h2>\n<p>The FAQ answers are shown on thisisdisclosure.com after the 18+ agreement. Put your own questions and answers here as h2 and p elements.</p>\n")
# art
os.makedirs(os.path.join(out, "art"), exist_ok=True)
for f in os.listdir("art"):
    stem = os.path.splitext(f)[0]
    if stem in exclude or f.startswith("sheet") or f.endswith("_preview.png") or not f.lower().endswith((".png", ".jpg")): continue
    shutil.copy2(os.path.join("art", f), os.path.join(out, "art", f))
# public assets and pages, without the gated fragments and without art tied to gated slides
for root, dirs, files in os.walk("public"):
    rel = os.path.relpath(root, "public")
    if rel in ("s", "sn", "n") or rel.startswith("s" + os.sep) or rel == "art" or rel.startswith("pdf"): dirs[:] = []; continue
    for f in files:
        if f.startswith(".") : continue
        src = os.path.join(root, f); dst = os.path.join(out, "public", rel, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
print("wrote", out)
