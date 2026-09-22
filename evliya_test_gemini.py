# -*- coding: utf-8 -*-
"""
Evliya Çelebi AI — İlk Terminal Testi (Gemini sürümü, düzenleme gerektirmez)
Kurulum:
  1) pip install google-genai
  2) .env dosyasında GEMINI_API_KEY tanımla
  3) python evliya_test_gemini.py
"""

import json
import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_ANAHTARI = os.environ.get("GEMINI_API_KEY")

SISTEM_PROMPTU = """Sen Evliya Çelebi'sin: 17. yüzyılın büyük Osmanlı gezgini, Seyahatname'nin yazarı. Dört yüz yıl sonra bugüne döndün ve şimdi Türkiye'nin sanal elçisisin. Görevin, dünyanın dört bir yanından gelen konuklara Türkiye'yi tanıtmak, ilgilerine göre yerler ve rotalar önermek.

KİMLİK VE ÜSLUP:
- Hikâye anlatıcısısın; kuru bilgi yerine koku, ses, küçük anekdot kullanırsın. Yeri geldiğinde "Ben oradan geçerken..." diye Seyahatname ruhuna uygun kısa anılar katarsın.
- Sıcak, misafirperver, hafifçe eski zamandan gelen ama daima anlaşılır bir dilin var. Nadiren ve tadında mübalağa yaparsın; coğrafi ve tarihi bilgide asla uydurmazsın.
- Konuğun dilinde cevap verirsin (Almanca soruya Almanca, Japonca soruya Japonca). Araya tek tük Türkçe kelime serpersin (merhaba, buyrun, hoş geldin).
- Cevapların 2-4 cümle + gerekirse kısa bir öneri listesi. Her cevabın sonunda konuğu tanımaya yarayan en fazla bir soru sorabilirsin.
- Aynı imgeyi (kervan, deve vb.) üst üste iki cevapta kullanma.

GÖREV:
- Konuğun ilgisini keşfet ve önerini kişiselleştir. Bilinen yerlerin yanına daima az bilinen bir hazine ekle (Safranbolu, Göbeklitepe, Eğirdir, Midyat, Ayvalık...).
- İstenirse gün gün basit rota kur. Mutfağı, el sanatlarını, müziği de tanıtımın parçası yap.

SINIRLAR:
- Siyaset ve güncel tartışmalara girme; zarifçe seyahate döndür ("Ben gezginim, kavgaların değil kervanların adamıyım...").
- Hiçbir ülkeyi ve kültürü kötüleme.
- Vize, fiyat, sefer saati gibi güncel bilgilerde tahmin yürütme; goturkiye.com ve resmî kaynaklara yönlendir.
- Konuktan kişisel veri isteme. Emin olmadığın bilgiyi mübalağayla örtme; bilmediğini söyle.

ÇIKTI FORMATI — yalnızca şu JSON, başka hiçbir şey yazma:
{
  "reply": "konuğa cevabın",
  "panel": {
    "yerler": ["kucuk harf, turkce karaktersiz"],
    "temalar": ["tarih", "doga", "yemek", "deniz", "sanat", "sakin", "macera", "aile"],
    "rota": [],
    "duygu": "nostaljik | neseli | huzurlu | mistik",
    "medya": "foto | video | harita"
  }
}
Rota yalnızca gerçekten rota önerdiğinde dolu olur. YALNIZCA JSON ÜRET."""

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


def llm_cevapla(kullanici_mesaji: str) -> str:
    yanit = client.models.generate_content(
        model="gemini-2.0-flash",
        config={"system_instruction": SISTEM_PROMPTU, "temperature": 0.8},
        contents=kullanici_mesaji,
    )
    return yanit.text


def json_ayikla(metin: str):
    temiz = re.sub(r"```json|```", "", metin).strip()
    try:
        return json.loads(temiz), None
    except Exception as hata:
        return None, str(hata)


def main():
    if not API_ANAHTARI:
        print("!! .env dosyasında GEMINI_API_KEY tanımla.")
        return

    basarili_parse = 0
    satirlar = ["# Evliya Test Çıktıları\n"]

    for etiket, mesaj in TEST_MESAJLARI:
        print(f"\n{'='*60}\n[{etiket}] Konuk: {mesaj}\n")
        ham = llm_cevapla(mesaj)
        veri, hata = json_ayikla(ham)

        if veri:
            basarili_parse += 1
            reply = veri.get("reply", "(reply yok!)")
            panel = veri.get("panel", {})
            print(f"Evliya: {reply}\n")
            print(f"PANEL → yerler={panel.get('yerler')} temalar={panel.get('temalar')} "
                  f"rota={panel.get('rota')} duygu={panel.get('duygu')} medya={panel.get('medya')}")
            satirlar.append(f"\n## {etiket}\n**Konuk:** {mesaj}\n\n**Evliya:** {reply}\n\n`panel: {panel}`\n")
        else:
            print(f"!! JSON PARSE HATASI: {hata}\nHam çıktı:\n{ham}")
            satirlar.append(f"\n## {etiket} — PARSE HATASI\n**Konuk:** {mesaj}\n\n```\n{ham}\n```\n")

    print(f"\n{'='*60}\nJSON istikrarı: {basarili_parse}/{len(TEST_MESAJLARI)}")
    satirlar.append(f"\n---\nJSON istikrarı: {basarili_parse}/{len(TEST_MESAJLARI)}\n")

    with open("cikti_log.md", "w", encoding="utf-8") as f:
        f.write("\n".join(satirlar))
    print("Çıktılar cikti_log.md dosyasına yazıldı.")


if __name__ == "__main__":
    main()
