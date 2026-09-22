"""Kotasız, açıklanabilir ve oturum profiline duyarlı günlük plan motoru."""
import json
import os
import re
from math import radians, sin, cos, asin, sqrt

import konum
import yakinimda


ISTANBUL = [
    {"slug":"ayasofya", "ad":"Ayasofya", "lat":41.0086, "lon":28.9802, "sure":70, "temalar":["tarih","sanat"], "tur":"tarihi yapı"},
    {"slug":"yerebatan-sarnici", "ad":"Yerebatan Sarnıcı", "lat":41.0084, "lon":28.9779, "sure":50, "temalar":["tarih","sakin"], "tur":"tarihi yapı"},
    {"slug":"topkapi-sarayi", "ad":"Topkapı Sarayı", "lat":41.0115, "lon":28.9834, "sure":120, "temalar":["tarih","sanat","aile"], "tur":"müze"},
    {"slug":"gulhane-parki", "ad":"Gülhane Parkı", "lat":41.0133, "lon":28.9811, "sure":45, "temalar":["doga","sakin","aile"], "tur":"park"},
    {"slug":"istanbul-arkeoloji-muzeleri", "ad":"İstanbul Arkeoloji Müzeleri", "lat":41.0117, "lon":28.9813, "sure":100, "temalar":["tarih","sanat"], "tur":"müze"},
    {"slug":"sultanahmet-camii", "ad":"Sultanahmet Camii", "lat":41.0054, "lon":28.9768, "sure":45, "temalar":["tarih","sanat","sakin"], "tur":"cami"},
    {"slug":"misir-carsisi", "ad":"Mısır Çarşısı", "lat":41.0165, "lon":28.9705, "sure":55, "temalar":["yemek","sanat","aile"], "tur":"çarşı"},
    {"slug":"galata-kulesi", "ad":"Galata Kulesi", "lat":41.0256, "lon":28.9741, "sure":65, "temalar":["tarih","macera","sanat"], "tur":"tarihi yapı"},
]

ANKARA = [
    {"slug":"anitkabir", "ad":"Anıtkabir", "lat":39.9251, "lon":32.8369, "sure":90, "temalar":["tarih","aile"], "tur":"anıtsal müze"},
    {"slug":"anadolu-medeniyetleri-muzesi", "ad":"Anadolu Medeniyetleri Müzesi", "lat":39.9385, "lon":32.8619, "sure":100, "temalar":["tarih","sanat","aile"], "tur":"müze"},
    {"slug":"ankara-kalesi", "ad":"Ankara Kalesi", "lat":39.9412, "lon":32.8644, "sure":70, "temalar":["tarih","macera"], "tur":"kale"},
    {"slug":"hamamonu", "ad":"Hamamönü", "lat":39.9323, "lon":32.8694, "sure":65, "temalar":["tarih","sanat","yemek"], "tur":"tarihi semt"},
    {"slug":"haci-bayram-camii", "ad":"Hacı Bayram Camii", "lat":39.9441, "lon":32.8596, "sure":45, "temalar":["tarih","sakin"], "tur":"cami"},
    {"slug":"eymir", "ad":"Eymir Gölü", "lat":39.8154, "lon":32.8365, "sure":100, "temalar":["doga","sakin","aile","macera"], "tur":"göl"},
]

KAPADOKYA = [
    {"slug":"goreme-acik-hava-muzesi", "ad":"Göreme Açık Hava Müzesi", "lat":38.6400, "lon":34.8450, "sure":110, "temalar":["tarih","sanat"], "tur":"açık hava müzesi"},
    {"slug":"uchisar-kalesi", "ad":"Uçhisar Kalesi", "lat":38.6307, "lon":34.8050, "sure":70, "temalar":["tarih","macera","doga"], "tur":"kale"},
    {"slug":"avanos", "ad":"Avanos", "lat":38.7153, "lon":34.8467, "sure":90, "temalar":["sanat","yemek","aile"], "tur":"kasaba ve çömlek atölyeleri"},
    {"slug":"pasabaglari", "ad":"Paşabağları", "lat":38.6770, "lon":34.8537, "sure":65, "temalar":["doga","macera","aile"], "tur":"peri bacaları"},
    {"slug":"kaymakli-yeralti-sehri", "ad":"Kaymaklı Yeraltı Şehri", "lat":38.4604, "lon":34.7518, "sure":80, "temalar":["tarih","macera"], "tur":"yeraltı şehri"},
    {"slug":"goreme", "ad":"Göreme Seyir Noktası", "lat":38.6431, "lon":34.8289, "sure":45, "temalar":["doga","sakin","sanat"], "tur":"manzara"},
]

ANTALYA = [
    {"slug":"kaleici", "ad":"Kaleiçi", "lat":36.8848, "lon":30.7046, "sure":90, "temalar":["tarih","sanat","yemek"], "tur":"tarihi semt"},
    {"slug":"hadrian-kapisi", "ad":"Hadrian Kapısı", "lat":36.8851, "lon":30.7086, "sure":35, "temalar":["tarih","sanat"], "tur":"anıtsal kapı"},
    {"slug":"antalya-muzesi", "ad":"Antalya Müzesi", "lat":36.8858, "lon":30.6802, "sure":100, "temalar":["tarih","sanat","aile"], "tur":"müze"},
    {"slug":"duden-selalesi", "ad":"Aşağı Düden Şelalesi", "lat":36.8514, "lon":30.7830, "sure":65, "temalar":["doga","sakin","aile"], "tur":"şelale"},
    {"slug":"konyaalti-sahili", "ad":"Konyaaltı Sahili", "lat":36.8675, "lon":30.6435, "sure":90, "temalar":["deniz","sakin","aile"], "tur":"sahil"},
    {"slug":"karaalioglu-parki", "ad":"Karaalioğlu Parkı", "lat":36.8805, "lon":30.7040, "sure":45, "temalar":["doga","deniz","sakin"], "tur":"park"},
]

GAZIANTEP = [
    {"slug":"zeugma-mozaik-muzesi", "ad":"Zeugma Mozaik Müzesi", "lat":37.0751, "lon":37.3866, "sure":110, "temalar":["tarih","sanat","aile"], "tur":"müze"},
    {"slug":"gaziantep-kalesi", "ad":"Gaziantep Kalesi", "lat":37.0662, "lon":37.3833, "sure":55, "temalar":["tarih","macera"], "tur":"kale"},
    {"slug":"bakircilar-carsisi", "ad":"Bakırcılar Çarşısı", "lat":37.0628, "lon":37.3825, "sure":65, "temalar":["sanat","yemek","tarih"], "tur":"çarşı"},
    {"slug":"emines-gogus-mutfak-muzesi", "ad":"Emine Göğüş Mutfak Müzesi", "lat":37.0647, "lon":37.3820, "sure":50, "temalar":["yemek","tarih","aile"], "tur":"mutfak müzesi"},
    {"slug":"zincirli-bedesten", "ad":"Zincirli Bedesten", "lat":37.0632, "lon":37.3811, "sure":45, "temalar":["yemek","sanat"], "tur":"bedesten"},
    {"slug":"rumkale", "ad":"Rumkale", "lat":37.2690, "lon":37.8374, "sure":120, "temalar":["tarih","doga","macera"], "tur":"kale ve manzara"},
]

SEHIRLER = {
    "istanbul": {"ad":"İstanbul", "ad_da":"İstanbul’da", "merkez":(41.0084, 28.9784), "yerler":ISTANBUL},
    "ankara": {"ad":"Ankara", "ad_da":"Ankara’da", "merkez":(39.9334, 32.8597), "yerler":ANKARA},
    "kapadokya": {"ad":"Kapadokya", "ad_da":"Kapadokya’da", "merkez":(38.6431, 34.8289), "yerler":KAPADOKYA},
    "antalya": {"ad":"Antalya", "ad_da":"Antalya’da", "merkez":(36.8850, 30.7050), "yerler":ANTALYA},
    "gaziantep": {"ad":"Gaziantep", "ad_da":"Gaziantep’te", "merkez":(37.0659, 37.3781), "yerler":GAZIANTEP},
}


# ---- Elle kayıtlı 5 şehir dışındaki HER şehir için: Nominatim (merkez) +
# Overpass (yakinimda.ara, "Yakınımda" özelliğiyle aynı zincir) ile otomatik
# gezilecek yer keşfi. Sonuç diske önbelleklenir (aynı şehir bir daha ağa
# çıkmadan gelsin) — SEHIRLER'deki 5 şehir gibi elle veri girmeye gerek kalmaz.

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
SEHIR_MEKAN_YOLU = os.path.join(TEMEL_DIZIN, "sehir-mekanlari.json")

# Overpass'ın tek "tur" etiketini plan motorunun ihtiyaç duyduğu tema
# listesine ve kaba bir ziyaret süresine (dk) çevirir — basit ama yeterli.
_TUR_TEMA_SURE = {
    "muze": (["tarih", "sanat"], 90),
    "manzara": (["doga", "sakin"], 40),
    "ibadet-yeri": (["tarih", "sakin"], 35),
    "park": (["doga", "sakin", "aile"], 50),
    "tarihi-yapi": (["tarih"], 60),
    "turistik-yer": (["tarih", "sanat"], 55),
}


def _sehir_slug(ad):
    ceviri = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", (ad or "").translate(ceviri).lower()).strip("-")


def _yer_eki_bul(ad):
    """Kaba ama makul bir Türkçe bulunma hâli eki tahmini (büyük/küçük ünlü
    uyumu + son ünsüz sertleşmesi) — elle kayıtlı 5 şehrin ekleriyle
    (İstanbul'da, Gaziantep'te...) örtüşecek şekilde doğrulandı."""
    temiz = (ad or "").strip()
    if not temiz:
        return "'da"
    sert_unsuzler = set("çfhkpsştÇFHKPSŞT")
    kalin_unluler = set("aıouAIOU")
    ince_unluler = set("eiöüEİÖÜ")
    son_unlu_ince = False
    for harf in reversed(temiz):
        if harf in kalin_unluler:
            break
        if harf in ince_unluler:
            son_unlu_ince = True
            break
    unsuz = "t" if temiz[-1] in sert_unsuzler else "d"
    unlu = "e" if son_unlu_ince else "a"
    return f"'{unsuz}{unlu}"


def _sehir_onbellegini_yukle():
    if os.path.exists(SEHIR_MEKAN_YOLU):
        with open(SEHIR_MEKAN_YOLU, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _sehir_onbellegini_kaydet(veri):
    with open(SEHIR_MEKAN_YOLU, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2, sort_keys=True)


def _yerleri_apiden_olustur(ham_yerler):
    sonuc = []
    for oge in ham_yerler:
        temalar, sure = _TUR_TEMA_SURE.get(oge["tur"], (["tarih"], 55))
        sonuc.append({
            "slug": oge["slug"], "ad": oge["ad"], "lat": oge["lat"], "lon": oge["lon"],
            "sure": sure, "temalar": temalar, "tur": oge["tur"],
        })
    return sonuc


def _sehir_bilgisini_apiden_getir(sehir_adi):
    """SEHIRLER'de olmayan bir şehir/yer adı için: önce diskteki önbelleğe
    bakar; yoksa Nominatim'le merkezini bulur, Overpass'la ("Yakınımda"
    özelliğiyle aynı fonksiyon) 5 km çevresindeki gezilecek yerleri çeker.
    Hiçbiri bulunamazsa None döner (çağıran zaten bunu zarifçe ele alıyor)."""
    slug = _sehir_slug(sehir_adi)
    if not slug:
        return None

    onbellek = _sehir_onbellegini_yukle()
    kayitli = onbellek.get(slug)
    if kayitli and kayitli.get("yerler"):
        return {**kayitli, "merkez": tuple(kayitli["merkez"])}

    merkez = konum.nominatim_ara(sehir_adi)
    if merkez is None:
        return None
    lat, lon = merkez

    try:
        # Şehir çapında bir sorgu küçük "yakınımda" sorgusundan daha ağırdır
        # ve bu yalnızca (diske önbelleklendiği için) o şehir için TEK
        # seferlik bir maliyettir — varsayılan 4 sn'lik canlı bütçe yerine
        # daha cömert bir zaman aşımı kullanılır.
        ham_yerler = yakinimda.ara(lat, lon, 5000, timeout=20)
    except Exception:
        ham_yerler = []
    if not ham_yerler:
        return None

    goruntu_adi = sehir_adi.strip().title()
    kayit = {
        "ad": goruntu_adi, "ad_da": f"{goruntu_adi}{_yer_eki_bul(goruntu_adi)}",
        "merkez": [lat, lon], "yerler": _yerleri_apiden_olustur(ham_yerler),
    }
    onbellek[slug] = kayit
    _sehir_onbellegini_kaydet(onbellek)
    return {**kayit, "merkez": (lat, lon)}


def mesafe_km(a_lat, a_lon, b_lat, b_lon):
    dlat, dlon = radians(b_lat-a_lat), radians(b_lon-a_lon)
    x = sin(dlat/2)**2 + cos(radians(a_lat))*cos(radians(b_lat))*sin(dlon/2)**2
    return 6371 * 2 * asin(sqrt(x))


def plan_olustur(sehir="istanbul", sure="yarim-gun", ulasim="yuruyus", ilgi="tarih",
                 tempo="dengeli", profil=None, lat=None, lon=None, kosul=None):
    sehir_ham = str(sehir or "istanbul").strip()
    sehir_bilgisi = SEHIRLER.get(_sehir_slug(sehir_ham)) or SEHIRLER.get(sehir_ham)
    if not sehir_bilgisi:
        # 5 elle kayıtlı şehrin dışında: Nominatim + Overpass ile otomatik
        # keşfet (bkz. _sehir_bilgisini_apiden_getir) — her şehri elle
        # eklemeye gerek kalmasın diye.
        sehir_bilgisi = _sehir_bilgisini_apiden_getir(sehir_ham)
    if not sehir_bilgisi:
        return None
    if kosul == "vakit-az":
        sure = "2-saat"
    if kosul == "yoruldum":
        tempo = "rahat"
    dakika_siniri = {"2-saat":120, "yarim-gun":300, "tam-gun":480}.get(sure, 300)
    tempo_carpani = {"rahat":1.2, "dengeli":1.0, "yogun":.82}.get(tempo, 1.0)
    sehir_lat, sehir_lon = sehir_bilgisi["merkez"]
    konum_geldi = lat is not None and lon is not None
    gelen_lat = float(lat) if konum_geldi else sehir_lat
    gelen_lon = float(lon) if konum_geldi else sehir_lon
    # Yanlış şehir seçimi günlük planı yüzlerce kilometre uzağa taşımamalı.
    # Konum şehir merkezinden 80 km'den uzaktaysa şehir merkezi kullanılır.
    konum_sehre_uygun = konum_geldi and mesafe_km(gelen_lat, gelen_lon, sehir_lat, sehir_lon) <= 80
    merkez_lat = gelen_lat if konum_sehre_uygun else sehir_lat
    merkez_lon = gelen_lon if konum_sehre_uygun else sehir_lon
    profil = profil or {}

    adaylar = []
    for yer in sehir_bilgisi["yerler"]:
        uzaklik = mesafe_km(merkez_lat, merkez_lon, yer["lat"], yer["lon"])
        yakinlik = max(0, 30 - uzaklik * 5)
        # Kullanıcının bu plan için açıkça seçtiği ilgi, yalnızca geçmişten
        # çıkarılan profile ve salt yakınlığa göre daha güçlü bir sinyaldir.
        acik_ilgi = 45 if ilgi in yer["temalar"] else 0
        profil_uyumu = min(18, sum(profil.get(t, 0) * 4 for t in yer["temalar"]))
        aile_bonus = 8 if ilgi == "aile" and "aile" in yer["temalar"] else 0
        kosul_puani = 0
        if kosul == "aciktim":
            kosul_puani += 60 if "yemek" in yer["temalar"] else -10
        elif kosul == "yoruldum":
            kosul_puani += (28 if "sakin" in yer["temalar"] else 0) - yer["sure"] * .12 - uzaklik * 3
        elif kosul == "yagmur":
            acik_hava = any(k in yer["tur"] for k in ("park", "sahil", "şelale", "manzara", "göl", "peri bacaları"))
            kosul_puani += -55 if acik_hava else 32
        adaylar.append({**yer, "uzaklik":uzaklik, "puan":round(yakinlik+acik_ilgi+profil_uyumu+aile_bonus+kosul_puani, 1)})
    adaylar.sort(key=lambda x: (-x["puan"], x["uzaklik"]))

    secilen, kullanilan = [], 0
    for yer in adaylar:
        ziyaret = round(yer["sure"] * tempo_carpani)
        ulasim_dk = 0 if not secilen else round(mesafe_km(secilen[-1]["lat"], secilen[-1]["lon"], yer["lat"], yer["lon"]) / ({"yuruyus":4.5,"toplu-tasima":16,"arac":22}.get(ulasim,4.5)) * 60 + (8 if ulasim=="toplu-tasima" else 0))
        if kullanilan + ziyaret + ulasim_dk > dakika_siniri:
            continue
        secilen.append({**yer, "ziyaret_dk":ziyaret, "ulasim_dk":ulasim_dk})
        kullanilan += ziyaret + ulasim_dk
        if len(secilen) >= (3 if sure=="2-saat" else 5 if sure=="yarim-gun" else 7):
            break

    # İlk seçimin ardından durakları en yakın komşuyla düzenleyerek zikzakları azalt.
    sirali, kalan = [], secilen[:]
    onceki = {"lat":merkez_lat, "lon":merkez_lon}
    while kalan:
        nxt = min(kalan, key=lambda y: mesafe_km(onceki["lat"], onceki["lon"], y["lat"], y["lon"]))
        kalan.remove(nxt); sirali.append(nxt); onceki = nxt

    saat = 10 * 60
    duraklar, toplam_km = [], 0
    onceki = {"lat":merkez_lat, "lon":merkez_lon}
    hiz = {"yuruyus":4.5,"toplu-tasima":16,"arac":22}.get(ulasim,4.5)
    for i, yer in enumerate(sirali):
        km = mesafe_km(onceki["lat"], onceki["lon"], yer["lat"], yer["lon"])
        yol_dk = round(km/hiz*60 + (8 if ulasim=="toplu-tasima" else 0)) if i else round(km/4.5*60)
        if i: saat += yol_dk
        neden = f"{ilgi} ilgine uyuyor"
        if profil and any(profil.get(t, 0) for t in yer["temalar"]): neden += " ve gezgin profilinle örtüşüyor"
        if kosul == "aciktim" and "yemek" in yer["temalar"]: neden += "; yemek molasına uygun"
        elif kosul == "yoruldum" and "sakin" in yer["temalar"]: neden += "; daha sakin bir durak"
        elif kosul == "yagmur": neden += "; yağmurda daha korunaklı"
        elif kosul == "vakit-az": neden += "; kalan kısa sürene sığıyor"
        neden += f"; önceki durağa yaklaşık {km:.1f} km"
        duraklar.append({"saat":f"{saat//60:02d}:{saat%60:02d}", "slug":yer["slug"], "ad":yer["ad"], "tur":yer["tur"], "sure_dk":yer["ziyaret_dk"], "neden":neden, "puan":yer["puan"], "lat":yer["lat"], "lon":yer["lon"], "ulasim":{"tur":ulasim,"sure_dk":yol_dk,"mesafe_km":round(km,1)}})
        saat += yer["ziyaret_dk"]; toplam_km += km; onceki = yer
    uyarlama = {"yoruldum":"Tempo rahatlatıldı; kısa, sakin ve yakın duraklar öne alındı.", "yagmur":"Açık hava durakları geri plana alındı; korunaklı mekânlar seçildi.", "aciktim":"Yemek ve çarşı deneyimleri rotada öne alındı.", "vakit-az":"Plan kalan iki saate sığacak şekilde kısaltıldı."}.get(kosul)
    konum_notu = None
    if konum_geldi and not konum_sehre_uygun:
        konum_notu = f"Mevcut konum {sehir_bilgisi['ad']} planlama bölgesinin dışında olduğu için şehir merkezi başlangıç alındı."
    elif konum_sehre_uygun:
        konum_notu = "Plan mevcut konumuna göre sıralandı."
    return {"baslik":f"{sehir_bilgisi['ad_da']} {ilgi} odaklı bir gün", "sehir":sehir_bilgisi["ad"], "kisisellestirme":[ilgi, tempo, ulasim], "kosul":kosul, "uyarlama_notu":uyarlama, "konum_kullanildi":konum_sehre_uygun, "konum_notu":konum_notu, "toplam_sure_dk":kullanilan, "toplam_mesafe_km":round(toplam_km,1), "duraklar":duraklar, "rota":[d["slug"] for d in duraklar], "uyarilar":["Ziyaret saatlerini ve bilet durumunu resmî kaynaklardan kontrol et."]}
