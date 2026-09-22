# -*- coding: utf-8 -*-
"""
Pexels arama/indirme — Commons'ta sonuç bulunamayan yerler için yedek görsel
kaynağı. API anahtarı .env'deki PEXELS_API_KEY'den okunur (commons.gorsel_bul
tarafından, Commons boş döndüğünde çağrılır).
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.pexels.com/v1/search"
USER_AGENT = "EvliyaCelebiAI/0.1"


def _api_anahtari():
    return os.environ.get("PEXELS_API_KEY")


def fotograf_ara(sorgu, adet=3, timeout=20):
    """Pexels'te arar; en fazla `adet` sonucu [{"indirme_url","fotografci",
    "kaynak_url"}, ...] olarak döner. API anahtarı yoksa, hiç sonuç yoksa
    veya bir hata olursa sessizce boş liste döner (çağıran isim kartına düşer,
    hata fırlatılmaz)."""
    anahtar = _api_anahtari()
    if not anahtar:
        return []

    params = {
        "query": sorgu,
        "orientation": "landscape",
        "per_page": adet,
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    istek = urllib.request.Request(url, headers={"Authorization": anahtar, "User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
    except Exception:
        return []

    sonuclar = []
    for foto in (veri.get("photos") or [])[:adet]:
        buyuk_url = (foto.get("src") or {}).get("large")
        if not buyuk_url:
            continue
        sonuclar.append({
            "indirme_url": buyuk_url,
            "fotografci": foto.get("photographer") or "bilinmiyor",
            "kaynak_url": foto.get("url") or foto.get("photographer_url") or "",
        })
    return sonuclar


def dosya_indir(url, hedef_yol, timeout=30):
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(istek, timeout=timeout) as yanit:
        veri = yanit.read()
    with open(hedef_yol, "wb") as f:
        f.write(veri)
