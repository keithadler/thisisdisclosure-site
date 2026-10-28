"""Re-check every quotation and link in content/faith/*.json against the live page. Run before publishing."""
import glob, json, re, subprocess, html, concurrent.futures as cf
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def norm(t, strip=True):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t) if strip else t)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("–", "-")
    t = re.sub(r"\[\d+\]|\d+\s*(?=[A-Z])", " ", t) if False else t
    t = re.sub(r"\s+", " ", t).strip().lower()
    t = re.sub(r"(\w)- (\w)", r"\1\2", t)
    return re.sub(r"\s+([,;.:!?])", r"\1", t)
def fetch(u):
    r = subprocess.run(["curl", "-sL", "-m", "240", "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9", "-w", "\n%{http_code}", u], capture_output=True, text=True, errors="ignore").stdout
    return r.rsplit("\n", 1)[1], r.rsplit("\n", 1)[0]
jobs = []
for f in sorted(glob.glob("content/faith/*.json")):
    d = json.load(open(f))
    for p in d["passages"]: jobs.append((d["slug"], "quote", p["url"], p["text"], p["ref"]))
    for s in d["sources"]: jobs.append((d["slug"], "source", s["url"], s["title"], ""))
cache = {}
def run(j):
    slug, kind, url, text, ref = j
    if url not in cache: cache[url] = fetch(url)
    code, body = cache[url]
    nb = norm(body, strip=not url.endswith(".txt"))
    if kind == "quote":
        ok = norm(text) in nb
        if not ok:   # tolerate scan quirks: match the first 8 and last 8 words
            w = norm(text).split(); ok = " ".join(w[:8]) in nb and " ".join(w[-8:]) in nb; note = "head+tail only" if ok else "NOT FOUND"
        else: note = "exact"
    else:
        key = norm(text)[:30]; ok = key in nb; note = "title found" if ok else "TITLE NOT FOUND"
    return slug, kind, code, note, url[:70], text[:50]
bad = 0
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(run, jobs):
        flag = "OK " if r[2] == "200" and "NOT" not in r[3] else "BAD"
        if flag == "BAD" or "head" in r[3]: print(flag, *r)
        bad += flag == "BAD"
print("checked", len(jobs), "bad", bad)
