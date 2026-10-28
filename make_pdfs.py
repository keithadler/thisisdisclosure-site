"""Render each cheat sheet page to public/pdf/*.pdf with headless Chrome (print CSS makes it a checklist).
Run after build.py and before deploy:  python3 make_pdfs.py"""
import subprocess, time, os, sys, signal
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
sys.path.insert(0, ".")
import re
names = sorted(re.findall(r'((?:cheat-sheet|guide|country|sign)-[a-z]+)\.html', " ".join(os.listdir("public"))))
if len(sys.argv)>1: names=[n for n in names if n.startswith(tuple(sys.argv[1:]))]
os.makedirs("public/pdf", exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8768", "--directory", "public"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(1.2)
    for s in names:
        out = os.path.abspath(f"public/pdf/{s}.pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                        f"--print-to-pdf={out}", f"http://localhost:8768/{s}.html"], check=True, capture_output=True, timeout=90)
        n = open(out, "rb").read().count(b"/Type /Page\n") or open(out, "rb").read().count(b"/Type/Page")
        print(s, os.path.getsize(out) // 1024, "KB")
finally:
    srv.send_signal(signal.SIGTERM)
