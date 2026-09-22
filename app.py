# -*- coding: utf-8 -*-
"""
Evliya Çelebi AI — Flask backend.

SISTEM_PROMPTU ve llm_cevapla mantığı evliya_test.py'deki test edilmiş (v4,
prompt v0.3) haliyle olduğu gibi taşındı: model yedekleme zinciri, 429/503/404
davranışları, JSON parse ve panel varsayılanları değişmedi.
"""

import json
import hmac
import os
import re
import secrets
import sys
import threading
import time
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from google import genai

import commons
import deneyim_db
import konum
import kultur_bilgi
import mekan_bilgi
import mekan_anlat
import gunluk_plan
import mekan_rehber
import merak_db
import yakinimda

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

TEMEL_DIZIN = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIZIN = os.path.join(TEMEL_DIZIN, "assets")
ASSETS_KATALOG_YOLU = os.path.join(TEMEL_DIZIN, "assets.json")

# Dinamik görsel tamamlama: canlı Commons araması 2 sn'yi geçmesin; indirme
# hep arka plan thread'inde biter (sonraki cevapta görsel hazır olur).
CANLI_ARAMA_BUDCESI_SN = 2.0
canli_arama_isleniyor = set()
canli_arama_kilidi = threading.Lock()
katalog_yazma_kilidi = threading.Lock()

API_ANAHTARI = os.environ.get("GEMINI_API_KEY")
ADMIN_PAROLASI = os.environ.get("ADMIN_PASSWORD")

MODELLER = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
]

SISTEM_PROMPTU = """EN ÖNEMLİ KURAL — CEVAP DİLİ:
"reply" alanının dili HER ZAMAN konuğun son mesajının dilidir. İngilizce mesaja İngilizce, Almanca mesaja Almanca, Japonca mesaja Japonca. Türkçe reply YALNIZCA konuk Türkçe yazarsa olur.
Türkçe serpiştirme sınırı: yabancı dildeki reply içinde Türkçe olarak yalnızca selam/nezaket sözleri (merhaba, hoş geldin, buyrun, afiyet olsun) ve yer/yemek adları geçebilir. Türkçe kelimeleri yabancı cümlenin dilbilgisine karıştırma.

PANEL DİL KURALI (reply kuralının tersi!):
"panel" içindeki BÜTÜN değerler, reply hangi dilde olursa olsun, HER ZAMAN aşağıdaki sabit sözlükten yazılır:
- temalar yalnızca şunlardan seçilir: tarih, doga, yemek, deniz, sanat, sakin, macera, aile (en fazla 3)
- duygu yalnızca şunlardan: nostaljik, neseli, huzurlu, mistik
- medya yalnızca şunlardan: foto, video, harita
- yerler ve rota: yalnızca GERÇEK yer adları, küçük harf ve Türkçe karaktersiz slug olarak (istanbul, kapadokya, safranbolu). Gerçek bir yer geçmiyorsa boş liste bırak; 'cities', 'nature' gibi genel kelimeler YAZMA.

Sen Evliya Çelebi'sin: 17. yüzyılın büyük Osmanlı gezgini, Seyahatname'nin yazarı. Dört yüz yıl sonra bugüne döndün ve şimdi Türkiye'nin sanal elçisisin. Görevin, dünyanın dört bir yanından gelen konuklara Türkiye'yi tanıtmak, ilgilerine göre yerler ve rotalar önermek.

KİMLİK VE ÜSLUP:
- Hikâye anlatıcısısın; kuru bilgi yerine koku, ses, küçük anekdot kullanırsın. Yeri geldiğinde "Ben oradan geçerken..." diye Seyahatname ruhuna uygun kısa anılar katarsın.
- Sıcak, misafirperver, hafifçe eski zamandan gelen ama daima anlaşılır bir dilin var. Nadiren ve tadında mübalağa yaparsın; coğrafi ve tarihi bilgide asla uydurmazsın.
- UZUNLUK: reply en fazla ~90 kelime; gerekirse ek olarak en fazla 3 maddelik kısa liste. Markdown biçimlendirme (yıldızlı kalın yazı vb.) kullanma; düz metin yaz.
- Her cevaba aynı selam kalıbıyla başlama; çeşitlendir veya doğrudan konuya gir.
- Aynı imgeyi (kervan, deve vb.) üst üste iki cevapta kullanma.
- Her cevabın sonunda konuğu tanımaya yarayan en fazla bir soru sorabilirsin.

GÖREV:
- Konuğun ilgisini keşfet ve önerini kişiselleştir. Bilinen yerlerin yanına daima az bilinen bir hazine ekle (Safranbolu, Göbeklitepe, Eğirdir, Midyat, Ayvalık, Ani, Hattuşa...).
- İstenirse rota kur: günlerin anlatımı reply metninde olur; panel.rota alanına ise yalnızca yer slug'ları yazılır ve medya "harita" yapılır.
- Mutfağı, el sanatlarını, müziği de tanıtımın parçası yap.

LEZZET VE DENEYİM:
Bir yer önerirken mümkünse o yörenin MUTLAKA tadılması gereken bir yemeğini/içeceğini ve bir yerel deneyimini (el sanatı, çarşı, ritüel, festival) somut biçimde öner. Örnek ton: "Gaziantep'e varırsan beyran çorbasını sabah aç karnına tat; bakırcılar çarşısında ustaların sesini dinle." Yemek/deneyim adı uydurma; emin değilsen o yörenin genel mutfağından söz et.

SINIRLAR:
- Siyaset ve güncel tartışmalara girme; zarifçe seyahate döndür ("Ben gezginim, kavgaların değil kervanların adamıyım...").
- Hiçbir ülkeyi ve kültürü kötüleme.
- Vize, fiyat, sefer saati gibi güncel bilgilerde tahmin yürütme; goturkiye.com ve resmî kaynaklara yönlendir.
- Konuktan kişisel veri isteme. Emin olmadığın bilgiyi mübalağayla örtme; bilmediğini söyle.

ÇIKTI: yalnızca şu JSON:
{
  "reply": "konuğun dilinde cevabın",
  "panel": {
    "yerler": [],
    "temalar": [],
    "rota": [],
    "duygu": "nostaljik",
    "medya": "foto",
    "dil": "en",
    "lezzetler": [],
    "deneyimler": [],
    "kultur": null
  }
}
EK ALAN: panel.dil, "reply" alanının yazıldığı dildir; yalnızca şu kodlardan biri olur: en, de, ja, tr.
EK ALANLAR: panel.lezzetler ve panel.deneyimler, reply içinde somut olarak önerilen yöresel yiyecek/içecek ve yerel deneyim adlarıdır; yerler ile aynı slug kuralına tabidir (küçük harf, Türkçe karaktersiz — ör. beyran, kunefe, menengic / bakircilar-carsisi, cini-atolyesi). Emin değilsen boş liste bırak, uydurma.
EK ALAN: panel.kultur, yalnızca konuk Türk kültürü/gelenekleri/adab-ı muaşeret hakkında soru sorduğunda (ör. çay kültürü, eve girerken ayakkabı çıkarma, nazar boncuğu, cami ziyareti, pazarlık, kahvaltı geleneği gibi) doldurulur; başka her durumda null bırakılır. Doluysa şu üç alanlı nesnedir: {"hikaye": "Evliya'nın birinci ağızdan kısa bir anlatım/anekdotu (1-2 cümle)", "kulturel_not": "Kısa ve doğru bir kültürel bilgi (1-2 cümle)", "adab": "Turistin saygıyla nasıl davranması gerektiğine dair somut bir öneri (1-2 cümle)"}. Güncel veya emin olmadığın hassas bilgide uydurma; genel ve saygılı bir dille konuş, hiçbir inancı/geleneği küçümseme. panel.kultur doluyken panel.yerler listesine konuyu temsil eden somut bir görsel anahtar kelimesi de ekle (ör. cami, cay, kahvalti, pazarlik, nazar-boncugu, misafirlik); bu anahtar kelime gerçek bir şehir olmak zorunda değildir, yalnızca ilgili görselin bulunmasını sağlar."""

# Kullanıcının asla görmemesi gereken teknik hatalar yerine dönülen,
# karakter içinden zarif bir cevap (LLM boş/hatalı döndüğünde veya günlük
# kota dolduğunda kullanılır). Teknik ayrıntı yalnızca terminal logunda kalır.
YOGUNLUK_CEVABI = "Kervanım bugün epey yol aldı, biraz soluklanmam gerek dostum. Az sonra tekrar sor."

client = genai.Client(api_key=API_ANAHTARI)
calisan_model = None


def simdi() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(etiket: str, mesaj: str) -> None:
    print(f"[{simdi()}] {etiket}: {mesaj}", flush=True)


def tek_istek(model_adi: str, contents, ek_baglam: str = None) -> str:
    sistem_talimati = SISTEM_PROMPTU + (f"\n\n{ek_baglam}" if ek_baglam else "")
    yanit = client.models.generate_content(
        model=model_adi,
        config={
            "system_instruction": sistem_talimati,
            "temperature": 0.8,
            "response_mime_type": "application/json",
        },
        contents=contents,
    )
    return yanit.text


def llm_cevapla(contents, ek_baglam: str = None) -> str:
    global calisan_model
    denenecekler = [calisan_model] + MODELLER if calisan_model else list(MODELLER)

    for model_adi in denenecekler:
        if model_adi is None:
            continue
        try:
            metin = tek_istek(model_adi, contents, ek_baglam)
            calisan_model = model_adi
            return metin
        except Exception as hata:
            mesaj = str(hata)
            if "429" in mesaj and "PerDay" in mesaj:
                # Günlük kota doldu: 35 sn beklemenin anlamı yok (kota dakikada
                # değil günde sıfırlanıyor), doğrudan sıradaki modele geç.
                log("GUNLUK KOTA", f"{model_adi} icin gunluk kota dolmus (PerDay), bekleme atlanip siradaki modele geciliyor. Detay: {mesaj}")
                continue
            if "429" in mesaj and "limit: 0" in mesaj:
                log("KOTA YOK", f"{model_adi} icin ucretsiz kota yok, siradaki modele geciliyor.")
                continue
            if "429" in mesaj:
                log("DAKIKALIK LIMIT", f"{model_adi}: 429, 35 sn beklenip tekrar denenecek.")
                time.sleep(35)
                try:
                    metin = tek_istek(model_adi, contents, ek_baglam)
                    calisan_model = model_adi
                    return metin
                except Exception as tekrar_hata:
                    log("TEKRAR BASARISIZ", f"{model_adi}: {tekrar_hata}")
                    continue
            if "503" in mesaj or "UNAVAILABLE" in mesaj:
                log("SUNUCU YOGUN", f"{model_adi}: 503, 20 sn beklenip tekrar denenecek.")
                time.sleep(20)
                try:
                    metin = tek_istek(model_adi, contents, ek_baglam)
                    calisan_model = model_adi
                    return metin
                except Exception as tekrar_hata:
                    log("TEKRAR BASARISIZ", f"{model_adi}: {tekrar_hata}")
                    continue
            if "404" in mesaj or "NOT_FOUND" in mesaj:
                log("MODEL YOK", f"{model_adi}: 404, siradaki modele geciliyor.")
                continue
            log("BEKLENMEYEN HATA", f"{model_adi}: {mesaj}")
            raise
    raise RuntimeError("Modellere ulaşılamadı (kota/yoğunluk). Birkaç dakika sonra tekrar dene.")


def json_ayikla(metin: str):
    """Önce doğrudan parse; olmazsa metnin içinden ilk { ile son } arasını çıkarır."""
    temiz = re.sub(r"```json|```", "", metin).strip()
    try:
        return json.loads(temiz), None
    except Exception:
        pass
    bas, son = temiz.find("{"), temiz.rfind("}")
    if bas != -1 and son > bas:
        try:
            return json.loads(temiz[bas:son + 1]), None
        except Exception as hata:
            return None, str(hata)
    return None, "JSON bloğu bulunamadı"


def panel_duzelt(panel):
    """Eksik alanlara güvenli varsayılanlar atar."""
    if not isinstance(panel, dict):
        panel = {}
    panel.setdefault("yerler", [])
    panel.setdefault("temalar", [])
    panel.setdefault("rota", [])
    panel.setdefault("duygu", "huzurlu")
    panel.setdefault("medya", "foto")
    panel.setdefault("dil", "en")
    panel.setdefault("lezzetler", [])
    panel.setdefault("deneyimler", [])
    panel.setdefault("kultur", None)
    for alan in ("yerler", "temalar", "rota", "lezzetler", "deneyimler"):
        if panel[alan] is None:
            panel[alan] = []
    if panel["kultur"] is not None and not isinstance(panel["kultur"], dict):
        panel["kultur"] = None
    return panel


# ---- Gezgin profili (oturum-içi, login/veritabanı YOK) ---------------------
# Profil hiçbir yerde saklanmaz: her istekte frontend'in gönderdiği `gecmis`
# içindeki her "evliya" turunun (frontend'in eklediği) temalar alanı sayılır.
# Böylece profil doğrudan konuşma geçmişiyle birlikte, yalnızca o oturum
# boyunca yaşar; yeni sohbette (gecmis=[]) otomatik sıfırlanır.

TEMA_KELIME_HAVUZU = ("tarih", "doga", "yemek", "deniz", "sanat", "sakin", "macera", "aile")

TEMA_SIFATLAR = {
    "tr": {
        "tarih": "kadim taşların fısıltısını", "doga": "doğanın sessiz güzelliğini",
        "yemek": "sofraların bereketini", "deniz": "denizin ferahlığını",
        "sanat": "el emeğinin inceliğini", "sakin": "sükûneti",
        "macera": "keşfin heyecanını", "aile": "birlikte geçirilen zamanı",
    },
    "en": {
        "tarih": "the whisper of ancient stones", "doga": "the quiet beauty of nature",
        "yemek": "the richness of a good table", "deniz": "the freshness of the sea",
        "sanat": "the artistry of skilled hands", "sakin": "tranquility",
        "macera": "the thrill of discovery", "aile": "time shared with loved ones",
    },
    "de": {
        "tarih": "das Flüstern uralter Steine", "doga": "die stille Schönheit der Natur",
        "yemek": "die Fülle einer guten Tafel", "deniz": "die Frische des Meeres",
        "sanat": "die Kunstfertigkeit geschickter Hände", "sakin": "die Ruhe",
        "macera": "den Nervenkitzel der Entdeckung", "aile": "gemeinsame Zeit mit den Liebsten",
    },
    "ja": {
        "tarih": "古い石々のささやき", "doga": "自然の静かな美しさ",
        "yemek": "食卓の豊かさ", "deniz": "海の清々しさ",
        "sanat": "職人技の妙", "sakin": "静けさ",
        "macera": "発見の興奮", "aile": "大切な人と過ごす時間",
    },
}

PROFIL_BAGLAC = {"tr": " ve ", "en": " and ", "de": " und ", "ja": "と"}

PROFIL_CUMLE_SABLONU = {
    "tr": lambda parca: f"Sen {parca} seven bir yolcusun.",
    "en": lambda parca: f"You are a traveler who loves {parca}.",
    "de": lambda parca: f"Du bist ein Reisender, der {parca} liebt.",
    "ja": lambda parca: f"あなたは{parca}を愛する旅人です。",
}

PROFIL_YETERSIZ_VERI_MESAJI = {
    "tr": "Evliya seni tanımaya başlıyor...",
    "en": "Evliya is just beginning to know you...",
    "de": "Evliya beginnt gerade, dich kennenzulernen...",
    "ja": "エヴリヤはあなたを知り始めたところです…",
}


def profil_hesapla(gecmis):
    """gecmis içindeki (frontend'in her evliya turuna eklediği) temalar
    listelerini sayarak {tema: puan} döner. Sunucuda hiçbir şey saklanmaz —
    profil her istekte, o isteğin gecmis'inden yeniden hesaplanır."""
    puanlar = {}
    if not isinstance(gecmis, list):
        return puanlar
    for tur in gecmis:
        if not isinstance(tur, dict):
            continue
        for tema in (tur.get("temalar") or []):
            if tema in TEMA_KELIME_HAVUZU:
                puanlar[tema] = puanlar.get(tema, 0) + 1
    return puanlar


def baglam_notu_olustur(puanlar):
    """LLM çağrısına eklenecek dinamik bağlam notu (SISTEM_PROMPTU sabitine
    dokunmaz, yalnızca bu istekte system_instruction'a eklenir)."""
    if not puanlar:
        return None
    siralanmis = sorted(puanlar.items(), key=lambda kv: (-kv[1], kv[0]))
    ust = [tema for tema, _ in siralanmis[:3]]
    return (
        f"BAĞLAM NOTU: Kullanıcının şu ana dek öne çıkan ilgileri: {', '.join(ust)}. "
        "Önerilerini mümkünse bu ilgilere doğru hafifçe yönlendir; ama konuğun güncel isteğini asla görmezden gelme."
    )


def profil_ozeti_olustur(puanlar, dil_kodu):
    """Panelde gösterilecek {"etiketler": [...], "aciklama": "..."} döner.
    Yeterli veri yoksa (toplam < 2 gözlem) sabit bir 'henüz tanımıyorum'
    mesajına düşer."""
    dil_kodu = dil_kodu if dil_kodu in TEMA_SIFATLAR else "en"

    if not puanlar or sum(puanlar.values()) < 2:
        return {"etiketler": [], "aciklama": PROFIL_YETERSIZ_VERI_MESAJI[dil_kodu]}

    siralanmis = sorted(puanlar.items(), key=lambda kv: (-kv[1], kv[0]))
    ust_etiketler = [tema for tema, _ in siralanmis[:3]]

    sifatlar = TEMA_SIFATLAR[dil_kodu]
    parcalar = [sifatlar.get(tema, tema) for tema in ust_etiketler[:2]]
    birlesik = PROFIL_BAGLAC.get(dil_kodu, " and ").join(parcalar)
    aciklama = PROFIL_CUMLE_SABLONU[dil_kodu](birlesik)

    return {"etiketler": ust_etiketler, "aciklama": aciklama}


def gecmisten_contents_olustur(mesaj: str, gecmis):
    """Konuşma geçmişini + yeni mesajı Gemini 'contents' listesine çevirir."""
    contents = []
    if isinstance(gecmis, list):
        for tur in gecmis:
            if not isinstance(tur, dict):
                continue
            rol_ham = tur.get("rol") or tur.get("role") or "user"
            icerik = tur.get("icerik") or tur.get("content") or ""
            if not icerik:
                continue
            rol = "model" if rol_ham in ("evliya", "model") else "user"
            contents.append({"role": rol, "parts": [{"text": icerik}]})
    contents.append({"role": "user", "parts": [{"text": mesaj}]})
    return contents


def katalog_yukle():
    if not os.path.exists(ASSETS_KATALOG_YOLU):
        def _kayit(dosya, yerler, temalar, genel=False):
            return {
                "yerler": yerler,
                "temalar": temalar,
                "genel": genel,
                "gorseller": [{"dosya": dosya, "lisans": "eklenecek", "fotografci": "bilinmiyor", "kaynak_url": ""}],
            }

        ornek_katalog = [
            _kayit("istanbul_1.svg", ["istanbul"], ["tarih", "sanat"]),
            _kayit("kapadokya_1.svg", ["kapadokya"], ["macera", "doga"]),
            _kayit("safranbolu_1.svg", ["safranbolu"], ["tarih", "sakin"]),
            _kayit("pamukkale_1.svg", ["pamukkale"], ["doga", "sakin"]),
            _kayit("antalya_1.svg", ["antalya"], ["deniz", "aile"]),
            _kayit("genel_1.svg", [], [], genel=True),
        ]
        with open(ASSETS_KATALOG_YOLU, "w", encoding="utf-8") as f:
            json.dump(ornek_katalog, f, ensure_ascii=False, indent=2)
        return ornek_katalog
    with open(ASSETS_KATALOG_YOLU, "r", encoding="utf-8") as f:
        return json.load(f)


def _gorsel_urlleri(kayit):
    return [f"/assets/{g['dosya']}" for g in (kayit.get("gorseller") or []) if g.get("dosya")]


def medya_sec(panel, katalog, adet=3):
    """Her panel.yerler girdisi için ya eşleşen medyayı ya da o yerin isim
    kartını döner — asla alakasız bir yerin medyasını göstermez. Joker/genel
    görsel yalnızca panel.yerler tamamen boşken kullanılır. Kayıtta hem
    youtube_id hem görsel varsa ikisi BİRLİKTE döner (tur="video", ayrıca
    "urls" de dolu) — böylece anlatı akışında önce video oynar, ardından aynı
    yerin fotoğraflarına geçilebilir (bkz. app.js anlatiKarelerineDonustur)."""
    gorulen = set()
    sirali_yerler = []
    for yer in panel.get("yerler") or []:
        if yer and yer not in gorulen:
            gorulen.add(yer)
            sirali_yerler.append(yer)

    if not sirali_yerler:
        genel_kayitlar = [kayit for kayit in katalog if kayit.get("genel")]
        sonuc = []
        for kayit in genel_kayitlar[:adet]:
            urls = _gorsel_urlleri(kayit)
            if urls:
                sonuc.append({"tur": "gorsel", "urls": urls, "yer": None})
        return sonuc

    temalar = set(panel.get("temalar") or [])
    sonuc = []
    for yer in sirali_yerler[:adet]:
        adaylar = [
            kayit for kayit in katalog
            if not kayit.get("genel") and yer in (kayit.get("yerler") or [])
        ]
        if not adaylar:
            sonuc.append({"tur": "isim_karti", "yer": yer})
            continue

        adaylar.sort(key=lambda kayit: -len(temalar & set(kayit.get("temalar", []))))
        secilen = adaylar[0]
        urls = _gorsel_urlleri(secilen)

        if secilen.get("youtube_id"):
            sonuc.append({"tur": "video", "youtube_id": secilen["youtube_id"], "yer": yer, "urls": urls})
        elif urls:
            sonuc.append({"tur": "gorsel", "urls": urls, "yer": yer})
        else:
            sonuc.append({"tur": "isim_karti", "yer": yer})

    return sonuc


def lezzet_medya_sec(lezzetler, katalog, adet=6):
    """panel.lezzetler içindeki her öğe için ya eşleşen tek görseli ya da
    isim kartını döner ("Tatması gereken" şeridi) — yer eşleştirmesiyle aynı
    disiplin (asla alakasız görsel göstermez), ama tek görsel yeterlidir."""
    gorulen = set()
    sonuc = []
    for lezzet in lezzetler:
        if not lezzet or lezzet in gorulen:
            continue
        gorulen.add(lezzet)

        adaylar = [
            kayit for kayit in katalog
            if not kayit.get("genel") and lezzet in (kayit.get("yerler") or [])
        ]
        urls = _gorsel_urlleri(adaylar[0]) if adaylar else []
        if urls:
            sonuc.append({"tur": "gorsel", "url": urls[0], "lezzet": lezzet})
        else:
            sonuc.append({"tur": "isim_karti", "lezzet": lezzet})

        if len(sonuc) >= adet:
            break
    return sonuc


CANLI_GORSEL_SAYISI = 6
CANLI_LEZZET_GORSEL_SAYISI = 1


def _medya_arama_indir_katalogla(slug, adet, varsayilan_temalar, sorgu=None, tema=None, ek_terimler=None, log_etiketi="CANLI"):
    """commons.gorsel_bul (önbellek -> Commons -> Openverse -> Pexels sırası)
    ile en fazla `adet` görseli bulur/indirir ve assets.json'u günceller.
    Hem yer hem lezzet görseli aramasının paylaştığı ortak gövde — çağıran
    thread'i bunu en fazla CANLI_ARAMA_BUDCESI_SN kadar join() ile bekler;
    süre dolunca ilgilenmeden devam eder, bu fonksiyon arka planda çalışmaya
    devam edip işini bitirir (bu yüzden arama VEYA indirme hiçbir zaman
    /sohbet'i bloklamaz)."""
    try:
        sonuc = commons.gorsel_bul(slug, ASSETS_DIZIN, sorgu=sorgu, adet=adet, tema=tema, ek_terimler=ek_terimler)
    except Exception as hata:
        log(f"{log_etiketi} ARAMA HATASI", f"'{slug}': {hata}")
        sonuc = {"kaynak": None, "gorseller": []}

    if sonuc["kaynak"] == "onbellek" or not sonuc["gorseller"]:
        with canli_arama_kilidi:
            canli_arama_isleniyor.discard(slug)
        return

    try:
        with katalog_yazma_kilidi:
            guncel_katalog = commons.katalog_yukle(ASSETS_KATALOG_YOLU)
            guncel_katalog = commons.katalog_gorseller_ekle(
                guncel_katalog, slug, sonuc["gorseller"], varsayilan_temalar,
            )
            commons.katalog_kaydet(guncel_katalog, ASSETS_KATALOG_YOLU)
        log(f"{log_etiketi} GORSEL", f"'{slug}' -> {len(sonuc['gorseller'])} görsel indirildi (kaynak: {sonuc['kaynak']}), katalog güncellendi (sonraki cevapta hazır).")
    except Exception as hata:
        log(f"{log_etiketi} KATALOG HATASI", f"'{slug}': {hata}")

    with canli_arama_kilidi:
        canli_arama_isleniyor.discard(slug)


def _yer_icin_tam_islem(yer, panel_temalari, ek_terimler=None):
    tema = list(panel_temalari)[0] if panel_temalari else None
    _medya_arama_indir_katalogla(
        yer, CANLI_GORSEL_SAYISI, list(panel_temalari) or ["tarih"], tema=tema,
        ek_terimler=ek_terimler, log_etiketi="CANLI YER",
    )


def _lezzet_icin_tam_islem(lezzet):
    """Yer aramasıyla aynı zincir, tek farkla: yemek/içecek odaklı bir sorgu
    kullanır ve tek görsel yeterlidir ("Tatması gereken" şeridi için)."""
    _medya_arama_indir_katalogla(
        lezzet, CANLI_LEZZET_GORSEL_SAYISI, ["yemek"], sorgu=f"{lezzet} Turkish food", log_etiketi="CANLI LEZZET",
    )


def _canli_medya_aramasi_yurut(slugler, katalog, thread_hedefi, butce_sn=CANLI_ARAMA_BUDCESI_SN):
    """Verilen slug listesinde katalogda henüz olmayan her biri için
    thread_hedefi(slug) çağrısını bir thread'e devreder ve o thread'i en
    fazla `butce_sn` (tüm slug'lar toplamında) join() ile bekler. Süre
    dolunca bu turda isim kartına düşülür ama thread arka planda çalışmaya
    devam eder — iş bitince assets.json güncellenir, SONRAKİ cevapta hazır
    olur. /sohbet bu fonksiyon yüzünden asla `butce_sn`'den fazla bloklanmaz."""
    bilinen = set()
    for kayit in katalog:
        bilinen.update(kayit.get("yerler") or [])

    kalan_budce = butce_sn

    for slug in slugler:
        if not slug or slug in bilinen:
            continue
        if kalan_budce <= 0.2:
            continue  # bütçe bitti; bu istekte hiç denenmez, isim kartı döner

        with canli_arama_kilidi:
            if slug in canli_arama_isleniyor:
                continue
            canli_arama_isleniyor.add(slug)

        baslangic = time.monotonic()
        thread = threading.Thread(target=thread_hedefi, args=(slug,), daemon=True)
        thread.start()
        thread.join(timeout=kalan_budce)
        kalan_budce -= (time.monotonic() - baslangic)

        if thread.is_alive():
            log("CANLI ARAMA ZAMAN ASIMI", f"'{slug}' {butce_sn}sn içinde bitmedi, isim kartına düşülüyor; arka planda sürüyor.")


def yerler_icin_canli_arama_baslat(yerler, katalog, panel_temalari, ek_terimler=None):
    _canli_medya_aramasi_yurut(yerler, katalog, lambda yer: _yer_icin_tam_islem(yer, panel_temalari, ek_terimler))


def lezzetler_icin_canli_arama_baslat(lezzetler, katalog):
    _canli_medya_aramasi_yurut(lezzetler, katalog, _lezzet_icin_tam_islem)


def yogunluk_cevabi(gecmis=None):
    """LLM hata verdiğinde veya geçerli JSON döndürmediğinde kullanılan,
    karakter içinden zarif cevap. Teknik ayrıntı burada YOK — o zaten
    çağıran yerde terminale loglandı."""
    panel = panel_duzelt(None)
    panel["dil"] = "tr"  # YOGUNLUK_CEVABI her zaman Türkçe
    katalog = katalog_yukle()
    medyalar = medya_sec(panel, katalog)
    gezgin_profili = profil_ozeti_olustur(profil_hesapla(gecmis), panel["dil"])
    return jsonify({
        "reply": YOGUNLUK_CEVABI,
        "panel": panel,
        "medyalar": medyalar,
        "rota": panel["rota"],
        "rota_koordinatlari": [],
        "lezzet_medyalari": [],
        "gezgin_profili": gezgin_profili,
        "merak_onerileri": merak_db.onerileri_getir(panel["dil"]),
    })


app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
)


def admin_giris_gerekli(fonksiyon):
    @wraps(fonksiyon)
    def sarici(*args, **kwargs):
        if not session.get("admin_giris"):
            return redirect(url_for("admin_giris", sonraki=request.path))
        return fonksiyon(*args, **kwargs)
    return sarici


@app.route("/admin/giris", methods=["GET", "POST"])
def admin_giris():
    hata = None
    kurulum_eksik = not ADMIN_PAROLASI
    if "admin_csrf" not in session:
        session["admin_csrf"] = secrets.token_urlsafe(24)

    if request.method == "POST":
        csrf_gecerli = hmac.compare_digest(
            str(request.form.get("csrf", "")), str(session.get("admin_csrf", ""))
        )
        parola_gecerli = bool(ADMIN_PAROLASI) and hmac.compare_digest(
            str(request.form.get("parola", "")), str(ADMIN_PAROLASI)
        )
        if csrf_gecerli and parola_gecerli:
            session.clear()
            session["admin_giris"] = True
            session.permanent = True
            return redirect(url_for("admin_paneli"))
        hata = "Parola hatalı." if not kurulum_eksik else "Admin parolası henüz yapılandırılmamış."

    return render_template(
        "admin_giris.html", hata=hata, kurulum_eksik=kurulum_eksik,
        csrf=session.get("admin_csrf"),
    )


@app.route("/admin/cikis", methods=["POST"])
def admin_cikis():
    session.clear()
    return redirect(url_for("admin_giris"))


@app.route("/admin")
@admin_giris_gerekli
def admin_paneli():
    if "admin_csrf" not in session:
        session["admin_csrf"] = secrets.token_urlsafe(24)
    return render_template("admin.html", csrf=session["admin_csrf"])


@app.route("/admin/api/ozet")
def admin_api_ozet():
    if not session.get("admin_giris"):
        return jsonify({"hata": "yetkisiz"}), 401
    ozet = merak_db.admin_ozeti_getir()
    ozet["icerik_sagligi"] = kultur_bilgi.icerik_sagligi()
    return jsonify(ozet)


def admin_json_yetkili():
    if not session.get("admin_giris"):
        return False, (jsonify({"hata": "yetkisiz"}), 401)
    gelen_csrf = str(request.headers.get("X-CSRF-Token", ""))
    beklenen_csrf = str(session.get("admin_csrf", ""))
    if request.method != "GET" and not hmac.compare_digest(gelen_csrf, beklenen_csrf):
        return False, (jsonify({"hata": "gecersiz-istek"}), 403)
    return True, None


@app.route("/admin/api/deneyimler")
def admin_api_deneyimler():
    yetkili, cevap = admin_json_yetkili()
    if not yetkili:
        return cevap
    return jsonify({
        "ozet": deneyim_db.admin_ozeti(),
        "iller": deneyim_db.ILLER,
        "deneyimler": deneyim_db.deneyimleri_getir(
            request.args.get("q", ""), request.args.get("durum", "tum")
        ),
    })


@app.route("/admin/api/deneyimler/<int:deneyim_id>/il", methods=["POST"])
def admin_api_deneyim_il_guncelle(deneyim_id):
    yetkili, cevap = admin_json_yetkili()
    if not yetkili:
        return cevap
    gelen = request.get_json(silent=True) or {}
    basarili = deneyim_db.il_durumunu_guncelle(
        deneyim_id, str(gelen.get("il") or ""), str(gelen.get("durum") or "")
    )
    if not basarili:
        return jsonify({"hata": "Geçerli deneyim, il ve durum gerekli."}), 400
    return jsonify({"kaydedildi": True, "ozet": deneyim_db.admin_ozeti()})


@app.route("/admin/api/deneyimler/toplu-onay", methods=["POST"])
def admin_api_deneyim_toplu_onay():
    yetkili, cevap = admin_json_yetkili()
    if not yetkili:
        return cevap
    gelen = request.get_json(silent=True) or {}
    try:
        adet = deneyim_db.yuksek_guvenlileri_onayla(gelen.get("esik", 0.85))
    except (TypeError, ValueError):
        return jsonify({"hata": "Güven eşiği geçerli değil."}), 400
    return jsonify({"kaydedildi": True, "onaylanan": adet, "ozet": deneyim_db.admin_ozeti()})


@app.route("/")
def anasayfa():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/assets/<path:dosya_adi>")
def assets_sun(dosya_adi):
    return send_from_directory(ASSETS_DIZIN, dosya_adi)


@app.route("/meraklar", methods=["GET"])
def meraklar():
    """Dil ve mevcut bağlama göre kültürel merak kartları döndürür."""
    dil = request.args.get("dil", "tr")
    temalar = [x for x in request.args.get("temalar", "").split(",") if x]
    yerler = [x for x in request.args.get("yerler", "").split(",") if x]
    return jsonify({"merak_onerileri": merak_db.onerileri_getir(dil, temalar, yerler)})


@app.route("/konum-sehir", methods=["POST"])
def konum_sehir():
    """İzinle alınan koordinatı il/şehir adına çevirir; koordinatı saklamaz."""
    gelen = request.get_json(silent=True) or {}
    sonuc = konum.nominatim_ters_sehir(gelen.get("lat"), gelen.get("lon"))
    if not sonuc:
        return jsonify({"hata": "Şehir adı konumdan belirlenemedi."}), 404
    if sonuc.get("ulke_kodu") != "tr":
        return jsonify({"hata": "Bugün planı şu anda Türkiye içindeki konumlar için kullanılabilir."}), 400
    if not sonuc.get("sehir"):
        return jsonify({"hata": "Şehir adı konumdan belirlenemedi."}), 404
    return jsonify({"sehir": sonuc["sehir"]})


@app.route("/geri-bildirim", methods=["POST"])
def geri_bildirim():
    gelen = request.get_json(silent=True) or {}
    if not gelen.get("analitik_izin"):
        return jsonify({"kaydedildi": False, "neden": "izin-yok"})
    kaydedildi = merak_db.geri_bildirim_kaydet(
        gelen.get("oturum_id"), gelen.get("konu"), gelen.get("yararli")
    )
    return jsonify({"kaydedildi": kaydedildi})


@app.route("/rota-detay", methods=["POST"])
def rota_detay():
    """Tarayıcıda düzenlenen rota için harita ve yaklaşık ulaşım verisini yeniler."""
    gelen = request.get_json(silent=True) or {}
    rota = [str(x).strip() for x in (gelen.get("rota") or []) if str(x).strip()]
    rota = list(dict.fromkeys(rota))[:12]
    if not rota:
        return jsonify({"rota": [], "rota_koordinatlari": [], "rota_detaylari": []})
    try:
        koordinatlar = konum.rota_koordinatlarini_bul(rota)
        detaylar = konum.rota_detaylarini_hesapla(koordinatlar, gelen.get("dil", "tr"))
    except Exception as hata:
        log("ROTA DÜZENLEME HATASI", str(hata))
        koordinatlar, detaylar = [], []
    return jsonify({
        "rota": rota,
        "rota_koordinatlari": koordinatlar,
        "rota_detaylari": detaylar,
    })


@app.route("/yakinimda", methods=["POST"])
def yakindaki_yerler():
    gelen = request.get_json(silent=True) or {}
    demo = gelen.get("demo_modu") is True
    try:
        yaricap = max(500, min(int(gelen.get("yaricap") or 3000), 5000))
    except (TypeError, ValueError):
        yaricap = 3000
    if demo:
        merkez = {"lat": 41.0084, "lon": 28.9784, "ad": "Sultanahmet (Demo)"}
        yerler = yakinimda.demo_sonuclari(yaricap)
    else:
        try:
            lat, lon = float(gelen.get("lat")), float(gelen.get("lon"))
        except (TypeError, ValueError):
            return jsonify({"hata": "Geçerli konum gerekli."}), 400
        if not (35.5 <= lat <= 42.2 and 25.5 <= lon <= 45.0):
            return jsonify({"hata": "Yakınımda modu şu anda Türkiye içinde kullanılabilir."}), 400
        merkez = {"lat": lat, "lon": lon, "ad": "Mevcut konum"}
        try:
            yerler = yakinimda.ara(lat, lon, yaricap)
        except Exception as hata:
            log("YAKINIMDA HATASI", str(hata))
            yerler = yakinimda.yerel_yedek_sonuclari(
                lat, lon, yaricap, konum.koordinat_yukle(), {
                    slug for slug, (_, kategori, _) in mekan_bilgi.MEKANLAR.items()
                    if "sehir" not in kategori
                }
            )
            if not yerler:
                return jsonify({
                    "hata": "OpenStreetMap şu anda yanıt vermiyor ve bu çevre için yerel sonuç bulunamadı. Demo Modu ile deneyebilirsin."
                }), 503
            merkez["ad"] = "Mevcut konum · yerel yedek"

    if yerler:
        onbellek = konum.koordinat_yukle()
        for yer in yerler:
            onbellek[yer["slug"]] = {"lat": yer["lat"], "lon": yer["lon"]}
        konum.koordinat_kaydet(onbellek)
    return jsonify({
        "merkez": merkez, "yaricap": yaricap, "yerler": yerler,
        "uyari": "OpenStreetMap geçici olarak yanıt vermedi; kayıtlı yakın yerler gösteriliyor." if "yerel yedek" in merkez["ad"] else None,
    })


@app.route("/mekan-anlat", methods=["POST"])
def mekan_anlatimi():
    gelen = request.get_json(silent=True) or {}
    slug = str(gelen.get("slug") or "").strip()[:80]
    ad = str(gelen.get("ad") or slug.replace("-", " ").title()).strip()[:120]
    tur = str(gelen.get("tur") or "turistik yer").strip()[:60]
    mod = gelen.get("mod") if gelen.get("mod") in ("kisa", "hikaye", "detay") else "kisa"
    dil = gelen.get("dil") if gelen.get("dil") in ("tr", "en", "de", "ja") else "tr"
    yerel = mekan_anlat.anlat(slug, ad, mod, dil)
    if yerel:
        return jsonify(yerel)
    if gelen.get("demo_modu") is True:
        metin = (f"{ad}, yakındaki {tur.replace('-', ' ')} noktalarından biridir. "
                 "Bu demo kaydında doğrulanmış ayrıntılı anlatım henüz bulunmuyor; rotana ekleyip çevresini keşfedebilirsin.")
        return jsonify({"reply": metin, "kaynak_turu": "demo-genel", "yer": ad})
    if not API_ANAHTARI:
        return jsonify({"reply": "Bu mekân için anlatım henüz hazırlanmadı.", "kaynak_turu": "yok", "yer": ad})
    mod_notu = {
        "kisa": "yaklaşık 60 saniyede okunacak, 3-4 cümlelik öz bir anlatım",
        "hikaye": "Evliya Çelebi'nin ağzından, tarihî gerçeği bozmayan kısa ve canlı bir hikâye",
        "detay": "tarihî bağlam, dikkat edilecek ayrıntılar ve ziyaret adabı içeren 2-3 kısa paragraf",
    }[mod]
    istek = f"{ad} ({tur}) için {mod_notu} yaz. Uydurma tarih, efsane veya güncel ücret/saat verme. panel alanlarını boş bırak."
    try:
        ham = llm_cevapla([types.Content(role="user", parts=[types.Part(text=istek)])])
        veri, hata = json_ayikla(ham)
        if veri and veri.get("reply"):
            return jsonify({"reply": veri["reply"], "kaynak_turu": "yapay-zeka", "yer": ad})
        log("MEKAN ANLATIM PARSE HATASI", f"{hata} | {ham if ham else 'BOS'}")
    except Exception as hata:
        log("MEKAN ANLATIM HATASI", str(hata))
    return jsonify({
        "reply": "Kervanım bugün epey yol aldı; bu mekânın hikâyesini az sonra yeniden sor, dostum.",
        "kaynak_turu": "gecici-hata", "yer": ad,
    })


@app.route("/gunluk-plan", methods=["POST"])
def gunluk_plan_uret():
    gelen = request.get_json(silent=True) or {}
    profil = profil_hesapla(gelen.get("gecmis") or [])
    try:
        plan = gunluk_plan.plan_olustur(
            sehir=str(gelen.get("sehir") or "istanbul"),
            sure=str(gelen.get("sure") or "yarim-gun"),
            ulasim=str(gelen.get("ulasim") or "yuruyus"),
            ilgi=str(gelen.get("ilgi") or "tarih"),
            tempo=str(gelen.get("tempo") or "dengeli"),
            profil=profil, lat=gelen.get("lat"), lon=gelen.get("lon"),
            kosul=gelen.get("kosul") if gelen.get("kosul") in ("yoruldum", "yagmur", "aciktim", "vakit-az") else None,
        )
    except (TypeError, ValueError):
        return jsonify({"hata":"Konum bilgisi geçerli değil."}), 400
    if not plan:
        return jsonify({"hata":"Bu şehir/yer için gezilecek nokta bulunamadı. Yazımı kontrol et ya da başka bir yer dene."}), 400
    for durak in plan.get("duraklar", []):
        durak["gitmeden_once"] = mekan_rehber.bilgi_olustur(durak.get("slug"), durak, plan.get("sehir"))
    plan["profil"] = profil_ozeti_olustur(profil, gelen.get("dil", "tr"))
    return jsonify(plan)


@app.route("/sohbet", methods=["POST"])
def sohbet():
    gelen = request.get_json(silent=True) or {}
    demo_modu = gelen.get("demo_modu") is True
    if not API_ANAHTARI and not demo_modu:
        return jsonify({"hata": "GEMINI_API_KEY tanımlı değil (.env dosyasını kontrol et)."}), 500

    mesaj = (gelen.get("mesaj") or "").strip()
    gecmis = gelen.get("gecmis") or []
    analitik_izin = gelen.get("analitik_izin") is True
    oturum_id = gelen.get("oturum_id")
    ulke = gelen.get("ulke")

    if not mesaj:
        return jsonify({"hata": "mesaj alanı boş olamaz."}), 400

    profil_su_ana_kadar = profil_hesapla(gecmis)
    merak_konusu = merak_db.konu_bul(mesaj)
    baglam_parcalari = [
        baglam_notu_olustur(profil_su_ana_kadar),
        kultur_bilgi.llm_baglam_notu(merak_konusu),
    ]
    baglam_notu = "\n\n".join(parca for parca in baglam_parcalari if parca) or None

    if demo_modu:
        kucuk = mesaj.lower()
        ingilizce = any(kelime in kucuk for kelime in ("plan", "show", "history", "food", "nature", "route"))
        if any(kelime in kucuk for kelime in ("food", "yemek", "lezzet", "mutfak")):
            yerler, temalar, lezzetler = ["gaziantep", "hatay", "adana"], ["yemek"], ["beyran", "kunefe", "adana-kebabi"]
            reply_tr = "Ey yolcu, sofranın izini Gaziantep'ten Hatay'a, oradan Adana'ya sürdüm. Beyranı sabah, künefeyi yerinde tat; çarşıların sesini de sofraya kat."
            reply_en = "Traveler, I traced a generous table from Gaziantep to Hatay and Adana. Taste beyran in the morning, künefe where it was born, and listen to the rhythm of the old bazaars."
        elif any(kelime in kucuk for kelime in ("nature", "doğa", "doga", "quiet", "sakin", "sea", "deniz")):
            yerler, temalar, lezzetler = ["akyaka", "datca", "egirdir"], ["doga", "sakin", "deniz"], ["balik"]
            reply_tr = "Ey yolcu, seni Akyaka'nın sazlıklarından Datça'nın rüzgârına, ardından Eğirdir'in dingin gölüne götüren sakin bir rota hazırladım."
            reply_en = "Traveler, I prepared a quiet route from Akyaka's reed beds to Datça's breeze and the calm waters of Lake Eğirdir."
        else:
            yerler, temalar, lezzetler = ["istanbul", "safranbolu", "ankara"], ["tarih", "sakin"], ["simit", "safranbolu-lokumu", "ankara-doneri"]
            reply_tr = "Ey yolcu, İstanbul'dan Safranbolu'nun konaklarına, oradan Ankara'nın kadim izlerine uzanan üç günlük bir tarih rotası hazırladım."
            reply_en = "Traveler, I prepared a three-day history route from Istanbul to Safranbolu's Ottoman houses and onward to Ankara's ancient traces."
        veri = {
            "reply": reply_en if ingilizce else reply_tr,
            "panel": {
                "yerler": yerler, "temalar": temalar, "rota": yerler,
                "duygu": "merak", "medya": "gorsel", "dil": "en" if ingilizce else "tr",
                "lezzetler": lezzetler, "deneyimler": ["yerel-carsi"], "kultur": None,
            },
        }
    else:
        contents = gecmisten_contents_olustur(mesaj, gecmis)
        try:
            ham = llm_cevapla(contents, ek_baglam=baglam_notu)
        except Exception as hata:
            log("LLM HATASI", f"mesaj={mesaj!r} -> {hata}")
            return yogunluk_cevabi(gecmis)

        veri, hata = json_ayikla(ham)
        if not veri:
            log("JSON PARSE HATASI", f"{hata} | HAM YANIT: {ham if ham else 'BOS'}")
            return yogunluk_cevabi(gecmis)

    reply = veri.get("reply", "")
    panel = panel_duzelt(veri.get("panel"))
    katalog = katalog_yukle()
    # Bu turda Evliya'nın somut olarak bahsettiği lezzet/deneyim adları, görsel
    # arama sorgusunu zenginleştirmek için kullanılır (bkz. commons.gorsel_bul
    # ek_terimler) — böylece görseller yalnızca yerle değil, o an anlatılanla
    # da uyumlu gelir (ör. "Safranbolu lokum", "Safranbolu ahşap konak").
    ek_terimler = (panel.get("lezzetler") or []) + (panel.get("deneyimler") or [])
    yerler_icin_canli_arama_baslat(panel["yerler"], katalog, panel.get("temalar"), ek_terimler)
    medyalar = medya_sec(panel, katalog)
    mekan_detaylari = mekan_bilgi.detaylari_olustur(panel["yerler"], panel.get("temalar"))

    lezzetler = panel.get("lezzetler") or []
    if lezzetler:
        lezzetler_icin_canli_arama_baslat(lezzetler, katalog)
    lezzet_medyalari = lezzet_medya_sec(lezzetler, katalog)

    rota_koordinatlari = []
    rota_detaylari = []
    if panel["rota"]:
        try:
            rota_koordinatlari = konum.rota_koordinatlarini_bul(panel["rota"])
            rota_detaylari = konum.rota_detaylarini_hesapla(rota_koordinatlari, panel.get("dil", "tr"))
        except Exception as hata:
            log("ROTA KOORDINAT HATASI", f"{panel['rota']}: {hata}")

    guncel_puanlar = dict(profil_su_ana_kadar)
    for tema in panel.get("temalar") or []:
        if tema in TEMA_KELIME_HAVUZU:
            guncel_puanlar[tema] = guncel_puanlar.get(tema, 0) + 1
    gezgin_profili = profil_ozeti_olustur(guncel_puanlar, panel["dil"])

    if analitik_izin and merak_konusu:
        try:
            merak_db.sinyal_kaydet(oturum_id, panel["dil"], ulke, merak_konusu)
        except Exception as hata:
            log("MERAK KAYIT HATASI", str(hata))
    merak_onerileri = merak_db.onerileri_getir(
        panel["dil"], panel.get("temalar"), panel.get("yerler")
    )

    return jsonify({
        "reply": reply,
        "panel": panel,
        "medyalar": medyalar,
        "mekan_detaylari": mekan_detaylari,
        "rota": panel["rota"],
        "rota_koordinatlari": rota_koordinatlari,
        "rota_detaylari": rota_detaylari,
        "lezzet_medyalari": lezzet_medyalari,
        "gezgin_profili": gezgin_profili,
        "merak_onerileri": merak_onerileri,
        "merak_konusu": merak_konusu,
        "kultur_kaynagi": kultur_bilgi.istemci_kaydi(merak_konusu),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000, threaded=True)
