"""Mekânların değişken olmayan 'Gitmeden Önce' rehber bilgilerini üretir.

Saat, ücret ve bilet uygunluğu gibi hızla değişen alanlar kesin değer olarak
saklanmaz; kullanıcı her zaman resmî kaynağa yönlendirilir.
"""

KONTROL_TARIHI = "2026-08-29"

SEHIR_KAYNAKLARI = {
    "İstanbul": ("İstanbul İl Kültür ve Turizm Müdürlüğü", "https://istanbul.ktb.gov.tr/"),
    "Ankara": ("Ankara İl Kültür ve Turizm Müdürlüğü", "https://ankara.ktb.gov.tr/"),
    "Kapadokya": ("T.C. Kültür ve Turizm Bakanlığı", "https://www.ktb.gov.tr/"),
    "Antalya": ("Antalya İl Kültür ve Turizm Müdürlüğü", "https://antalya.ktb.gov.tr/"),
    "Gaziantep": ("T.C. Kültür ve Turizm Bakanlığı", "https://www.ktb.gov.tr/"),
}

MUZE_VE_ORENYERI = {
    "topkapi-sarayi", "istanbul-arkeoloji-muzeleri", "anadolu-medeniyetleri-muzesi",
    "goreme-acik-hava-muzesi", "kaymakli-yeralti-sehri", "antalya-muzesi",
    "zeugma-mozaik-muzesi", "emines-gogus-mutfak-muzesi",
}

OZEL_KAYNAKLAR = {
    "anitkabir": ("Anıtkabir Komutanlığı", "https://www.anitkabir.tsk.tr/"),
}


def _alan_tipi(tur):
    tur = tur.casefold()
    if any(x in tur for x in ("müze", "yeraltı", "cami", "çarşı", "bedesten")):
        return "Çoğunlukla kapalı / korunaklı"
    if any(x in tur for x in ("park", "sahil", "şelale", "göl", "manzara", "peri bacaları")):
        return "Açık hava"
    return "Açık ve kapalı alanlar birlikte"


def _adab(slug, tur):
    kucuk = tur.casefold()
    if "cami" in kucuk:
        return "İbadet saatlerine saygı göster; sessiz ol ve kıyafet kurallarını girişte kontrol et."
    if slug == "kaymakli-yeralti-sehri":
        return "Dar ve alçak geçitlerde acele etme; kapalı alan hassasiyetin varsa önceden değerlendir."
    if any(x in kucuk for x in ("park", "sahil", "göl", "şelale")):
        return "Doğal alanı temiz bırak; işaretli güzergâhlardan ayrılma."
    if any(x in kucuk for x in ("çarşı", "bedesten")):
        return "Fotoğraf çekmeden önce esnaftan izin istemek zarif bir davranıştır."
    return "Eserlere dokunma; fotoğraf ve çanta kurallarını mekân girişinde kontrol et."


def bilgi_olustur(slug, durak, sehir):
    tur = str(durak.get("tur") or "turistik yer")
    kaynak = OZEL_KAYNAKLAR.get(slug)
    if not kaynak and slug in MUZE_VE_ORENYERI:
        kaynak = ("T.C. Kültür ve Turizm Bakanlığı – Müze ve Örenyerleri", "https://muze.gov.tr/")
    kaynak = kaynak or SEHIR_KAYNAKLARI.get(sehir) or ("T.C. Kültür ve Turizm Bakanlığı", "https://www.ktb.gov.tr/")
    acik_hava = _alan_tipi(tur) == "Açık hava"
    return {
        "alan_tipi": _alan_tipi(tur),
        "en_uygun_zaman": "Aşırı sıcak ve yoğunluğu azaltmak için sabah saatlerini değerlendirebilirsin." if acik_hava else "Yoğunluğu azaltmak için günün erken saatlerini değerlendirebilirsin.",
        "cocuklar": "Genellikle uygun; yürüyüş mesafesi ve dinlenme ihtiyacını hesaba kat." if acik_hava else "Genellikle uygun; mekânın yaş ve güvenlik kurallarını kontrol et.",
        "erisilebilirlik": "Giriş, asansör, rampa ve erişilebilir tuvalet durumunu resmî kaynaktan doğrula.",
        "rezervasyon": "Güncel bilet, rezervasyon, çalışma saati ve kapanış gününü resmî kaynaktan kontrol et.",
        "adab": _adab(slug, tur),
        "resmi_kaynak": {"ad": kaynak[0], "url": kaynak[1]},
        "dogrulama": "genel-rehber",
        "son_kontrol": KONTROL_TARIHI,
        "guncel_bilgi_notu": "Saat, ücret ve erişim koşulları değişebilir; bu kart güncel operasyon bilgisi garantisi vermez.",
    }
