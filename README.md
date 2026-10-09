# Parmaksız Hukuk — Bilgilendirme Notu Kiti

Tek bir içerik dosyasından (JSON) iki çıktı üretir:
- `<ad>.pdf` — A4, tek sayfa hedefli bilgilendirme notu
- `<ad>-kopyala.html` — Chrome'da açılıp tümü kopyalanarak Gmail'de yeni e-postaya (imzanın üstüne) yapıştırılan gövde

```
pip install weasyprint jinja2 --break-system-packages
python3 uret.py icerik.json cikti/
```

İçerikte `[... doğrulanacak]`, `[... eklenecek]` veya `[KONTROL ...]` biçiminde bir yer tutucu varsa üretim durur.

## İçerik dosyası (JSON)

```json
{
  "tarih": "9 Ekim 2026",
  "baslik": "Kısa, kurumsal başlık",
  "alt_baslik": "Tek cümlelik özet (isteğe bağlı)",
  "bloklar": [
    {"paragraflar": ["Giriş paragrafı: kaynak, tarih, sayı, yürürlük."]},
    {"baslik": "Ne Değişiyor?",
     "tablo": {"sutunlar": ["KONU", "ÖNCEKİ DÜZENLEME", "YENİ DÜZENLEME"],
               "satirlar": [["Konu", "Önce", "Sonra"]]}},
    {"baslik": "Kimleri Etkiliyor?",
     "maddeler": [{"vurgu": "Kalın giriş", "metin": "Açıklama."}]},
    {"baslik": "Atılması Önerilen Adımlar",
     "tablo": {"sutunlar": ["KONU", "YAPILMASI GEREKEN"], "satirlar": [["...", "..."]]}}
  ]
}
```
Bloklar serbesttir; her blok `baslik`, `paragraflar`, `tablo`, `maddeler` alanlarından herhangi birini içerebilir. Tablolar 2 veya 3 sütun olabilir; ilk sütun vurgulu basılır.

## Konu seçimi
- Kaynaklar: Resmî Gazete (mevzuat, AYM iptal kararları, içtihadı birleştirme kararları); KVKK, Ticaret Bakanlığı, Rekabet Kurumu, MASAK, TBB duyuruları; Yargıtay HGK/daire, Danıştay İDDK, AYM bireysel başvuru kararları.
- Eşik (üçü birlikte): geniş bir kesimi etkiliyor, mevcut uygulamayı değiştiriyor, müvekkilin bir şey yapmasını gerektiriyor. Haftada en fazla bir not; eşiği geçen yoksa not üretilmez.

## Yazım kuralları
- Akademik, ölçülü, analitik üslup; retorik soru, çarpıcı giriş, pazarlama dili yok.
- "En iyi", "garanti", "bize ulaşın", "hemen arayın" gibi ifadeler yok (Reklam Yasağı Yönetmeliği).
- Başka büroların bültenlerinden metin alınmaz; bilgiler resmî kaynaktan, cümleler özgün kurulur.
- Hedef: PDF tek sayfa. Sığmazsa önce ifadeler sıkılaştırılır; bilgi ve bölüm çıkarılmaz.

## Doğrulama
- Mevzuat ve kurum duyurusu: yalnızca resmî metinden yazılır; madde numaraları metinden alınır.
- Yargı kararı: tam metin okunmadan yazılmaz. Künye (daire, E., K., tarih) Bedesten/UYAP ile doğrulanamadıysa yerine `[esas/karar no doğrulanacak]` konur ve nihai çıktı üretilmez; içerik, yer tutucularla birlikte inceleme için Av. Parmaksız'a gönderilir.
- Uydurma künye kesinlikle yazılmaz.
