"""Extrai quadros (1 a cada 10 s) da gravacao TV Senado e roda OCR para achar telas com o painel do TSE.
Offset do video: 0 s = 16:19:46 BRT (04/10/2026). Janela: 19:00 (9600 s) a 20:15 (14100 s)."""
import csv, os, re, subprocess
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = os.path.join(RAIZ, "video", "apuracao_tvsenado_041026.mp4")
OUT = os.path.join(RAIZ, "video", "janela")
os.makedirs(OUT, exist_ok=True)
INI, FIM, PASSO = 9600, 14100, 10
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(INI), "-t", str(FIM - INI), "-i", VID,
                "-vf", f"fps=1/{PASSO}", os.path.join(OUT, "f_%04d.png")], check=True)
arqs = sorted(f for f in os.listdir(OUT) if f.endswith(".png"))
print("quadros:", len(arqs), flush=True)


def ocr(f):
    r = subprocess.run([TESS, os.path.join(OUT, f), "-", "-l", "por", "--psm", "11"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return f, r.stdout


with ThreadPoolExecutor(6) as ex, open(os.path.join(RAIZ, "dados", "video_ocr.csv"), "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo)
    w.writerow(["quadro", "offset_s", "hora_brt", "painel", "texto"])
    for f, txt in ex.map(ocr, arqs):
        n = int(re.search(r"(\d+)", f).group(1))
        off = INI + (n - 1) * PASSO
        h, m, s = (16 * 3600 + 19 * 60 + 46 + off) // 3600, ((16 * 3600 + 19 * 60 + 46 + off) % 3600) // 60, (16 * 3600 + 19 * 60 + 46 + off) % 60
        t = txt.replace("\n", " | ")
        painel = bool(re.search(r"(seç|secoes|apurad|%)", t, re.I) and re.search(r"(Flávio|Flavio|Lula|Bolsonaro)", t, re.I))
        w.writerow([f, off, f"{h:02d}:{m:02d}:{s:02d}", int(painel), t[:600]])
print("fim", flush=True)
