# -*- coding: utf-8 -*-
"""
Rota haritası için yer -> (lat, lon) çözümleme.

Önce yerler-koordinat.json'daki önbelleğe bakar; orada yoksa Nominatim
(OpenStreetMap) geocoding API'siyle arar ve bulduğunu önbelleğe yazar.
Nominatim kullanım kuralları gereği User-Agent zorunlu ve istekler arasında
en az 1 sn bekleniyor. Bulunamayan duraklar sessizce atlanır — harita o
nokta olmadan çizilir, /sohbet asla bu yüzden hataya düşmez.
"""

import json
import math
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "EvliyaCelebiAI/0.1"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
KOORDINAT_YOLU = os.path.join(TEMEL_DIZIN, "yerler-koordinat.json")


def koordinat_yukle():
    if os.path.exists(KOORDINAT_YOLU):
        with open(KOORDINAT_YOLU, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def koordinat_kaydet(veri):
    with open(KOORDINAT_YOLU, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2, sort_keys=True)


def nominatim_ara(slug, timeout=8):
    """Nominatim'de arar; bulursa (lat, lon) döner, bulamaz/hata alırsa None."""
    params = {
        "q": f"{slug}, Turkey",
        "format": "json",
        "limit": 1,
        "countrycodes": "tr",
    }
    url = NOMINATIM_URL + "?" + urllib.parse.urlencode(params)
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            sonuclar = json.loads(yanit.read().decode("utf-8"))
    except Exception:
        return None

    if not sonuclar:
        return None
    try:
        return float(sonuclar[0]["lat"]), float(sonuclar[0]["lon"])
    except (KeyError, ValueError, TypeError, IndexError):
        return None


def nominatim_ters_sehir(lat, lon, timeout=6):
    """Koordinatı Türkiye'deki il/şehir adına çevirir.

    Kesin koordinat diske yazılmaz. Kullanıcının şehir alanını güncellemek
    için yalnızca Nominatim'in döndürdüğü genel il/şehir adı istemciye verilir.
    """
    try:
        lat, lon = float(lat), float(lon)
    except (TypeError, ValueError):
        return None
    if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
        return None

    params = {
        "lat": f"{lat:.6f}",
        "lon": f"{lon:.6f}",
        "format": "jsonv2",
        "zoom": 10,
        "addressdetails": 1,
        "accept-language": "tr",
    }
    url = NOMINATIM_REVERSE_URL + "?" + urllib.parse.urlencode(params)
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "tr"})
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            veri = json.loads(yanit.read().decode("utf-8"))
    except Exception:
        return None

    adres = veri.get("address") or {}
    ulke_kodu = str(adres.get("country_code") or "").lower()
    if ulke_kodu and ulke_kodu != "tr":
        return {"sehir": None, "ulke_kodu": ulke_kodu}

    # Türkiye sonuçlarında il çoğunlukla province/state alanında; daha küçük
    # yerleşimlerde city/town/county alanlarına güvenli biçimde düşülür.
    sehir = next((adres.get(alan) for alan in (
        "province", "state", "city", "town", "municipality", "state_district", "county"
    ) if adres.get(alan)), None)
    if not sehir:
        return None
    sehir = re.sub(r"\s+(ili|province)$", "", str(sehir).strip(), flags=re.IGNORECASE)
    return {"sehir": sehir, "ulke_kodu": ulke_kodu or "tr"}


def rota_koordinatlarini_bul(slugs):
    """Verilen slug listesi için sırayla [{yer, lat, lon}, ...] döner.
    Önbellekte olmayan her slug için Nominatim'e gidilir ve sonuç (bulunduysa)
    önbelleğe yazılır; bulunamayan slug'lar listeye hiç girmez."""
    onbellek = koordinat_yukle()
    sonuc = []
    guncellendi = False
    ilk_arama = True

    for slug in slugs:
        if not slug:
            continue

        kayit = onbellek.get(slug)
        if kayit is None:
            if not ilk_arama:
                time.sleep(1)  # Nominatim kullanım kuralı: sn başına en fazla 1 istek
            ilk_arama = False

            bulunan = nominatim_ara(slug)
            if bulunan is None:
                continue

            kayit = {"lat": bulunan[0], "lon": bulunan[1]}
            onbellek[slug] = kayit
            guncellendi = True

        sonuc.append({"yer": slug, "lat": kayit["lat"], "lon": kayit["lon"]})

    if guncellendi:
        koordinat_kaydet(onbellek)

    return sonuc


def _kus_ucusu_km(a, b):
    """İki koordinat arasındaki kuş uçuşu mesafeyi Haversine ile hesaplar."""
    yaricap = 6371.0
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return yaricap * 2 * math.asin(math.sqrt(h))


def rota_detaylarini_hesapla(koordinatlar, dil="tr"):
    """Ardışık rota durakları için yaklaşık mesafe, süre ve ulaşım önerisi.

    Harici bir yol tarifi servisine bağımlı olmadan karar desteği verir.
    Mesafe kuş uçuşudur; kara yolu karşılığı için kıvrım payı eklenir.
    """
    metinler = {
        "tr": {"yuruyus": "Yürüyüş", "taksi": "Taksi / yerel ulaşım", "arac": "Araç veya otobüs", "otobus": "Şehirlerarası otobüs veya araç", "ucak": "Uçak; alternatif olarak gece otobüsü", "dk": "dk", "sa": "sa"},
        "en": {"yuruyus": "Walking", "taksi": "Taxi / local transit", "arac": "Car or coach", "otobus": "Intercity coach or car", "ucak": "Flight; alternatively an overnight coach", "dk": "min", "sa": "hr"},
        "de": {"yuruyus": "Zu Fuß", "taksi": "Taxi / Nahverkehr", "arac": "Auto oder Bus", "otobus": "Fernbus oder Auto", "ucak": "Flug; alternativ Nachtbus", "dk": "Min.", "sa": "Std."},
        "ja": {"yuruyus": "徒歩", "taksi": "タクシー／地域交通", "arac": "車またはバス", "otobus": "長距離バスまたは車", "ucak": "飛行機（夜行バスも可）", "dk": "分", "sa": "時間"},
    }.get(dil, None)
    metinler = metinler or {
        "yuruyus": "Walking", "taksi": "Taxi / local transit", "arac": "Car or coach", "otobus": "Intercity coach or car",
        "ucak": "Flight; alternatively an overnight coach", "dk": "min", "sa": "hr",
    }
    detaylar = []
    for baslangic, varis in zip(koordinatlar, koordinatlar[1:]):
        kus_ucusu = _kus_ucusu_km(baslangic, varis)
        kara_ham = max(0.1, kus_ucusu * 1.22)
        kara_km = round(kara_ham, 1) if kara_ham < 10 else round(kara_ham)

        min_dakika = 15
        if kara_km <= 2.5:
            ulasim, hiz, ek_sure, min_dakika = metinler["yuruyus"], 4.5, 0, 5
        elif kara_km <= 15:
            ulasim, hiz, ek_sure = metinler["taksi"], 28, 0.15
        elif kara_km <= 120:
            ulasim, hiz, ek_sure = metinler["arac"], 65, 0.35
        elif kara_km <= 450:
            ulasim, hiz, ek_sure = metinler["otobus"], 72, 0.6
        else:
            ulasim, hiz, ek_sure = metinler["ucak"], 520, 2.2

        saat = kara_km / hiz + ek_sure
        if saat < 1:
            sure = f"{max(min_dakika, round(saat * 60 / 5) * 5)} {metinler['dk']}"
        else:
            tam_saat = int(saat)
            dakika = round((saat - tam_saat) * 60 / 5) * 5
            sure = f"{tam_saat} {metinler['sa']}" + (f" {dakika} {metinler['dk']}" if dakika else "")

        detaylar.append({
            "baslangic": baslangic["yer"],
            "varis": varis["yer"],
            "yaklasik_km": kara_km,
            "tahmini_sure": sure,
            "ulasim": ulasim,
        })
    return detaylar
