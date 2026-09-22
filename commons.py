# -*- coding: utf-8 -*-
"""
Görsel kaynağı ortak modülü — dört kademeli zincir: yerel önbellek (assets/)
-> Wikimedia Commons -> Openverse -> Pexels (PEXELS_API_KEY gerekir; diğer
ikisi anahtar istemez). Birleşik gorsel_bul() burada. gorsel_indir.py (toplu,
önceden indirme) ve app.py (canlı/dinamik tamamlama) aynı fonksiyonları
paylaşır.
"""

import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

import openverse
import pexels

USER_AGENT = "EvliyaCelebiAI/0.1 (staj projesi)"
API_URL = "https://commons.wikimedia.org/w/api.php"

MIN_GENISLIK = 800
GECERLI_UZANTILAR = (".jpg", ".jpeg")
GECERSIZ_ICERIR = ("map", "logo", "icon", "diagram", "location")


def url_getir(url, timeout=30, max_deneme=4, bekleme=20):
    """429 (çok istek) alınırsa Retry-After'a (veya sabit süreye) göre
    bekleyip tekrar dener; max_deneme=1 verilirse hiç tekrar denemeden
    ilk hatada yükseltir (canlı/gecikmeye duyarlı çağrılar için)."""
    istek = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for deneme in range(max_deneme):
        try:
            with urllib.request.urlopen(istek, timeout=timeout) as yanit:
                return yanit.read()
        except urllib.error.HTTPError as hata:
            if hata.code == 429 and deneme < max_deneme - 1:
                bekleme_suresi = bekleme
                retry_after = hata.headers.get("Retry-After") if hata.headers else None
                if retry_after:
                    try:
                        bekleme_suresi = max(bekleme, int(retry_after))
                    except ValueError:
                        pass
                print(f"   ... 429 alındı, {bekleme_suresi} sn bekleyip tekrar denenecek ({deneme + 1}/{max_deneme})")
                time.sleep(bekleme_suresi)
                continue
            raise
    raise RuntimeError("429: çok fazla denemeden sonra vazgeçildi")


def api_istek(params, timeout=20, max_deneme=4):
    sorgu = dict(params)
    sorgu.setdefault("format", "json")
    url = API_URL + "?" + urllib.parse.urlencode(sorgu)
    return json.loads(url_getir(url, timeout=timeout, max_deneme=max_deneme).decode("utf-8"))


def etiket_temizle(metin):
    """extmetadata alanları (ör. Artist) HTML içerebilir; etiketleri temizler."""
    if not metin:
        return ""
    temiz = re.sub(r"<[^>]+>", "", metin)
    return html.unescape(temiz).strip()


def uygun_mu(dosya_basligi, genislik):
    if not dosya_basligi:
        return False
    kucuk = dosya_basligi.lower()
    if not kucuk.endswith(GECERLI_UZANTILAR):
        return False
    if any(kelime in kucuk for kelime in GECERSIZ_ICERIR):
        return False
    if genislik is not None and genislik < MIN_GENISLIK:
        return False
    return True


def gorsel_bul_coklu(sorgu, adet=3, timeout=20, max_deneme=4):
    """Commons'ta arar, en fazla `adet` uygun (800px+ JPEG, SVG/PDF/harita
    değil) sonucu bir liste olarak döner (yeterli bulunamazsa daha kısa
    olabilir, hiç yoksa boş liste). timeout/max_deneme çağırana göre ayarlanır."""
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": sorgu,
        "gsrnamespace": 6,
        "gsrlimit": max(10, adet * 4),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": 1200,
    }
    veri = api_istek(params, timeout=timeout, max_deneme=max_deneme)
    sayfalar = (veri.get("query") or {}).get("pages") or {}
    if not sayfalar:
        return []

    sirali = sorted(sayfalar.values(), key=lambda s: s.get("index", 9999))

    sonuclar = []
    for sayfa in sirali:
        imageinfo = sayfa.get("imageinfo")
        if not imageinfo:
            continue
        bilgi = imageinfo[0]
        baslik = sayfa.get("title", "")
        genislik = bilgi.get("width")
        if not uygun_mu(baslik, genislik):
            continue
        sonuclar.append({
            "baslik": baslik,
            "indirme_url": bilgi.get("thumburl") or bilgi.get("url"),
            "aciklama_url": bilgi.get("descriptionurl") or "",
            "extmetadata": bilgi.get("extmetadata") or {},
        })
        if len(sonuclar) >= adet:
            break
    return sonuclar


def dosya_indir(url, hedef_yol, timeout=30, max_deneme=4):
    veri = url_getir(url, timeout=timeout, max_deneme=max_deneme)
    with open(hedef_yol, "wb") as f:
        f.write(veri)


def katalog_yukle(katalog_yolu):
    if os.path.exists(katalog_yolu):
        with open(katalog_yolu, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def katalog_kaydet(katalog, katalog_yolu):
    with open(katalog_yolu, "w", encoding="utf-8") as f:
        json.dump(katalog, f, ensure_ascii=False, indent=2)


def katalog_gorseller_ekle(katalog, slug, yeni_gorseller, varsayilan_temalar=None):
    """slug zaten katalogdaysa gorseller listesine (dosya adına göre, kopyasız)
    ekler; yoksa yeni kayıt oluşturur. yeni_gorseller: [{dosya, lisans,
    fotografci, kaynak_url}, ...]. Görsel akışı (çoklu foto) ve video
    (youtube_id, elle eklenir) aynı kaydı paylaşır."""
    for kayit in katalog:
        if slug in (kayit.get("yerler") or []):
            mevcut = kayit.setdefault("gorseller", [])
            mevcut_dosyalar = {g.get("dosya") for g in mevcut}
            for g in yeni_gorseller:
                if g.get("dosya") not in mevcut_dosyalar:
                    mevcut.append(g)
                    mevcut_dosyalar.add(g.get("dosya"))
            return katalog
    katalog.append({
        "yerler": [slug],
        "temalar": varsayilan_temalar or [],
        "gorseller": list(yeni_gorseller),
        "genel": False,
    })
    return katalog


def extmetadata_ayikla(extmetadata):
    """extmetadata sözlüğünden temizlenmiş (lisans, fotoğrafçı) çifti döner."""
    lisans = etiket_temizle((extmetadata.get("LicenseShortName") or {}).get("value")) or "bilinmiyor"
    fotografci = etiket_temizle((extmetadata.get("Artist") or {}).get("value")) or "bilinmiyor"
    return lisans, fotografci


def _commons_indir(sonuclar, hedef_dosyalar, assets_dizin):
    gorseller = []
    for dosya_adi, sonuc in zip(hedef_dosyalar, sonuclar):
        hedef_yol = os.path.join(assets_dizin, dosya_adi)
        time.sleep(1)
        try:
            dosya_indir(sonuc["indirme_url"], hedef_yol)
        except Exception:
            continue
        lisans, fotografci = extmetadata_ayikla(sonuc["extmetadata"])
        gorseller.append({
            "dosya": dosya_adi,
            "lisans": lisans,
            "fotografci": fotografci,
            "kaynak_url": sonuc["aciklama_url"],
            "kaynak": "commons",
        })
    return gorseller


def _openverse_indir(sonuclar, hedef_dosyalar, assets_dizin):
    gorseller = []
    for dosya_adi, sonuc in zip(hedef_dosyalar, sonuclar):
        hedef_yol = os.path.join(assets_dizin, dosya_adi)
        time.sleep(1)
        try:
            openverse.dosya_indir(sonuc["indirme_url"], hedef_yol)
        except Exception:
            continue
        gorseller.append({
            "dosya": dosya_adi,
            "lisans": sonuc["lisans"],
            "fotografci": sonuc["fotografci"],
            "kaynak_url": sonuc["kaynak_url"],
            "kaynak": "openverse",
        })
    return gorseller


def _pexels_indir(sonuclar, hedef_dosyalar, assets_dizin):
    gorseller = []
    for dosya_adi, sonuc in zip(hedef_dosyalar, sonuclar):
        hedef_yol = os.path.join(assets_dizin, dosya_adi)
        time.sleep(1)
        try:
            pexels.dosya_indir(sonuc["indirme_url"], hedef_yol)
        except Exception:
            continue
        gorseller.append({
            "dosya": dosya_adi,
            "lisans": "Pexels License",
            "fotografci": sonuc["fotografci"],
            "kaynak_url": sonuc["kaynak_url"],
            "kaynak": "pexels",
        })
    return gorseller


def _sorgu_varyantlarini_olustur(slug, sorgu, tema, ek_terimler):
    """Basit alaka skoru: en spesifik sorgu önce denenir, slotlar dolana kadar
    sırayla bir sonrakine geçilir — o yüzden erken varyantlardan gelen
    görseller (o turda Evliya'nın bahsettiği lezzet/deneyimle eşleşen) her
    zaman genel "{slug} Turkey" sonucundan önce sıraya girer."""
    if sorgu:
        return [sorgu]

    varyantlar = []
    for terim in (ek_terimler or []):
        if terim:
            varyantlar.append(f"{slug} {terim.replace('-', ' ')}")
    varyantlar.append(f"{slug} Turkey" + (f" {tema}" if tema else ""))

    gorulen = set()
    sirali = []
    for v in varyantlar:
        if v not in gorulen:
            gorulen.add(v)
            sirali.append(v)
    return sirali


def gorsel_bul(slug, assets_dizin, sorgu=None, adet=6, tema=None, ek_terimler=None):
    """Bir yer (slug) için hedef `adet` (varsayılan 6) görsel toplar. `sorgu`
    verilmezse, `ek_terimler` (ör. o turda geçen lezzet/deneyim adları) ve
    `tema`'dan bir sorgu VARYANT LİSTESİ kurulur — en spesifik önce (bkz.
    _sorgu_varyantlarini_olustur) — ve slotlar dolana kadar sırayla dener:
    1) assets/ klasöründe zaten `adet` kadar dosya varsa (önbellek) hiç ağa
       çıkmadan boş sonuç döner (çağıran zaten diskteki dosyaları kullanır).
    2) Her varyant için sırayla: Wikimedia Commons -> (hâlâ eksikse) Openverse
       (license_type=commercial, JPEG, anahtar gerekmez) -> (hâlâ eksikse)
       Pexels; üçü de aynı varyantın sorgu metnini kullanır.
    3) Hiçbiri bulamazsa boş döner — çağıran isim kartına düşer, hata fırlamaz.

    Döner: {"kaynak": "onbellek" | "commons" | "openverse" | "pexels" |
            "commons+openverse" (birden fazla kaynak karıştıysa) | None,
            "gorseller": [{"dosya","lisans","fotografci","kaynak_url","kaynak"}, ...]}
    """
    hedef_dosyalar = [f"{slug}-{i:02d}.jpg" for i in range(1, adet + 1)]
    eksikler = [d for d in hedef_dosyalar if not os.path.exists(os.path.join(assets_dizin, d))]

    if not eksikler:
        return {"kaynak": "onbellek", "gorseller": []}

    varyantlar = _sorgu_varyantlarini_olustur(slug, sorgu, tema, ek_terimler)

    kalan = list(eksikler)
    toplanan = []
    kullanilan_kaynaklar = []

    for arama_sorgusu in varyantlar:
        if not kalan:
            break

        # Commons
        try:
            commons_sonuclari = gorsel_bul_coklu(arama_sorgusu, adet=len(kalan))
        except Exception:
            commons_sonuclari = []
        if commons_sonuclari:
            yeni = _commons_indir(commons_sonuclari, kalan, assets_dizin)
            if yeni:
                toplanan.extend(yeni)
                if "commons" not in kullanilan_kaynaklar:
                    kullanilan_kaynaklar.append("commons")
                kullanilanlar = {g["dosya"] for g in yeni}
                kalan = [d for d in kalan if d not in kullanilanlar]

        # Openverse
        if kalan:
            time.sleep(1)
            try:
                openverse_sonuclari = openverse.resim_ara(arama_sorgusu, adet=len(kalan))
            except Exception:
                openverse_sonuclari = []
            if openverse_sonuclari:
                yeni = _openverse_indir(openverse_sonuclari, kalan, assets_dizin)
                if yeni:
                    toplanan.extend(yeni)
                    if "openverse" not in kullanilan_kaynaklar:
                        kullanilan_kaynaklar.append("openverse")
                    kullanilanlar = {g["dosya"] for g in yeni}
                    kalan = [d for d in kalan if d not in kullanilanlar]

        # Pexels
        if kalan:
            time.sleep(1)
            try:
                pexels_sonuclari = pexels.fotograf_ara(arama_sorgusu, adet=len(kalan))
            except Exception:
                pexels_sonuclari = []
            if pexels_sonuclari:
                yeni = _pexels_indir(pexels_sonuclari, kalan, assets_dizin)
                if yeni:
                    toplanan.extend(yeni)
                    if "pexels" not in kullanilan_kaynaklar:
                        kullanilan_kaynaklar.append("pexels")
                    kullanilanlar = {g["dosya"] for g in yeni}
                    kalan = [d for d in kalan if d not in kullanilanlar]

    if not toplanan:
        return {"kaynak": None, "gorseller": []}

    return {"kaynak": "+".join(kullanilan_kaynaklar), "gorseller": toplanan}
