"""OpenStreetMap/Overpass üzerinden yakındaki turistik noktaları bulur."""

import json
import math
import re
import time
import urllib.parse
import urllib.request

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
)
USER_AGENT = "EvliyaCelebiAI/0.1 (staj projesi)"
_ONBELLEK = {}


DEMO_NOKTALARI = [
    ("ayasofya", "Ayasofya", "tarihi-yapi", 41.0086, 28.9802),
    ("sultanahmet-camii", "Sultanahmet Camii", "cami", 41.0054, 28.9768),
    ("yerebatan-sarnici", "Yerebatan Sarnıcı", "muze", 41.0084, 28.9779),
    ("topkapi-sarayi", "Topkapı Sarayı", "muze", 41.0115, 28.9834),
    ("gulhane-parki", "Gülhane Parkı", "park", 41.0132, 28.9810),
    ("istanbul-arkeoloji-muzeleri", "İstanbul Arkeoloji Müzeleri", "muze", 41.0117, 28.9813),
]


def _mesafe_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _slug_yap(metin):
    ceviri = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    sonuc = re.sub(r"[^a-z0-9]+", "-", metin.translate(ceviri).lower()).strip("-")
    return sonuc[:70] or "gezilecek-yer"


def _tur_bul(tags):
    if tags.get("tourism") == "museum": return "muze"
    if tags.get("tourism") == "viewpoint": return "manzara"
    if tags.get("amenity") == "place_of_worship": return "ibadet-yeri"
    if tags.get("leisure") == "park": return "park"
    if tags.get("historic"): return "tarihi-yapi"
    return "turistik-yer"


def _kayit(slug, ad, tur, lat, lon, merkez_lat, merkez_lon):
    km = _mesafe_km(merkez_lat, merkez_lon, lat, lon)
    yuruyus_dk = max(1, round(km / 4.5 * 60))
    return {"slug": slug, "ad": ad, "tur": tur, "lat": lat, "lon": lon,
            "mesafe_km": round(km, 2), "yuruyus_dk": yuruyus_dk}


def demo_sonuclari(yaricap_m=3000):
    merkez_lat, merkez_lon = 41.0084, 28.9784
    sonuc = [
        _kayit(slug, ad, tur, lat, lon, merkez_lat, merkez_lon)
        for slug, ad, tur, lat, lon in DEMO_NOKTALARI
        if _mesafe_km(merkez_lat, merkez_lon, lat, lon) * 1000 <= yaricap_m
    ]
    sonuc.sort(key=lambda x: x["mesafe_km"])
    return sonuc


def yerel_yedek_sonuclari(lat, lon, yaricap_m, koordinatlar, izinli_sluglar):
    """Overpass yokken paketli koordinatlardan yakın, sınırlı sonuç üretir."""
    adaylar = list(DEMO_NOKTALARI)
    for slug, koordinat in (koordinatlar or {}).items():
        if slug not in izinli_sluglar:
            continue
        adaylar.append((slug, slug.replace("-", " ").title(), "turistik-yer", koordinat["lat"], koordinat["lon"]))
    sonuc, gorulen = [], set()
    for slug, ad, tur, yer_lat, yer_lon in adaylar:
        if slug in gorulen:
            continue
        kayit = _kayit(slug, ad, tur, yer_lat, yer_lon, lat, lon)
        if kayit["mesafe_km"] * 1000 <= yaricap_m:
            gorulen.add(slug)
            sonuc.append(kayit)
    sonuc.sort(key=lambda x: x["mesafe_km"])
    return sonuc[:20]


def ara(lat, lon, yaricap_m=3000, timeout=4):
    yaricap_m = max(500, min(int(yaricap_m), 5000))
    anahtar = (round(lat, 3), round(lon, 3), yaricap_m)
    eski = _ONBELLEK.get(anahtar)
    if eski and time.time() - eski[0] < 600:
        return eski[1]

    # Küçük bounding-box sorgusu, genel around sorgusundan daha hafiftir.
    lat_farki = yaricap_m / 111_320
    lon_farki = yaricap_m / max(1, 111_320 * math.cos(math.radians(lat)))
    bbox = f"{lat-lat_farki},{lon-lon_farki},{lat+lat_farki},{lon+lon_farki}"
    sorgu = f'''[out:json][timeout:6];(
      nwr["tourism"~"attraction|museum|viewpoint"]({bbox});
      nwr["historic"]({bbox});
      nwr["amenity"="place_of_worship"]["name"]({bbox});
      nwr["leisure"="park"]["name"]({bbox});
    );out center tags 60;'''
    veri = urllib.parse.urlencode({"data": sorgu}).encode("utf-8")
    son_hata = None
    ham = None
    for adres in OVERPASS_URLS:
        istek = urllib.request.Request(adres, data=veri, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(istek, timeout=timeout) as yanit:
                ham = json.loads(yanit.read().decode("utf-8"))
            break
        except Exception as hata:
            son_hata = hata
    if ham is None:
        raise son_hata or RuntimeError("Overpass yanıt vermedi")

    sonuc, gorulen = [], set()
    for oge in ham.get("elements", []):
        tags = oge.get("tags") or {}
        ad = tags.get("name:tr") or tags.get("name:en") or tags.get("name")
        merkez = oge.get("center") or oge
        if not ad or "lat" not in merkez or "lon" not in merkez:
            continue
        slug = _slug_yap(ad)
        if slug in gorulen:
            continue
        kayit = _kayit(slug, ad, _tur_bul(tags), float(merkez["lat"]), float(merkez["lon"]), lat, lon)
        if kayit["mesafe_km"] * 1000 <= yaricap_m:
            gorulen.add(slug)
            sonuc.append(kayit)
    sonuc.sort(key=lambda x: x["mesafe_km"])
    sonuc = sonuc[:20]
    _ONBELLEK[anahtar] = (time.time(), sonuc)
    return sonuc
