"""Evliya'nın izinli ve anonim kültürel merak sinyalleri.

Ham mesaj, IP, ad veya kesin konum saklanmaz. Yalnızca katalogdaki konu slug'ı,
dil, isteğe bağlı ülke, genel kategori ve oturum başına rastgele kimlik tutulur.
"""

import datetime as dt
import json
import os
import re
import sqlite3

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
DB_YOLU = os.path.join(TEMEL_DIZIN, "evliya.db")
MERAK_KATALOG_YOLU = os.path.join(TEMEL_DIZIN, "meraklar.json")


def baglan():
    baglanti = sqlite3.connect(DB_YOLU, timeout=5)
    baglanti.row_factory = sqlite3.Row
    return baglanti


def kur():
    with baglan() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS merak_kayitlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                oturum_id TEXT NOT NULL,
                dil TEXT NOT NULL,
                ulke TEXT,
                kategori TEXT NOT NULL,
                konu TEXT NOT NULL,
                yararli INTEGER,
                olusturma_tarihi TEXT NOT NULL
            )
        """)
        db.execute("CREATE INDEX IF NOT EXISTS idx_merak_dil_konu ON merak_kayitlari(dil, konu)")


def katalog_yukle():
    with open(MERAK_KATALOG_YOLU, "r", encoding="utf-8") as dosya:
        return json.load(dosya)


def guvenli_kod(deger, azami=40):
    deger = str(deger or "")[:azami]
    return deger if re.fullmatch(r"[A-Za-z0-9_-]+", deger) else ""


def konu_bul(mesaj, dil="tr"):
    """Katalog sorularındaki belirgin sözcüklerle konu bulur; ham metni saklamaz."""
    metin = (mesaj or "").casefold()
    eslesmeler = {
        "cay-ikrami": ("çay", "tea", "tee", "お茶"),
        "cami-ziyareti": ("cami", "mosque", "moschee", "モスク"),
        "nazar-boncugu": ("nazar", "evil eye", "blaue auge", "ナザール"),
        "evde-ayakkabi": ("ayakkabı", "shoes", "schuhe", "靴"),
        "turk-kahvaltisi": ("kahvalt", "breakfast", "frühstück", "朝食"),
        "pazarlik": ("pazarlık", "bargain", "feilsch", "値段交渉"),
        "bahsis": ("bahşiş", "tip", "trinkgeld", "チップ"),
        "misafirperverlik": ("misafir", "hospitality", "gastfreund", "おもてなし"),
        "ramazanda-seyahat": ("ramazan", "ramadan", "ラマダン"),
        "yalniz-seyahat": ("yalnız", "solo", "allein", "一人旅"),
        "hamam-adabi": ("hamam", "turkish bath", "ハマム", "トルコ風呂"),
        "kahve-fali": ("kahve fal", "fortune", "kaffeesatz", "コーヒー占い"),
        "sokak-kedileri": ("sokak kedi", "street cat", "straßenkat", "野良猫"),
        "abi-abla-hitabi": ("abi", "abla", "older brother", "older sister", "bruder", "schwester", "アビ", "アブラ"),
        "dolmus-kullanimi": ("dolmuş", "dolmus", "ドルムシュ"),
        "kolonya-ikrami": ("kolonya", "cologne", "kolonya", "コロンヤ"),
        "yolcuya-su-dokmek": ("arkasından su", "pour water", "wasser nach", "水をまく"),
        "kilim-desenleri": ("kilim", "rug motif", "teppichmuster", "キリム"),
        "meze-sofrasi": ("meze", "メゼ"),
        "dugun-gelenekleri": ("düğün", "wedding", "hochzeit", "結婚式"),
        "tavla-kulturu": ("tavla", "backgammon", "バックギャモン"),
        "kahvenin-yaninda-su": ("kahvenin yanında su", "water with coffee", "wasser zum kaffee", "コーヒーに水"),
    }
    for slug, kelimeler in eslesmeler.items():
        if any(kelime in metin for kelime in kelimeler):
            return slug
    return None


def sinyal_kaydet(oturum_id, dil, ulke, konu):
    katalog = {kayit["slug"]: kayit for kayit in katalog_yukle()}
    if konu not in katalog:
        return False
    oturum_id = guvenli_kod(oturum_id, 80)
    if not oturum_id:
        return False
    dil = dil if dil in ("tr", "en", "de", "ja") else "en"
    ulke = guvenli_kod(ulke, 2).upper() or None
    with baglan() as db:
        db.execute(
            "INSERT INTO merak_kayitlari (oturum_id,dil,ulke,kategori,konu,olusturma_tarihi) VALUES (?,?,?,?,?,?)",
            (oturum_id, dil, ulke, katalog[konu]["kategori"], konu, dt.datetime.now(dt.timezone.utc).isoformat()),
        )
    return True


def geri_bildirim_kaydet(oturum_id, konu, yararli):
    oturum_id = guvenli_kod(oturum_id, 80)
    konu = guvenli_kod(konu, 60)
    if not oturum_id or not konu or not isinstance(yararli, bool):
        return False
    with baglan() as db:
        sonuc = db.execute(
            "UPDATE merak_kayitlari SET yararli=? WHERE id=(SELECT id FROM merak_kayitlari WHERE oturum_id=? AND konu=? ORDER BY id DESC LIMIT 1)",
            (int(yararli), oturum_id, konu),
        )
    return sonuc.rowcount > 0


def onerileri_getir(dil="tr", temalar=None, yerler=None, limit=9):
    dil = dil if dil in ("tr", "en", "de", "ja") else "en"
    temalar, yerler = set(temalar or []), set(yerler or [])
    katalog = katalog_yukle()
    tarih = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).isoformat()
    with baglan() as db:
        satirlar = db.execute(
            "SELECT konu, COUNT(*) adet, AVG(CASE WHEN yararli IS NULL THEN 0.5 ELSE yararli END) fayda FROM merak_kayitlari WHERE dil=? AND olusturma_tarihi>=? GROUP BY konu",
            (dil, tarih),
        ).fetchall()
    egilim = {s["konu"]: (s["adet"], s["fayda"]) for s in satirlar}

    def puan(kayit):
        adet, fayda = egilim.get(kayit["slug"], (0, 0.5))
        return len(temalar & set(kayit.get("temalar", []))) * 4 + len(yerler & set(kayit.get("yerler", []))) * 6 + min(adet, 20) + fayda

    sonuc = []
    for kayit in sorted(katalog, key=puan, reverse=True)[:max(1, min(int(limit), 18))]:
        adet = egilim.get(kayit["slug"], (0, 0.5))[0]
        neden = "ilgi-alanina-gore" if temalar & set(kayit.get("temalar", [])) else "kesfet"
        if adet >= 20:
            neden = "dilinde-sik-soruluyor"
        sonuc.append({
            "slug": kayit["slug"], "ikon": kayit["ikon"], "kategori": kayit["kategori"],
            "soru": kayit["sorular"].get(dil) or kayit["sorular"]["en"], "neden": neden,
        })
    return sonuc


def admin_ozeti_getir():
    """Kimlik içermeyen toplu admin istatistiklerini döndürür."""
    simdi = dt.datetime.now(dt.timezone.utc)
    yedi_gun = (simdi - dt.timedelta(days=7)).isoformat()
    otuz_gun = (simdi - dt.timedelta(days=30)).isoformat()
    katalog = {kayit["slug"]: kayit for kayit in katalog_yukle()}

    with baglan() as db:
        toplam = db.execute("SELECT COUNT(*) FROM merak_kayitlari").fetchone()[0]
        oturum = db.execute("SELECT COUNT(DISTINCT oturum_id) FROM merak_kayitlari").fetchone()[0]
        son7 = db.execute("SELECT COUNT(*) FROM merak_kayitlari WHERE olusturma_tarihi>=?", (yedi_gun,)).fetchone()[0]
        son30 = db.execute("SELECT COUNT(*) FROM merak_kayitlari WHERE olusturma_tarihi>=?", (otuz_gun,)).fetchone()[0]
        geri = db.execute("SELECT COUNT(*) adet, AVG(yararli) oran FROM merak_kayitlari WHERE yararli IS NOT NULL").fetchone()
        diller = db.execute("SELECT dil etiket, COUNT(*) adet FROM merak_kayitlari GROUP BY dil ORDER BY adet DESC").fetchall()
        ulkeler = db.execute("SELECT ulke etiket, COUNT(*) adet FROM merak_kayitlari WHERE ulke IS NOT NULL GROUP BY ulke ORDER BY adet DESC").fetchall()
        konular = db.execute("SELECT konu etiket, COUNT(*) adet, AVG(yararli) fayda FROM merak_kayitlari GROUP BY konu ORDER BY adet DESC LIMIT 10").fetchall()
        gunler = db.execute("SELECT substr(olusturma_tarihi,1,10) gun, COUNT(*) adet FROM merak_kayitlari WHERE olusturma_tarihi>=? GROUP BY gun ORDER BY gun", (otuz_gun,)).fetchall()

    def liste(satirlar):
        return [{"etiket": s["etiket"], "adet": s["adet"]} for s in satirlar]

    # Çok küçük ülke gruplarını göstermemek anonimlik açısından daha güvenli.
    ulke_listesi = [x for x in liste(ulkeler) if x["adet"] >= 5]
    konu_listesi = []
    for satir in konular:
        kayit = katalog.get(satir["etiket"], {})
        konu_listesi.append({
            "slug": satir["etiket"],
            "baslik": (kayit.get("sorular") or {}).get("tr", satir["etiket"]),
            "ikon": kayit.get("ikon", "✦"),
            "adet": satir["adet"],
            "fayda": round(float(satir["fayda"]) * 100) if satir["fayda"] is not None else None,
        })

    gun_sozlugu = {s["gun"]: s["adet"] for s in gunler}
    gunluk = []
    for fark in range(29, -1, -1):
        gun = (simdi - dt.timedelta(days=fark)).date().isoformat()
        gunluk.append({"gun": gun, "adet": gun_sozlugu.get(gun, 0)})

    return {
        "kartlar": {
            "toplam_merak": toplam, "izinli_oturum": oturum,
            "son_7_gun": son7, "son_30_gun": son30,
            "geri_bildirim": geri["adet"],
            "yararli_orani": round(float(geri["oran"]) * 100) if geri["oran"] is not None else None,
        },
        "diller": liste(diller), "ulkeler": ulke_listesi,
        "konular": konu_listesi, "gunluk": gunluk,
        "gizlilik_notu": "Ülke dağılımında 5'ten az kaydı olan gruplar gizlenir.",
        "uretildi": simdi.isoformat(),
    }


kur()
