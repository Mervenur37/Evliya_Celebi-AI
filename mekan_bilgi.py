"""Seyahat Defteri için kısa, değişmeyen mekân planlama bilgileri."""

MEKANLAR = {
    "istanbul": ("İstanbul", "sehir", "1-3 gün"),
    "kapadokya": ("Nevşehir", "doga-tarih", "2-3 gün"),
    "safranbolu": ("Karabük", "tarih", "1 gün"),
    "gaziantep": ("Gaziantep", "gastronomi", "1-2 gün"),
    "hatay": ("Hatay", "gastronomi-tarih", "1-2 gün"),
    "gobeklitepe": ("Şanlıurfa", "orenyeri", "2-3 saat"),
    "hattusa": ("Çorum", "orenyeri", "3-4 saat"),
    "ani": ("Kars", "orenyeri", "3-4 saat"),
    "amasya": ("Amasya", "sehir-tarih", "1 gün"),
    "datca": ("Muğla", "deniz-sakin", "1-2 gün"),
    "assos": ("Çanakkale", "orenyeri-deniz", "3-5 saat"),
    "egirdir": ("Isparta", "gol-doga", "1 gün"),
    "kackar": ("Rize-Artvin", "doga-macera", "2-4 gün"),
    "antalya": ("Antalya", "sehir-deniz", "1-3 gün"),
    "pamukkale": ("Denizli", "doga-orenyeri", "4-6 saat"),
    "bursa": ("Bursa", "sehir-tarih", "1-2 gün"),
    "kayseri": ("Kayseri", "sehir-gastronomi", "1 gün"),
    "akyaka": ("Muğla", "deniz-sakin", "1 gün"),
    "sagalassos": ("Burdur", "orenyeri", "3-4 saat"),
    "mardin": ("Mardin", "sehir-tarih", "1-2 gün"),
    "ankara": ("Ankara", "sehir-tarih", "1-2 gün"),
    "eymir": ("Ankara", "gol-doga", "2-4 saat"),
    "beypazari": ("Ankara", "tarih-gastronomi", "1 gün"),
    "edirne": ("Edirne", "sehir-tarih", "1 gün"),
    "balat": ("İstanbul", "semt-tarih", "2-3 saat"),
    "avanos": ("Nevşehir", "sanat-deneyim", "2-4 saat"),
    "goreme": ("Nevşehir", "orenyeri", "4-6 saat"),
    "hamamonu": ("Ankara", "semt-tarih", "2-3 saat"),
    "gordion": ("Ankara", "orenyeri", "2-3 saat"),
    "alanya": ("Antalya", "deniz-tarih", "1 gün"),
    "side": ("Antalya", "orenyeri-deniz", "3-5 saat"),
    "kars": ("Kars", "sehir-tarih", "1-2 gün"),
    "konya": ("Konya", "sehir-kultur", "1-2 gün"),
    "ayder": ("Rize", "doga", "1 gün"),
    "ayvalik": ("Balıkesir", "deniz-gastronomi", "1-2 gün"),
    "cunda": ("Balıkesir", "ada-gastronomi", "1 gün"),
    "foca": ("İzmir", "deniz-sakin", "1 gün"),
    "izmir": ("İzmir", "sehir-deniz", "1-2 gün"),
    "adana": ("Adana", "sehir-gastronomi", "1 gün"),
    "sanliurfa": ("Şanlıurfa", "sehir-tarih", "1-2 gün"),
    "diyarbakir": ("Diyarbakır", "sehir-tarih", "1-2 gün"),
    "diyarbakır": ("Diyarbakır", "sehir-tarih", "1-2 gün"),
    "kastamonu": ("Kastamonu", "sehir-tarih", "1 gün"),
}


def detaylari_olustur(sluglar, temalar=None):
    """Slug listesini arayüzün kullanacağı güvenli planlama kayıtlarına çevirir."""
    varsayilan_kategori = next(iter(temalar or []), "kesif")
    sonuc = []
    for slug in dict.fromkeys(sluglar or []):
        if not slug:
            continue
        sehir, kategori, sure = MEKANLAR.get(
            slug, (slug.replace("-", " ").title(), varsayilan_kategori, "2-4 saat")
        )
        sonuc.append({
            "slug": slug,
            "sehir": sehir,
            "kategori": kategori,
            "ziyaret_suresi": sure,
            "guncel_bilgi": False,
        })
    return sonuc
