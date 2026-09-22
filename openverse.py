# -*- coding: utf-8 -*-
"""
Openverse arama/indirme — Commons'ta yetmeyen görselleri tamamlamak için
ikinci yedek kaynak (Pexels'ten önce denenir). API anahtarı GEREKMEZ.
"""

import json
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.openverse.org/v1/images/"
USER_AGENT = "EvliyaCelebiAI/0.1"
GECERLI_UZANTILAR = (".jpg", ".jpeg")


def _lisans_metni(oge):
    kod = (oge.get("license") or "").lower()
    versiyon = (oge.get("license_version") or "").strip()
    if kod == "pdm":
        return ("Public Domain Mark " + versiyon).strip()
    if kod == "cc0":
        return ("CC0 " + versiyon).strip()
    if kod:
        return (f"CC {kod.upper()} " + versiyon).strip()
    return "bilinmiyor"


def resim_ara(sorgu, adet=3, timeout=20):
    """Openverse'de arar; en fazla `adet` JPEG sonucu [{"indirme_url",
    "fotografci","kaynak_url","lisans"}, ...] olarak döner. API hatası veya
    sonuçsuzlukta sessizce boş liste döner (çağıran sıradaki kaynağa/isim
    kartına düşer)."""
    params = {
        "q": sorgu,
        "license_type": "commercial",
        "page_size": max(adet * 3, 12),  # JPEG olmayanları eleyebilmek icin fazladan iste
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
    except Exception:
        return []

    sonuclar = []
    for oge in (veri.get("results") or []):
        dogrudan_url = oge.get("url") or ""
        if not dogrudan_url.lower().split("?")[0].endswith(GECERLI_UZANTILAR):
            continue
        sonuclar.append({
            "indirme_url": dogrudan_url,
            "fotografci": oge.get("creator") or "bilinmiyor",
            "kaynak_url": oge.get("foreign_landing_url") or dogrudan_url,
            "lisans": _lisans_metni(oge),
        })
        if len(sonuclar) >= adet:
            break
    return sonuclar


def dosya_indir(url, hedef_yol, timeout=30):
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(istek, timeout=timeout) as yanit:
        veri = yanit.read()
    with open(hedef_yol, "wb") as f:
        f.write(veri)
