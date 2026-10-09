"""Parmaksız Hukuk bilgilendirme notu üretici.

Kullanım:
    pip install weasyprint jinja2 --break-system-packages
    python3 uret.py icerik.json cikti_klasoru

Çıktı:
    <ad>.pdf           A4 bilgilendirme notu (e-posta eki / arşiv)
    <ad>-kopyala.html  Chrome'da açılıp Gmail'e yapıştırılacak e-posta gövdesi
Kural: içerikte "[" ile başlayan bir yer tutucu varsa üretim durur.
"""
import json, re, sys, pathlib
from jinja2 import Environment, FileSystemLoader

KIT = pathlib.Path(__file__).resolve().parent
SABIT = {
    "etiket": "BİLGİLENDİRME NOTU",
    "yazar": "Av. H. Özgür Parmaksız",
    "eposta": "parmaksiz@ozgurparmaksiz.av.tr",
    "site": "ozgurparmaksiz.av.tr",
    "sorumluluk": ("Bu not, belirtilen tarih itibarıyla genel bilgilendirme amaçlıdır ve hukuki görüş "
                   "niteliği taşımaz. Somut durumunuza ilişkin hukuki destek alınması önerilir."),
}

def main(src, outdir):
    src, out = pathlib.Path(src), pathlib.Path(outdir)
    ham = src.read_text(encoding="utf-8")
    acik = [m.group(0) for m in re.finditer(r"\[[^\]]*(?:doğrulan|eklenecek|KONTROL)[^\]]*\]", ham, re.I)]
    if acik:
        sys.exit("Doğrulanmamış yer tutucu var, nihai çıktı üretilmedi: " + ", ".join(acik))
    data = {**SABIT, **json.loads(ham)}
    env = Environment(loader=FileSystemLoader(KIT), autoescape=True)
    out.mkdir(parents=True, exist_ok=True)
    ad = src.stem

    from weasyprint import HTML
    HTML(string=env.get_template("pdf.html.j2").render(**data), base_url=str(KIT)).write_pdf(out / f"{ad}.pdf")

    govde = env.get_template("eposta.html.j2").render(**data)
    govde = re.sub(r">\s+<", "><", govde)
    sayfa = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>' + ad +
             ' - kopyala</title></head><body style="margin:0;background:#fff">' + govde + "</body></html>")
    (out / f"{ad}-kopyala.html").write_text(sayfa, encoding="utf-8")
    print("Üretildi:", out / f"{ad}.pdf", out / f"{ad}-kopyala.html")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
