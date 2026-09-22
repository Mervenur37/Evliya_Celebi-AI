# -*- coding: utf-8 -*-
"""
Görsel indirici — dört kademeli kaynak zinciri: yerel önbellek (assets/) ->
Wikimedia Commons -> Openverse -> Pexels (yalnızca Pexels için .env'deki
PEXELS_API_KEY gerekir; diğerleri anahtarsız).

Her slug için commons.gorsel_bul(slug, ...) çağrılır: önce assets/ klasöründe
zaten var mı bakar, yoksa sırayla Commons, Openverse, Pexels'te arar
(slug-01..06.jpg olarak iner). Hiçbiri bulamazsa slug "bulunamayan" listesine
düşer (assets.json değişmez, çağıran taraf isim kartına düşer).

Arama/indirme/katalog mantığı commons.py + openverse.py + pexels.py'de ortak
— app.py'deki canlı görsel tamamlama da aynı fonksiyonları kullanır.

Kullanım: python gorsel_indir.py
"""

import os
import sys
import time

from dotenv import load_dotenv

import commons

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIZIN = os.path.join(TEMEL_DIZIN, "assets")
KATALOG_YOLU = os.path.join(TEMEL_DIZIN, "assets.json")

SORGULAR = {
    "istanbul": "Istanbul Hagia Sophia",
    "kapadokya": "Cappadocia balloons",
    "safranbolu": "Safranbolu houses",
    "gaziantep": "baklava",
    "hatay": "künefe",
    "gobeklitepe": "Göbekli Tepe",
    "hattusa": "Hattusa",
    "ani": "Ani ruins",
    "amasya": "Amasya houses",
    "datca": "Datça",
    "assos": "Assos Behramkale",
    "egirdir": "Eğirdir lake",
    "kackar": "Kaçkar",
    "antalya": "Antalya Kaleiçi",
    "pamukkale": "Pamukkale travertine",
    "bursa": "İskender kebap",
    "kayseri": "Mantı",
    "akyaka": "Akyaka",
    "sagalassos": "Sagalassos",
    "mardin": "Mardin old town",
    "ankara": "Anıtkabir",
}

# Katalogda henüz kaydı olmayan slug'lar için varsayılan temalar
# (sabit tema sözlüğü: tarih, doga, yemek, deniz, sanat, sakin, macera, aile).
VARSAYILAN_TEMALAR = {
    "ankara": ["tarih", "sanat"],
}

GORSEL_SAYISI = 6


def main():
    os.makedirs(ASSETS_DIZIN, exist_ok=True)
    katalog = commons.katalog_yukle(KATALOG_YOLU)

    basarili = []
    basarisiz = []
    kaynak_ozet = {}

    for slug, sorgu in SORGULAR.items():
        print(f"[{slug}] kontrol ediliyor...")
        sonuc = commons.gorsel_bul(
            slug, ASSETS_DIZIN, sorgu=sorgu, adet=GORSEL_SAYISI,
            tema=(VARSAYILAN_TEMALAR.get(slug) or [None])[0],
        )
        kaynak = sonuc["kaynak"]

        if kaynak == "onbellek":
            print(f"   zaten {GORSEL_SAYISI}/{GORSEL_SAYISI} indirilmiş, atlanıyor.")
            basarili.append(slug)
            kaynak_ozet["onbellek"] = kaynak_ozet.get("onbellek", 0) + 1
            continue

        if not sonuc["gorseller"]:
            print("   !! Uygun görsel bulunamadı (Commons, Openverse, Pexels).")
            basarisiz.append(slug)
            continue

        katalog = commons.katalog_gorseller_ekle(
            katalog, slug, sonuc["gorseller"], VARSAYILAN_TEMALAR.get(slug, ["tarih"]),
        )
        kaynak_ozet[kaynak] = kaynak_ozet.get(kaynak, 0) + 1
        for g in sonuc["gorseller"]:
            print(f"   ✓ {g['dosya']}  ({g['kaynak']} | {g['lisans']} | {g['fotografci']})")
        basarili.append(slug)

        time.sleep(1)

    commons.katalog_kaydet(katalog, KATALOG_YOLU)

    print(f"\n{'=' * 50}")
    print(f"İşlenen: {len(basarili)}/{len(SORGULAR)}")
    print(f"Kaynak özeti: {kaynak_ozet}")
    if basarisiz:
        print(f"Bulunamayan: {', '.join(basarisiz)}")
    print(f"assets.json güncellendi -> {KATALOG_YOLU}")


if __name__ == "__main__":
    main()
