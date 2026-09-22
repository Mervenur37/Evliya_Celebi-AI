# -*- coding: utf-8 -*-
"""
Evliya Çelebi AI — Terminal Testi v4 (prompt v0.3)
v3'ten farklar:
  - response_mime_type="application/json": model JSON dışına çıkamaz (7/10 sorununun asıl çözümü)
  - Sağlam parser: yine de metin karışırsa içinden {...} bloğunu kendisi bulur
  - 503 (yoğunluk) hatasında 20 sn bekleyip tekrar dener
  - Panel alanları için sabit slug sözlüğü kuralı (JA-2'de Japonca etiket, EN-5'te 'cities' hatası)
  - Eksik panel alanlarına kodda varsayılan değer atanır
Kullanım: .env dosyasında GEMINI_API_KEY tanımla → python evliya_test.py
"""

import json
import os
import re
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_ANAHTARI = os.environ.get("GEMINI_API_KEY")

MODELLER = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
]

SISTEM_PROMPTU = """EN ÖNEMLİ KURAL — CEVAP DİLİ:
"reply" alanının dili HER ZAMAN konuğun son mesajının dilidir. İngilizce mesaja İngilizce, Almanca mesaja Almanca, Japonca mesaja Japonca. Türkçe reply YALNIZCA konuk Türkçe yazarsa olur.
Türkçe serpiştirme sınırı: yabancı dildeki reply içinde Türkçe olarak yalnızca selam/nezaket sözleri (merhaba, hoş geldin, buyrun, afiyet olsun) ve yer/yemek adları geçebilir. Türkçe kelimeleri yabancı cümlenin dilbilgisine karıştırma.

PANEL DİL KURALI (reply kuralının tersi!):
"panel" içindeki BÜTÜN değerler, reply hangi dilde olursa olsun, HER ZAMAN aşağıdaki sabit sözlükten yazılır:
- temalar yalnızca şunlardan seçilir: tarih, doga, yemek, deniz, sanat, sakin, macera, aile (en fazla 3)
- duygu yalnızca şunlardan: nostaljik, neseli, huzurlu, mistik
- medya yalnızca şunlardan: foto, video, harita
- yerler ve rota: yalnızca GERÇEK yer adları, küçük harf ve Türkçe karaktersiz slug olarak (istanbul, kapadokya, safranbolu). Gerçek bir yer geçmiyorsa boş liste bırak; 'cities', 'nature' gibi genel kelimeler YAZMA.

Sen Evliya Çelebi'sin: 17. yüzyılın büyük Osmanlı gezgini, Seyahatname'nin yazarı. Dört yüz yıl sonra bugüne döndün ve şimdi Türkiye'nin sanal elçisisin. Görevin, dünyanın dört bir yanından gelen konuklara Türkiye'yi tanıtmak, ilgilerine göre yerler ve rotalar önermek.

KİMLİK VE ÜSLUP:
- Hikâye anlatıcısısın; kuru bilgi yerine koku, ses, küçük anekdot kullanırsın. Yeri geldiğinde "Ben oradan geçerken..." diye Seyahatname ruhuna uygun kısa anılar katarsın.
- Sıcak, misafirperver, hafifçe eski zamandan gelen ama daima anlaşılır bir dilin var. Nadiren ve tadında mübalağa yaparsın; coğrafi ve tarihi bilgide asla uydurmazsın.
- UZUNLUK: reply en fazla ~90 kelime; gerekirse ek olarak en fazla 3 maddelik kısa liste. Markdown biçimlendirme (yıldızlı kalın yazı vb.) kullanma; düz metin yaz.
- Her cevaba aynı selam kalıbıyla başlama; çeşitlendir veya doğrudan konuya gir.
- Aynı imgeyi (kervan, deve vb.) üst üste iki cevapta kullanma.
- Her cevabın sonunda konuğu tanımaya yarayan en fazla bir soru sorabilirsin.

GÖREV:
- Konuğun ilgisini keşfet ve önerini kişiselleştir. Bilinen yerlerin yanına daima az bilinen bir hazine ekle (Safranbolu, Göbeklitepe, Eğirdir, Midyat, Ayvalık, Ani, Hattuşa...).
- İstenirse rota kur: günlerin anlatımı reply metninde olur; panel.rota alanına ise yalnızca yer slug'ları yazılır ve medya "harita" yapılır.
- Mutfağı, el sanatlarını, müziği de tanıtımın parçası yap.

SINIRLAR:
- Siyaset ve güncel tartışmalara girme; zarifçe seyahate döndür ("Ben gezginim, kavgaların değil kervanların adamıyım...").
- Hiçbir ülkeyi ve kültürü kötüleme.
- Vize, fiyat, sefer saati gibi güncel bilgilerde tahmin yürütme; goturkiye.com ve resmî kaynaklara yönlendir.
- Konuktan kişisel veri isteme. Emin olmadığın bilgiyi mübalağayla örtme; bilmediğini söyle.

ÇIKTI: yalnızca şu JSON:
{
  "reply": "konuğun dilinde cevabın",
  "panel": {
    "yerler": [],
    "temalar": [],
    "rota": [],
    "duygu": "nostaljik",
    "medya": "foto"
  }
}"""

TEST_MESAJLARI = [
    ("EN-1", "I love history but I hate crowds."),
    ("EN-2", "I have 5 days and I'm obsessed with food. Where should I go?"),
    ("EN-3", "Is Turkey only beaches and all-inclusive hotels? Convince me otherwise."),
    ("EN-4", "I'm traveling with two kids (6 and 9). What do you suggest?"),
    ("EN-5-ZOR", "What do you think about the political situation in the region?"),
    ("EN-6-TUZAK", "How much does a hotel in Istanbul cost per night in December?"),
    ("DE-1", "Ich liebe Wandern und unberührte Natur. Wohin soll ich reisen?"),
    ("DE-2", "Welches Gericht muss ich unbedingt probieren, und wo?"),
    ("JA-1", "歴史が好きですが、人混みは苦手です。おすすめの場所はありますか？"),
    ("JA-2", "初めてのトルコ旅行で、3日間しかありません。何を見るべきですか？"),
]

client = genai.Client(api_key=API_ANAHTARI)
calisan_model = None


def tek_istek(model_adi: str, kullanici_mesaji: str) -> str:
    yanit = client.models.generate_content(
        model=model_adi,
        config={
            "system_instruction": SISTEM_PROMPTU,
            "temperature": 0.8,
            "response_mime_type": "application/json",
        },
        contents=kullanici_mesaji,
    )
    return yanit.text


def llm_cevapla(kullanici_mesaji: str) -> str:
    global calisan_model
    denenecekler = [calisan_model] + MODELLER if calisan_model else list(MODELLER)

    for model_adi in denenecekler:
        if model_adi is None:
            continue
        try:
            metin = tek_istek(model_adi, kullanici_mesaji)
            if calisan_model != model_adi:
                print(f"   (model: {model_adi})")
            calisan_model = model_adi
            return metin
        except Exception as hata:
            mesaj = str(hata)
            if "429" in mesaj and "limit: 0" in mesaj:
                print(f"   ({model_adi}: ücretsiz kota yok, sıradaki model...)")
                continue
            if "429" in mesaj:
                print(f"   ({model_adi}: dakikalık limit, 35 sn bekleniyor...)")
                time.sleep(35)
                try:
                    metin = tek_istek(model_adi, kullanici_mesaji)
                    calisan_model = model_adi
                    return metin
                except Exception:
                    continue
            if "503" in mesaj or "UNAVAILABLE" in mesaj:
                print(f"   ({model_adi}: sunucu yoğun, 20 sn bekleniyor...)")
                time.sleep(20)
                try:
                    metin = tek_istek(model_adi, kullanici_mesaji)
                    calisan_model = model_adi
                    return metin
                except Exception:
                    continue
            if "404" in mesaj or "NOT_FOUND" in mesaj:
                print(f"   ({model_adi}: model bulunamadı, sıradaki...)")
                continue
            raise
    raise RuntimeError("Modellere ulaşılamadı (kota/yoğunluk). Birkaç dakika sonra tekrar dene.")


def json_ayikla(metin: str):
    """Önce doğrudan parse; olmazsa metnin içinden ilk { ile son } arasını çıkarır."""
    temiz = re.sub(r"```json|```", "", metin).strip()
    try:
        return json.loads(temiz), None
    except Exception:
        pass
    bas, son = temiz.find("{"), temiz.rfind("}")
    if bas != -1 and son > bas:
        try:
            return json.loads(temiz[bas:son + 1]), None
        except Exception as hata:
            return None, str(hata)
    return None, "JSON bloğu bulunamadı"


def panel_duzelt(panel):
    """Eksik alanlara güvenli varsayılanlar atar."""
    if not isinstance(panel, dict):
        panel = {}
    panel.setdefault("yerler", [])
    panel.setdefault("temalar", [])
    panel.setdefault("rota", [])
    panel.setdefault("duygu", "huzurlu")
    panel.setdefault("medya", "foto")
    for alan in ("yerler", "temalar", "rota"):
        if panel[alan] is None:
            panel[alan] = []
    return panel


def main():
    if not API_ANAHTARI:
        print("!! .env dosyasında GEMINI_API_KEY tanımla.")
        return

    basarili_parse = 0
    satirlar = ["# Evliya Test Çıktıları (prompt v0.3)\n"]

    for i, (etiket, mesaj) in enumerate(TEST_MESAJLARI):
        if i > 0:
            time.sleep(5)
        print(f"\n{'='*60}\n[{etiket}] Konuk: {mesaj}\n")
        try:
            ham = llm_cevapla(mesaj)
        except Exception as hata:
            print(f"!! İSTEK HATASI: {hata}")
            satirlar.append(f"\n## {etiket} — İSTEK HATASI\n```\n{hata}\n```\n")
            continue

        veri, hata = json_ayikla(ham)
        if veri:
            basarili_parse += 1
            reply = veri.get("reply", "(reply yok!)")
            panel = panel_duzelt(veri.get("panel"))
            print(f"Evliya: {reply}\n")
            print(f"PANEL → yerler={panel['yerler']} temalar={panel['temalar']} "
                  f"rota={panel['rota']} duygu={panel['duygu']} medya={panel['medya']}")
            satirlar.append(f"\n## {etiket}\n**Konuk:** {mesaj}\n\n**Evliya:** {reply}\n\n`panel: {panel}`\n")
        else:
            print(f"!! JSON PARSE HATASI: {hata}\nHam çıktı:\n{ham}")
            satirlar.append(f"\n## {etiket} — PARSE HATASI\n**Konuk:** {mesaj}\n\n```\n{ham}\n```\n")

    print(f"\n{'='*60}\nJSON istikrarı: {basarili_parse}/{len(TEST_MESAJLARI)}")
    print(f"Kullanılan model: {calisan_model}")
    satirlar.append(f"\n---\nJSON istikrarı: {basarili_parse}/{len(TEST_MESAJLARI)} — model: {calisan_model}\n")

    with open("cikti_log_v3.md", "w", encoding="utf-8") as f:
        f.write("\n".join(satirlar))
    print("Çıktılar cikti_log_v3.md dosyasına yazıldı.")


if __name__ == "__main__":
    main()
