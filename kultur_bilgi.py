"""Doğrulanmış kültür bilgisini yükler, LLM bağlamı ve içerik sağlığı üretir."""

import datetime as dt
import json
import os

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
BILGI_YOLU = os.path.join(TEMEL_DIZIN, "kultur-bilgileri.json")


def tumunu_yukle():
    with open(BILGI_YOLU, "r", encoding="utf-8") as dosya:
        return json.load(dosya)


def kayit_getir(slug):
    if not slug:
        return None
    return next((kayit for kayit in tumunu_yukle() if kayit.get("slug") == slug), None)


def llm_baglam_notu(slug):
    kayit = kayit_getir(slug)
    if not kayit or kayit.get("durum") != "onayli" or not kayit.get("dogrulanmis_bilgiler"):
        return None
    bilgiler = " ".join(f"- {x}" for x in kayit.get("dogrulanmis_bilgiler", []))
    adab = " ".join(f"- {x}" for x in kayit.get("adab", []))
    return (
        f"DOĞRULANMIŞ KÜLTÜR BAĞLAMI ({slug}): Aşağıdaki bilgileri olgusal temel olarak kullan; "
        f"bunlarla çelişen veya bunların ötesinde kesin iddia üretme. BİLGİLER: {bilgiler} ADAB: {adab}"
    )


def istemci_kaydi(slug):
    kayit = kayit_getir(slug)
    if not kayit:
        return None
    return {
        "slug": kayit["slug"], "durum": kayit.get("durum", "incelemede"),
        "son_kontrol": kayit.get("son_kontrol"), "kaynaklar": kayit.get("kaynaklar", []),
    }


def icerik_sagligi():
    kayitlar = tumunu_yukle()
    bugun = dt.date.today()
    eski = 0
    for kayit in kayitlar:
        try:
            tarih = dt.date.fromisoformat(kayit.get("son_kontrol", ""))
            if (bugun - tarih).days > 180:
                eski += 1
        except ValueError:
            eski += 1
    return {
        "toplam": len(kayitlar),
        "onayli": sum(k.get("durum") == "onayli" for k in kayitlar),
        "incelemede": sum(k.get("durum") != "onayli" for k in kayitlar),
        "kaynaksiz": sum(not k.get("kaynaklar") for k in kayitlar),
        "eski": eski,
    }
