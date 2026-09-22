"""GoTürkiye deneyim başlıkları ve çoklu il eşleşmelerinin editoryal deposu.

Excel'in kendisi değiştirilmez. Ondan çıkarılan deneyim kataloğu başlangıçta
SQLite'a eklenir; öneri/onay/red kararları daha sonra admin panelinden kalıcı
olarak yönetilir.
"""

import datetime as dt
import json
import os
import re
import sqlite3
import unicodedata


TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
DB_YOLU = os.path.join(TEMEL_DIZIN, "evliya.db")
KATALOG_YOLU = os.path.join(TEMEL_DIZIN, "deneyimler.json")

ILLER = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya",
    "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik",
    "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum",
    "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir",
    "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul",
    "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis",
    "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa",
    "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize",
    "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ",
    "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak",
]


def baglan():
    db = sqlite3.connect(DB_YOLU, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def slug_olustur(metin):
    ceviri = str.maketrans({"ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c"})
    sade = unicodedata.normalize("NFKD", str(metin or "").translate(ceviri)).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", sade).strip("-")


def kur_ve_aktar():
    with baglan() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS deneyimler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kaynak_no INTEGER UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                ad_en TEXT NOT NULL,
                ad_tr TEXT NOT NULL,
                temalar TEXT NOT NULL DEFAULT '[]',
                kaynak_dosya TEXT NOT NULL,
                aktif INTEGER NOT NULL DEFAULT 1,
                guncelleme_tarihi TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS deneyim_il_eslesmeleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deneyim_id INTEGER NOT NULL REFERENCES deneyimler(id) ON DELETE CASCADE,
                il TEXT NOT NULL,
                durum TEXT NOT NULL DEFAULT 'oneri' CHECK(durum IN ('oneri','onayli','reddedildi')),
                guven REAL NOT NULL DEFAULT 0.5,
                kaynak_adi TEXT,
                kaynak_url TEXT,
                gerekce TEXT,
                guncelleme_tarihi TEXT NOT NULL,
                UNIQUE(deneyim_id, il)
            );
            CREATE INDEX IF NOT EXISTS idx_deneyim_eslesme_durum ON deneyim_il_eslesmeleri(durum);
            CREATE INDEX IF NOT EXISTS idx_deneyim_eslesme_il ON deneyim_il_eslesmeleri(il);
        """)

        # Özel kaynak listesi depoya eklenmez. Yeni kurulumda tablolar boş
        # açılır; yerel katalog eklendiğinde yeniden başlatmak yeterlidir.
        if not os.path.exists(KATALOG_YOLU):
            return
        with open(KATALOG_YOLU, "r", encoding="utf-8") as dosya:
            katalog = json.load(dosya)
        simdi = dt.datetime.now(dt.timezone.utc).isoformat()
        for kayit in katalog:
            slug = slug_olustur(kayit["ad_en"])
            db.execute("""
                INSERT INTO deneyimler (kaynak_no,slug,ad_en,ad_tr,temalar,kaynak_dosya,guncelleme_tarihi)
                VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(kaynak_no) DO UPDATE SET
                    slug=excluded.slug, ad_en=excluded.ad_en, ad_tr=excluded.ad_tr,
                    temalar=excluded.temalar, guncelleme_tarihi=excluded.guncelleme_tarihi
            """, (
                kayit["no"], slug, kayit["ad_en"], kayit["ad_tr"],
                json.dumps(kayit.get("temalar", []), ensure_ascii=False),
                "Goturkiye_Experiences_list.xlsx", simdi,
            ))
            deneyim_id = db.execute("SELECT id FROM deneyimler WHERE kaynak_no=?", (kayit["no"],)).fetchone()[0]
            for il in kayit.get("iller", []):
                if il not in ILLER:
                    continue
                db.execute("""
                    INSERT INTO deneyim_il_eslesmeleri
                        (deneyim_id,il,durum,guven,kaynak_adi,gerekce,guncelleme_tarihi)
                    VALUES (?,?, 'oneri', ?, ?, ?, ?)
                    ON CONFLICT(deneyim_id,il) DO NOTHING
                """, (
                    deneyim_id, il, float(kayit.get("guven", 0.5)),
                    "Editoryal başlangıç önerisi",
                    "Uygunluk adayıdır; admin onayı ve kaynak doğrulaması bekler.", simdi,
                ))


def admin_ozeti():
    with baglan() as db:
        toplam = db.execute("SELECT COUNT(*) FROM deneyimler WHERE aktif=1").fetchone()[0]
        satirlar = db.execute("SELECT durum, COUNT(*) adet FROM deneyim_il_eslesmeleri GROUP BY durum").fetchall()
        coklu = db.execute("""
            SELECT COUNT(*) FROM (
                SELECT deneyim_id FROM deneyim_il_eslesmeleri
                WHERE durum != 'reddedildi' GROUP BY deneyim_id HAVING COUNT(*) > 1
            )
        """).fetchone()[0]
    durumlar = {satir["durum"]: satir["adet"] for satir in satirlar}
    return {
        "toplam_deneyim": toplam,
        "onerilen_eslesme": durumlar.get("oneri", 0),
        "onayli_eslesme": durumlar.get("onayli", 0),
        "reddedilen_eslesme": durumlar.get("reddedildi", 0),
        "coklu_il_deneyimi": coklu,
    }


def deneyimleri_getir(arama="", durum="tum"):
    arama = str(arama or "").strip().casefold()
    durum = durum if durum in ("tum", "oneri", "onayli", "reddedildi") else "tum"
    with baglan() as db:
        deneyimler = db.execute("SELECT * FROM deneyimler WHERE aktif=1 ORDER BY kaynak_no").fetchall()
        eslesmeler = db.execute("""
            SELECT e.*, d.kaynak_no FROM deneyim_il_eslesmeleri e
            JOIN deneyimler d ON d.id=e.deneyim_id
            ORDER BY e.guven DESC, e.il
        """).fetchall()
    eslesme_haritasi = {}
    for satir in eslesmeler:
        eslesme_haritasi.setdefault(satir["deneyim_id"], []).append(dict(satir))
    sonuc = []
    for satir in deneyimler:
        if arama and arama not in satir["ad_tr"].casefold() and arama not in satir["ad_en"].casefold():
            continue
        adaylar = eslesme_haritasi.get(satir["id"], [])
        if durum != "tum" and not any(x["durum"] == durum for x in adaylar):
            continue
        sonuc.append({
            "id": satir["id"], "no": satir["kaynak_no"], "slug": satir["slug"],
            "ad_en": satir["ad_en"], "ad_tr": satir["ad_tr"],
            "temalar": json.loads(satir["temalar"] or "[]"), "iller": adaylar,
            "sayilar": {
                "oneri": sum(x["durum"] == "oneri" for x in adaylar),
                "onayli": sum(x["durum"] == "onayli" for x in adaylar),
                "reddedildi": sum(x["durum"] == "reddedildi" for x in adaylar),
            },
        })
    return sonuc


def il_durumunu_guncelle(deneyim_id, il, durum):
    if il not in ILLER or durum not in ("oneri", "onayli", "reddedildi"):
        return False
    simdi = dt.datetime.now(dt.timezone.utc).isoformat()
    with baglan() as db:
        var_mi = db.execute("SELECT 1 FROM deneyimler WHERE id=? AND aktif=1", (int(deneyim_id),)).fetchone()
        if not var_mi:
            return False
        db.execute("""
            INSERT INTO deneyim_il_eslesmeleri
                (deneyim_id,il,durum,guven,kaynak_adi,gerekce,guncelleme_tarihi)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(deneyim_id,il) DO UPDATE SET
                durum=excluded.durum, kaynak_adi=excluded.kaynak_adi,
                gerekce=excluded.gerekce, guncelleme_tarihi=excluded.guncelleme_tarihi
        """, (
            int(deneyim_id), il, durum, 1.0 if durum == "onayli" else 0.5,
            "Yönetici kararı", "Admin panelinden güncellendi.", simdi,
        ))
    return True


def yuksek_guvenlileri_onayla(esik=0.85):
    esik = max(0.5, min(float(esik), 1.0))
    with baglan() as db:
        sonuc = db.execute("""
            UPDATE deneyim_il_eslesmeleri
            SET durum='onayli', kaynak_adi='Yönetici toplu onayı',
                gerekce='Yüksek güvenli başlangıç önerisi admin tarafından onaylandı.',
                guncelleme_tarihi=?
            WHERE durum='oneri' AND guven>=?
        """, (dt.datetime.now(dt.timezone.utc).isoformat(), esik))
    return sonuc.rowcount


kur_ve_aktar()
