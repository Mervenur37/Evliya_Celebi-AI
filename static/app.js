const mesajAkisi = document.getElementById("mesajAkisi");
const mesajFormu = document.getElementById("mesajFormu");
const mesajGirisi = document.getElementById("mesajGirisi");
const defterHarita = document.getElementById("defterHarita");
const defterMedya = document.getElementById("defterMedya");
const anlatiSahnesi = document.getElementById("anlatiSahnesi");
const anlatiMedya = document.getElementById("anlatiMedya");
const anlatiMetniEl = document.getElementById("anlatiMetni");
const altyaziDugmesi = document.getElementById("altyaziDugmesi");
const defterLezzet = document.getElementById("defterLezzet");
const defterRota = document.getElementById("defterRota");
const gezginProfili = document.getElementById("gezginProfili");
const sesDugmesi = document.getElementById("sesDugmesi");
const sesSecimi = document.getElementById("sesSecimi");
const dilSecimi = document.getElementById("dilSecimi");
const kartButonu = document.getElementById("kartButonu");
const kartOverlay = document.getElementById("kartOverlay");
const kartCanvas = document.getElementById("kartCanvas");
const kartIndirButonu = document.getElementById("kartIndirButonu");
const kartKapatButonu = document.getElementById("kartKapatButonu");
const kartYukleniyor = document.getElementById("kartYukleniyor");
const kartEksikNotu = document.getElementById("kartEksikNotu");
const baslangicKartlari = document.getElementById("baslangicKartlari");
const kulturSorulari = document.getElementById("kulturSorulari");
const yeniYolculukButonu = document.getElementById("yeniYolculukButonu");
const yolculukOverlay = document.getElementById("yolculukOverlay");
const yolculukKapat = document.getElementById("yolculukKapat");
const yolculukIcerik = document.getElementById("yolculukIcerik");
const yolculukIlerleme = document.getElementById("yolculukIlerleme");
const merakIzinOverlay = document.getElementById("merakIzinOverlay");
const merakIzinVer = document.getElementById("merakIzinVer");
const merakIzinReddet = document.getElementById("merakIzinReddet");
const merakUlke = document.getElementById("merakUlke");
const merakGizlilikNotu = document.getElementById("merakGizlilikNotu");
const demoModuDugmesi = document.getElementById("demoModuDugmesi");
const demoBildirimi = document.getElementById("demoBildirimi");
const yakinimdaButonu = document.getElementById("yakinimdaButonu");
const yakinimdaYaricap = document.getElementById("yakinimdaYaricap");
const yakinimdaDurum = document.getElementById("yakinimdaDurum");
const yakinimdaListesi = document.getElementById("yakinimdaListesi");
const mekanAnlatOverlay = document.getElementById("mekanAnlatOverlay");
const mekanAnlatKapat = document.getElementById("mekanAnlatKapat");
const mekanAnlatBaslik = document.getElementById("mekanAnlatBaslik");
const mekanAnlatTur = document.getElementById("mekanAnlatTur");
const mekanAnlatMetni = document.getElementById("mekanAnlatMetni");
const mekanAnlatKaynak = document.getElementById("mekanAnlatKaynak");
const mekanAnlatDinle = document.getElementById("mekanAnlatDinle");
const mekanAnlatRotayaEkle = document.getElementById("mekanAnlatRotayaEkle");
const anlatimModuDugmeleri = document.querySelectorAll(".anlatim-modu-dugmesi");
const gunlukPlanFormu = document.getElementById("gunlukPlanFormu");
const gunlukPlanSonucu = document.getElementById("gunlukPlanSonucu");
const planKonumButonu = document.getElementById("planKonumButonu");
const planKonumDurumu = document.getElementById("planKonumDurumu");
const planSehirGirisi = document.getElementById("planSehir");
const seyahatModu = document.getElementById("seyahatModu");
const seyahatModuKapat = document.getElementById("seyahatModuKapat");
const seyahatPlanBaslik = document.getElementById("seyahatPlanBaslik");
const seyahatIlerlemeCubugu = document.getElementById("seyahatIlerlemeCubugu");
const seyahatIlerlemeMetni = document.getElementById("seyahatIlerlemeMetni");
const seyahatDurakNo = document.getElementById("seyahatDurakNo");
const seyahatDurakAdi = document.getElementById("seyahatDurakAdi");
const seyahatDurakTuru = document.getElementById("seyahatDurakTuru");
const seyahatDurakNedeni = document.getElementById("seyahatDurakNedeni");
const seyahatZiyaretSuresi = document.getElementById("seyahatZiyaretSuresi");
const seyahatUlasimBilgisi = document.getElementById("seyahatUlasimBilgisi");
const seyahatSonraki = document.getElementById("seyahatSonraki");
const seyahatYolTarifi = document.getElementById("seyahatYolTarifi");
const seyahatEvliyaAnlat = document.getElementById("seyahatEvliyaAnlat");
const seyahatGeldim = document.getElementById("seyahatGeldim");
const seyahatGec = document.getElementById("seyahatGec");
const seyahatDurumNotu = document.getElementById("seyahatDurumNotu");
const seyahatOncesiDugmesi = document.getElementById("seyahatOncesiDugmesi");
const seyahatOncesiIcerik = document.getElementById("seyahatOncesiIcerik");

const i18n = window.EVLIYA_I18N;
let dilTercihi = localStorage.getItem("evliyaArayuzDili") || "auto";
if (!["auto", ...(i18n ? i18n.supported : ["tr", "en", "de", "ja"])].includes(dilTercihi)) dilTercihi = "auto";
let aktifArayuzDili = dilTercihi === "auto" ? (i18n ? i18n.detect() : "tr") : dilTercihi;

function t(anahtar, degiskenler = {}) {
  return i18n ? i18n.t(aktifArayuzDili, anahtar, degiskenler) : anahtar;
}

function statikMetinleriUygula() {
  document.documentElement.lang = aktifArayuzDili;
  document.querySelectorAll("[data-i18n]").forEach((oge) => { oge.textContent = t(oge.dataset.i18n); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((oge) => { oge.placeholder = t(oge.dataset.i18nPlaceholder); });
  document.querySelectorAll("[data-i18n-title]").forEach((oge) => { oge.title = t(oge.dataset.i18nTitle); });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((oge) => { oge.setAttribute("aria-label", t(oge.dataset.i18nAriaLabel)); });
  if (dilSecimi) {
    dilSecimi.value = dilTercihi;
    dilSecimi.title = dilTercihi === "auto" ? t("auto_language_note") : dilSecimi.options[dilSecimi.selectedIndex]?.text || "Language";
  }
}

function arayuzDiliniAyarla(dil, cevapDiliMi = false) {
  if (!i18n || !i18n.supported.includes(dil)) return;
  if (cevapDiliMi && dilTercihi !== "auto") return;
  aktifArayuzDili = dil;
  statikMetinleriUygula();
  demoModunuGuncelle();
  gorselAltyaziDurumunuGuncelle();
  sesDugmesiniGuncelle();
  sesSecimiOlustur();
  if (typeof baslangicKartlariniOlustur === "function") baslangicKartlariniOlustur();
  if (typeof merakIzinDurumunuGuncelle === "function") merakIzinDurumunuGuncelle();
  if (duzenlenenRota.length) rotaGuncelle(duzenlenenRota, duzenlenenRotaDetaylari, true);
  if (aktifGunlukPlan) gunlukPlaniCiz(aktifGunlukPlan);
  if (seyahatModu?.classList.contains("gorunur")) seyahatDuraginiCiz();
  kulturGosterilenDil = null;
  kulturSorulariniOlustur(aktifArayuzDili);
}

if (dilSecimi) {
  dilSecimi.addEventListener("change", () => {
    dilTercihi = dilSecimi.value;
    localStorage.setItem("evliyaArayuzDili", dilTercihi);
    arayuzDiliniAyarla(dilTercihi === "auto" ? i18n.detect() : dilTercihi);
  });
}
statikMetinleriUygula();

let gecmis = [];
let demoModu = localStorage.getItem("evliyaDemoModu") === "acik";
let merakAnalitikIzni = localStorage.getItem("evliyaMerakIzni") === "evet";
let merakUlkeKodu = localStorage.getItem("evliyaMerakUlke") || "";
let merakOturumId = sessionStorage.getItem("evliyaMerakOturum");
if (!merakOturumId) {
  merakOturumId = (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);
  sessionStorage.setItem("evliyaMerakOturum", merakOturumId);
}

const ISTEK_ZAMAN_ASIMI_MS = 30000;
const YOGUNLUK_MESAJI = () => t("busy_reply");
const SLAYT_ARALIGI_MS = 4000;
const ROTA_CIZIM_SURESI_MS = 1500;
let aktifMekanAnlatimi = null;
let sonMekanAnlatimMetni = "";
let planKonumu = null;
let sonYakinimdaKonumu = null;
let aktifGunlukPlan = null;
let seyahatDurakIndex = 0;
const ziyaretEdilenDuraklar = new Set();

function demoModunuGuncelle() {
  if (!demoModuDugmesi || !demoBildirimi) return;
  demoModuDugmesi.textContent = demoModu ? t("demo_on") : t("demo_off");
  demoModuDugmesi.title = t("demo_title");
  demoModuDugmesi.classList.toggle("aktif", demoModu);
  demoModuDugmesi.setAttribute("aria-pressed", String(demoModu));
  demoBildirimi.classList.toggle("gorunur", demoModu);
}

if (demoModuDugmesi) {
  demoModuDugmesi.addEventListener("click", () => {
    demoModu = !demoModu;
    localStorage.setItem("evliyaDemoModu", demoModu ? "acik" : "kapali");
    demoModunuGuncelle();
  });
  demoModunuGuncelle();
}

// Sohbet metni zaten ana okuma alanı olduğu için görsel altyazısı varsayılan
// olarak kapalıdır. Erişilebilirlik/TTS takibi isteyen kullanıcı CC ile açar.
let gorselAltyaziAcik = localStorage.getItem("evliyaGorselAltyazi") === "acik";

function gorselAltyaziDurumunuGuncelle() {
  if (!anlatiSahnesi || !altyaziDugmesi) return;
  anlatiSahnesi.classList.toggle("altyazi-acik", gorselAltyaziAcik);
  altyaziDugmesi.classList.toggle("aktif", gorselAltyaziAcik);
  altyaziDugmesi.setAttribute("aria-pressed", String(gorselAltyaziAcik));
  altyaziDugmesi.textContent = gorselAltyaziAcik ? t("captions_on") : t("captions");
  altyaziDugmesi.title = gorselAltyaziAcik ? t("captions_disable") : t("captions_enable");
}

if (altyaziDugmesi) {
  altyaziDugmesi.addEventListener("click", () => {
    gorselAltyaziAcik = !gorselAltyaziAcik;
    localStorage.setItem("evliyaGorselAltyazi", gorselAltyaziAcik ? "acik" : "kapali");
    gorselAltyaziDurumunuGuncelle();
  });
  gorselAltyaziDurumunuGuncelle();
}

// ---- Seyahat Defteri sekmeleri ---------------------------------------------
// Görseller/Harita/Profil aynı anda görünmez; dikkat dağılmasın diye
// kullanıcı hangisini göreceğini seçer. Varsayılan: Görseller. Harita
// sekmesi ilk rota gelene kadar devre dışıdır (bkz. haritayiGuncelle).

const defterSekmeDugmeleri = document.querySelectorAll(".defter-sekme-dugmesi");
const defterSekmeIcerikleri = document.querySelectorAll(".defter-sekme-icerik");

// ---- Kenar çubuğu: Sohbet / Bugün / Yakınımda / Meraklar / Ayarlar -------
// Tek seferde tek bölüm görünür; Görseller/Harita/Profil sekmeleri hâlâ
// yalnızca Sohbet görünümü içinde yaşıyor (bkz. sekmeSec altında).
const kenarDugmeleri = document.querySelectorAll(".kenar-dugmesi[data-gorunum]");
const gorunumIcerikleri = document.querySelectorAll(".gorunum-icerik");

function gorunumSec(gorunumAdi) {
  kenarDugmeleri.forEach((dugme) => {
    dugme.classList.toggle("aktif", dugme.dataset.gorunum === gorunumAdi);
  });
  gorunumIcerikleri.forEach((icerik) => {
    icerik.classList.toggle("aktif", icerik.dataset.gorunumIcerik === gorunumAdi);
  });
  if (gorunumAdi === "sohbet") {
    const haritaSekmesiAktifMi = document.querySelector('.defter-sekme-dugmesi[data-sekme="harita"].aktif');
    if (haritaSekmesiAktifMi) haritaBoyutunuYenile();
  }
}

kenarDugmeleri.forEach((dugme) => {
  dugme.addEventListener("click", () => gorunumSec(dugme.dataset.gorunum));
});

function sekmeSec(sekmeAdi) {
  // Görseller/Harita/Profil sekmeleri yalnızca Sohbet görünümünde yaşıyor;
  // bu fonksiyon Meraklar/Bugün gibi başka görünümlerden de çağrılabildiği
  // için (ör. bir soru kartına tıklayınca) önce Sohbet'e dönmemiz gerekir,
  // yoksa güncelleme gizli bir görünümde sessizce gerçekleşir.
  gorunumSec("sohbet");
  defterSekmeDugmeleri.forEach((dugme) => {
    const aktifMi = dugme.dataset.sekme === sekmeAdi;
    dugme.classList.toggle("aktif", aktifMi);
    dugme.setAttribute("aria-selected", String(aktifMi));
  });
  defterSekmeIcerikleri.forEach((icerik) => {
    icerik.classList.toggle("aktif", icerik.dataset.sekmeIcerik === sekmeAdi);
  });
  if (sekmeAdi === "harita") haritaBoyutunuYenile();
}

defterSekmeDugmeleri.forEach((dugme) => {
  dugme.addEventListener("click", () => {
    if (dugme.disabled) return;
    sekmeSec(dugme.dataset.sekme);
  });
});

function balonEkle(rol, metin) {
  const balon = document.createElement("div");
  balon.className = `balon ${rol}`;
  const p = document.createElement("p");
  p.textContent = metin;
  balon.appendChild(p);
  mesajAkisi.appendChild(balon);
  mesajAkisi.scrollTop = mesajAkisi.scrollHeight;
  return balon;
}

// "Yabancılar Soruyor, Evliya Cevaplıyor": kültür sorularında panel.kultur
// doluysa (bkz. SISTEM_PROMPTU EK ALAN), cevap balonunun altına üç etiketli
// bir kart eklenir — hikaye/kulturel_not/adab, hepsi opsiyonel doldurulabilir.
const KULTUR_ETIKETLERI = {
  tr: { hikaye: "Evliya'nın Hikâyesi", kulturel_not: "Kültürel Not", adab: "Adab / Dikkat" },
  en: { hikaye: "Evliya's Story", kulturel_not: "Cultural Note", adab: "Etiquette" },
  de: { hikaye: "Evliyas Geschichte", kulturel_not: "Kulturelle Notiz", adab: "Etikette" },
  ja: { hikaye: "エヴリヤの物語", kulturel_not: "文化的な注記", adab: "作法・心得" },
};

function kulturEtiketleriGetir(dilKodu) {
  return KULTUR_ETIKETLERI[dilKodu] || KULTUR_ETIKETLERI.en;
}

function kulturCevabiEkle(kultur, dilKodu, merakKonusu, kulturKaynagi) {
  if (!kultur) return;
  const etiketler = kulturEtiketleriGetir(dilKodu);
  const kart = document.createElement("div");
  kart.className = "kultur-cevap-karti";

  [["hikaye", kultur.hikaye], ["kulturel_not", kultur.kulturel_not], ["adab", kultur.adab]].forEach(([anahtar, metin]) => {
    if (!metin) return;
    const bolum = document.createElement("div");
    bolum.className = "kultur-cevap-bolumu";
    const baslik = document.createElement("span");
    baslik.className = "kultur-cevap-etiket";
    baslik.textContent = etiketler[anahtar];
    const govde = document.createElement("p");
    govde.textContent = metin;
    bolum.appendChild(baslik);
    bolum.appendChild(govde);
    kart.appendChild(bolum);
  });

  if (kart.children.length === 0) return;
  if (kulturKaynagi) {
    const kaynakMetinleri = {
      tr: { ac: "Kaynakları göster", kapat: "Kaynakları gizle", kontrol: "Son kontrol", inceleniyor: "Kaynak doğrulaması sürüyor" },
      en: { ac: "Show sources", kapat: "Hide sources", kontrol: "Last reviewed", inceleniyor: "Source review in progress" },
      de: { ac: "Quellen anzeigen", kapat: "Quellen ausblenden", kontrol: "Zuletzt geprüft", inceleniyor: "Quellenprüfung läuft" },
      ja: { ac: "出典を表示", kapat: "出典を隠す", kontrol: "最終確認", inceleniyor: "出典を確認中" },
    }[dilKodu] || { ac: "Show sources", kapat: "Hide sources", kontrol: "Last reviewed", inceleniyor: "Source review in progress" };
    const kaynakAlani = document.createElement("div");
    kaynakAlani.className = "kultur-kaynak-alani";
    if (kulturKaynagi.durum === "onayli" && kulturKaynagi.kaynaklar.length) {
      const dugme = document.createElement("button");
      dugme.type = "button"; dugme.className = "kultur-kaynak-dugmesi";
      dugme.textContent = `✓ ${kaynakMetinleri.ac}`; dugme.setAttribute("aria-expanded", "false");
      const liste = document.createElement("div"); liste.className = "kultur-kaynak-listesi";
      kulturKaynagi.kaynaklar.forEach((kaynak) => {
        const baglanti = document.createElement("a"); baglanti.href = kaynak.url;
        baglanti.target = "_blank"; baglanti.rel = "noopener noreferrer";
        baglanti.textContent = `${kaynak.kurum} — ${kaynak.baslik}`; liste.appendChild(baglanti);
      });
      const tarih = document.createElement("small");
      tarih.textContent = `${kaynakMetinleri.kontrol}: ${kulturKaynagi.son_kontrol}`; liste.appendChild(tarih);
      dugme.addEventListener("click", () => {
        const acik = liste.classList.toggle("gorunur");
        dugme.setAttribute("aria-expanded", String(acik));
        dugme.textContent = `✓ ${acik ? kaynakMetinleri.kapat : kaynakMetinleri.ac}`;
      });
      kaynakAlani.append(dugme, liste);
    } else {
      kaynakAlani.classList.add("incelemede");
      kaynakAlani.textContent = `◷ ${kaynakMetinleri.inceleniyor}`;
    }
    kart.appendChild(kaynakAlani);
  }
  if (merakKonusu && merakAnalitikIzni) {
    const geriMetinleri = {
      tr: ["Bu kültürel cevap yararlı mıydı?", "Teşekkürler, yolcu."],
      en: ["Was this cultural answer helpful?", "Thank you, traveler."],
      de: ["War diese kulturelle Antwort hilfreich?", "Danke, Reisender."],
      ja: ["この文化的な回答は役に立ちましたか？", "ありがとう、旅人よ。"],
    }[dilKodu] || ["Was this cultural answer helpful?", "Thank you, traveler."];
    const geriBildirim = document.createElement("div");
    geriBildirim.className = "merak-geri-bildirim";
    geriBildirim.innerHTML = `<span>${geriMetinleri[0]}</span>`;
    [["👍", true], ["👎", false]].forEach(([etiket, yararli]) => {
      const dugme = document.createElement("button");
      dugme.type = "button";
      dugme.textContent = etiket;
      dugme.addEventListener("click", async () => {
        geriBildirim.querySelectorAll("button").forEach((d) => { d.disabled = true; });
        try {
          await fetch("/geri-bildirim", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ analitik_izin: true, oturum_id: merakOturumId, konu: merakKonusu, yararli }),
          });
          geriBildirim.querySelector("span").textContent = geriMetinleri[1];
        } catch (hata) { console.error("Geri bildirim gönderilemedi:", hata); }
      });
      geriBildirim.appendChild(dugme);
    });
    kart.appendChild(geriBildirim);
  }
  mesajAkisi.appendChild(kart);
  mesajAkisi.scrollTop = mesajAkisi.scrollHeight;
}

function gorselOgesiOlustur(urls, yer) {
  const kapsayici = document.createElement("div");
  kapsayici.className = "medya-oge";

  const imgler = urls.map((url, i) => {
    const img = document.createElement("img");
    img.src = url;
    img.alt = yer ? `${yerAdiniYaz(yer)} — ${t("turkey_frame")}` : t("turkey_frame");
    if (i === 0) img.classList.add("aktif");
    kapsayici.appendChild(img);
    return img;
  });

  // Birden fazla görsel varsa yumuşak çapraz geçişle (crossfade) döndür;
  // tek görsel varsa sabit kalır.
  if (imgler.length > 1) {
    let index = 0;
    setInterval(() => {
      imgler[index].classList.remove("aktif");
      index = (index + 1) % imgler.length;
      imgler[index].classList.add("aktif");
    }, SLAYT_ARALIGI_MS);
  }

  const etiket = document.createElement("div");
  etiket.className = "medya-yer-etiketi";
  etiket.innerHTML = `<strong>${yerAdiniYaz(yer)}</strong><span>Türkiye · ${urls.length} ${urls.length > 1 ? t("photos") : t("photo")}</span>`;
  kapsayici.appendChild(etiket);

  return kapsayici;
}

function videoOgesiOlustur(youtubeId, yer) {
  const kapsayici = document.createElement("div");
  kapsayici.className = "video-oge";

  const iframe = document.createElement("iframe");
  const id = encodeURIComponent(youtubeId);
  iframe.src = `https://www.youtube.com/embed/${id}?autoplay=1&mute=1&loop=1&playlist=${id}&controls=1`;
  iframe.title = yer ? `${yerAdiniYaz(yer)} — ${t("promo_video")}` : `Türkiye — ${t("promo_video")}`;
  iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
  iframe.allowFullscreen = true;
  iframe.frameBorder = "0";

  kapsayici.appendChild(iframe);
  const etiket = document.createElement("div");
  etiket.className = "medya-yer-etiketi video-etiketi";
  etiket.innerHTML = `<strong>${yerAdiniYaz(yer)}</strong><span>${t("promo_video")}</span>`;
  kapsayici.appendChild(etiket);
  return kapsayici;
}

// Seyahat defteri sohbet boyunca BİRİKİR: her /sohbet cevabı defteri
// sıfırlamaz, yalnızca o cevaptaki yeni yerleri ekler. Aynı yer tekrar
// gelirse çoğaltılmaz; ama önce isim kartı olarak eklenmiş bir yer daha
// sonra gerçek bir görselle/videoyla gelirse (canlı arama tamamlandığında),
// kart yerinde gerçek görsele YÜKSELTİLİR. yerGaleriKayitlari bu yüzden
// {yer -> {tur, element}} tutar.
const yerGaleriKayitlari = new Map();
const mekanDetayKayitlari = new Map();
let duzenlenenRota = [];
let duzenlenenRotaDetaylari = [];
let rotaGunleri = new Map();
const PLAN_METINLERI = {
  tr: { sureNotu:"Saat ve ücret için resmî kaynağı kontrol et", ekle:"+ Rotama ekle", rotada:"✓ Rotada", rota:"Gün Gün Rotan", aciklama:"Durakları sırala, güne ata veya çıkar.", durak:"durak", gun:"gün", yaklasik:"Yaklaşık", yukari:"Yukarı taşı", asagi:"Aşağı taşı", sil:"Rotadan çıkar", tahmin:"Mesafe ve süreler yaklaşık planlama değerleridir; yol ve sefer koşullarına göre değişebilir." },
  en: { sureNotu:"Check the official source for hours and admission", ekle:"+ Add to my route", rotada:"✓ On route", rota:"Your Day-by-Day Route", aciklama:"Reorder, assign a day or remove stops.", durak:"stops", gun:"day", yaklasik:"About", yukari:"Move up", asagi:"Move down", sil:"Remove", tahmin:"Distances and times are planning estimates and may change with road and service conditions." },
  de: { sureNotu:"Öffnungszeiten und Eintritt offiziell prüfen", ekle:"+ Zur Route", rotada:"✓ In der Route", rota:"Deine Tagesroute", aciklama:"Stopps ordnen, Tagen zuweisen oder entfernen.", durak:"Stopps", gun:"Tag", yaklasik:"Ca.", yukari:"Nach oben", asagi:"Nach unten", sil:"Entfernen", tahmin:"Entfernungen und Zeiten sind Schätzwerte und können sich ändern." },
  ja: { sureNotu:"営業時間と料金は公式情報をご確認ください", ekle:"＋ルートに追加", rotada:"✓ ルート内", rota:"日ごとのルート", aciklama:"順番・日程の変更、削除ができます。", durak:"か所", gun:"日目", yaklasik:"約", yukari:"上へ", asagi:"下へ", sil:"削除", tahmin:"距離と所要時間は目安で、道路状況により変わります。" },
};

function planMetinleri() { return PLAN_METINLERI[aktifArayuzDili] || PLAN_METINLERI.en; }

function ziyaretSuresiniCevir(sure) {
  if (aktifArayuzDili === "en") return String(sure).replace(/^1 gün$/, "1 day").replace("gün", "days").replace("saat", "hours");
  if (aktifArayuzDili === "de") return String(sure).replace(/^1 gün$/, "1 Tag").replace("gün", "Tage").replace("saat", "Std.");
  if (aktifArayuzDili === "ja") return String(sure).replace("gün", "日").replace("saat", "時間");
  return sure;
}

function konumuAl() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject(new Error(t("location_failed")));
    navigator.geolocation.getCurrentPosition(
      (konum) => resolve({ lat: konum.coords.latitude, lon: konum.coords.longitude, accuracy: Math.round(konum.coords.accuracy || 0) }),
      reject,
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 30000 },
    );
  });
}

const PLAN_KONUM_METINLERI = {
  tr: { sehir: "Şehir belirleniyor...", bulunamadi: "Konum alındı fakat şehir adı belirlenemedi. Şehri elle yazabilirsin." },
  en: { sehir: "Detecting your city...", bulunamadi: "Location received, but the city could not be identified. You can enter it manually." },
  de: { sehir: "Stadt wird ermittelt...", bulunamadi: "Standort empfangen, aber die Stadt wurde nicht erkannt. Du kannst sie manuell eingeben." },
  ja: { sehir: "都市を確認しています…", bulunamadi: "位置情報は取得できましたが都市名を特定できませんでした。手入力できます。" },
};

async function konumdanSehirBul(koordinat) {
  const denetleyici = new AbortController();
  const zamanlayici = setTimeout(() => denetleyici.abort(), 8000);
  try {
    const yanit = await fetch("/konum-sehir", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({lat: koordinat.lat, lon: koordinat.lon}), signal: denetleyici.signal,
    });
    const veri = await yanit.json();
    if (!yanit.ok || !veri.sehir) throw new Error(veri.hata || "Şehir bulunamadı");
    return veri.sehir;
  } finally {
    clearTimeout(zamanlayici);
  }
}

function googleMapsYolTarifiOlustur(yer, ulasim="yuruyus", baslangic=null, sehir="", adlaBul=false) {
  const modlar={"yuruyus":"walking","toplu-tasima":"transit","arac":"driving"};
  const hedef=adlaBul && yer.ad ? `${yer.ad}, ${sehir || "Türkiye"}, Türkiye` : `${yer.lat},${yer.lon}`;
  const params=new URLSearchParams({api:"1",destination:hedef,travelmode:modlar[ulasim]||"walking",dir_action:"navigate"});
  if(baslangic && Number.isFinite(Number(baslangic.lat)) && Number.isFinite(Number(baslangic.lon))) params.set("origin",`${baslangic.lat},${baslangic.lon}`);
  return `https://www.google.com/maps/dir/?${params.toString()}`;
}

function yakinimdaKartlariniCiz(veri) {
  yakinimdaListesi.innerHTML = "";
  const yerler = veri.yerler || [];
  if (!yerler.length) {
    yakinimdaListesi.innerHTML = `<p class="bos-not">${t("no_nearby")}</p>`;
    return;
  }
  yerler.forEach((yer) => {
    const kart = document.createElement("article");
    kart.className = "yakin-yer-karti";
    const ikon = { muze:"🏛", "tarihi-yapi":"⌛", cami:"◈", "ibadet-yeri":"◈", park:"♧", manzara:"◉" }[yer.tur] || "✦";
    kart.innerHTML = `<div class="yakin-yer-ikon">${ikon}</div><div class="yakin-yer-bilgi"><strong>${yer.ad}</strong><span>${yer.tur.replaceAll("-", " ")}</span><small>${yer.mesafe_km < 1 ? Math.round(yer.mesafe_km * 1000) + " m" : yer.mesafe_km + " km"} · ${t("walk_minutes", {minutes: yer.yuruyus_dk})}</small></div>`;
    const aksiyonlar = document.createElement("div");
    aksiyonlar.className = "yakin-yer-aksiyonlari";
    const anlat = document.createElement("button");
    anlat.type = "button"; anlat.className = "evliya-anlat-dugmesi"; anlat.textContent = t("tell_me");
    anlat.addEventListener("click", () => mekanAnlatPenceresiniAc(yer));
    const ekle = document.createElement("button");
    ekle.type = "button"; ekle.textContent = duzenlenenRota.includes(yer.slug) ? t("on_route") : t("add_route");
    ekle.disabled = duzenlenenRota.includes(yer.slug);
    ekle.addEventListener("click", () => { rotayaYerEkle(yer.slug); ekle.textContent = t("on_route"); ekle.disabled = true; });
    const yol = document.createElement("a");
    yol.href = googleMapsYolTarifiOlustur(yer,"yuruyus",sonYakinimdaKonumu,null,false);
    yol.target = "_blank"; yol.rel = "noopener noreferrer"; yol.textContent = t("route_directions");
    aksiyonlar.append(anlat, ekle, yol);
    kart.appendChild(aksiyonlar);
    yakinimdaListesi.appendChild(kart);
  });
}

function mekanAnlatPenceresiniKapat() {
  if (!mekanAnlatOverlay) return;
  mekanAnlatOverlay.classList.remove("gorunur");
  mekanAnlatOverlay.setAttribute("aria-hidden", "true");
  sesDurdur();
}

async function mekanAnlatiminiGetir(mod) {
  if (!aktifMekanAnlatimi) return;
  anlatimModuDugmeleri.forEach((dugme) => dugme.classList.toggle("aktif", dugme.dataset.mod === mod));
  mekanAnlatMetni.textContent = t("story_loading");
  mekanAnlatKaynak.textContent = "";
  mekanAnlatDinle.disabled = true;
  const kontrolci = new AbortController();
  const zamanlayici = setTimeout(() => kontrolci.abort(), 20000);
  try {
    const yanit = await fetch("/mekan-anlat", {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: kontrolci.signal,
      body: JSON.stringify({
        slug: aktifMekanAnlatimi.slug, ad: aktifMekanAnlatimi.ad, tur: aktifMekanAnlatimi.tur,
        mod, dil: aktifArayuzDili, demo_modu: demoModu,
      }),
    });
    const veri = await yanit.json();
    if (!yanit.ok || !veri.reply) throw new Error(t("story_unavailable"));
    sonMekanAnlatimMetni = veri.reply;
    mekanAnlatMetni.textContent = veri.reply;
    const kaynaklar = {
      "yerel-katalog": "Kotasız yerel anlatım · Güncel saat ve ücretleri resmî kaynaktan kontrol et.",
      "demo-genel": "Demo anlatımı · Doğrulanmış ayrıntılı kayıt hazırlanıyor.",
      "yapay-zeka": "Yapay zekâ anlatımı · Güncel ziyaret bilgisi değildir.",
      "yok": "Bu mekân için ayrıntılı anlatım henüz hazırlanmadı.",
      "gecici-hata": "Anlatım servisi şu anda dinleniyor.",
    };
    mekanAnlatKaynak.textContent = kaynaklar[veri.kaynak_turu] || "";
    mekanAnlatDinle.disabled = false;
  } catch (hata) {
    sonMekanAnlatimMetni = "Kervanım biraz soluklanıyor; bu mekânın hikâyesini az sonra yeniden sor, dostum.";
    mekanAnlatMetni.textContent = sonMekanAnlatimMetni;
    mekanAnlatKaynak.textContent = hata.name === "AbortError" ? t("story_timeout") : t("story_unavailable");
    mekanAnlatDinle.disabled = false;
  } finally {
    clearTimeout(zamanlayici);
  }
}

function mekanAnlatPenceresiniAc(yer) {
  aktifMekanAnlatimi = yer;
  sonMekanAnlatimMetni = "";
  mekanAnlatBaslik.textContent = yer.ad;
  mekanAnlatTur.textContent = String(yer.tur || "turistik yer").replaceAll("-", " ");
  mekanAnlatRotayaEkle.disabled = duzenlenenRota.includes(yer.slug);
  mekanAnlatRotayaEkle.textContent = mekanAnlatRotayaEkle.disabled ? t("on_route") : t("add_route");
  mekanAnlatOverlay.classList.add("gorunur");
  mekanAnlatOverlay.setAttribute("aria-hidden", "false");
  mekanAnlatiminiGetir("kisa");
}

if (mekanAnlatKapat) mekanAnlatKapat.addEventListener("click", mekanAnlatPenceresiniKapat);
if (mekanAnlatOverlay) mekanAnlatOverlay.addEventListener("click", (olay) => {
  if (olay.target === mekanAnlatOverlay) mekanAnlatPenceresiniKapat();
});
anlatimModuDugmeleri.forEach((dugme) => dugme.addEventListener("click", () => mekanAnlatiminiGetir(dugme.dataset.mod)));
if (mekanAnlatDinle) mekanAnlatDinle.addEventListener("click", () => {
  if (sonMekanAnlatimMetni) metniSesliOku(sonMekanAnlatimMetni, aktifArayuzDili);
});
if (mekanAnlatRotayaEkle) mekanAnlatRotayaEkle.addEventListener("click", () => {
  if (!aktifMekanAnlatimi) return;
  rotayaYerEkle(aktifMekanAnlatimi.slug);
  mekanAnlatRotayaEkle.textContent = t("on_route");
  mekanAnlatRotayaEkle.disabled = true;
});

async function yakindakileriBul() {
  if (!yakinimdaButonu) return;
  yakinimdaButonu.disabled = true;
  yakinimdaDurum.textContent = demoModu ? t("demo_location") : t("location_wait");
  try {
    const koordinat = demoModu ? {lat:41.0084,lon:28.9784,accuracy:0} : await konumuAl();
    sonYakinimdaKonumu = koordinat;
    yakinimdaDurum.textContent = t("nearby_searching");
    const kontrolci = new AbortController();
    const zamanlayici = setTimeout(() => kontrolci.abort(), 12000);
    const yanit = await fetch("/yakinimda", {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: kontrolci.signal,
      body: JSON.stringify({ ...koordinat, yaricap: Number(yakinimdaYaricap.value), demo_modu: demoModu }),
    });
    clearTimeout(zamanlayici);
    const veri = await yanit.json();
    if (!yanit.ok || veri.hata) throw new Error(veri.hata || t("search_timeout"));
    yakinimdaDurum.textContent = `${t("nearby_summary", {center: veri.merkez.ad, radius: (veri.yaricap / 1000).toFixed(0), count: veri.yerler.length})}${veri.uyari ? " · " + veri.uyari : ""}`;
    yakinimdaKartlariniCiz(veri);
  } catch (hata) {
    const izinHatasi = hata && (hata.code === 1 || hata.name === "NotAllowedError");
    yakinimdaDurum.textContent = izinHatasi
      ? t("location_denied")
      : (hata.name === "AbortError" ? t("search_timeout") : hata.message);
  } finally {
    yakinimdaButonu.disabled = false;
  }
}

if (yakinimdaButonu) yakinimdaButonu.addEventListener("click", yakindakileriBul);

function dakikaYaz(dakika) {
  const saat = Math.floor(dakika / 60), kalan = dakika % 60;
  return saat ? `${saat} ${t("hour_short")} ${kalan ? kalan + " " + t("minute") : ""}`.trim() : `${kalan} ${t("minute")}`;
}

function gitmedenOnceIcerigiOlustur(bilgi) {
  if (!bilgi) return `<p class="gitmeden-once-bos">${t("guide_missing")}</p>`;
  const satirlar = [
    [t("field"), bilgi.alan_tipi], [t("best_time"), bilgi.en_uygun_zaman],
    [t("with_children"), bilgi.cocuklar], [t("accessibility"), bilgi.erisilebilirlik],
    [t("ticket_reservation"), bilgi.rezervasyon], [t("etiquette"), bilgi.adab],
  ];
  return `<div class="gitmeden-once-durum"><span>${t("general_guide")}</span><small>${t("last_review")}: ${bilgi.son_kontrol || "—"}</small></div>
    <dl>${satirlar.map(([etiket,deger])=>`<div><dt>${etiket}</dt><dd>${deger}</dd></div>`).join("")}</dl>
    <p class="gitmeden-once-uyari">${bilgi.guncel_bilgi_notu || ""}</p>
    ${bilgi.resmi_kaynak ? `<a class="gitmeden-once-kaynak" href="${bilgi.resmi_kaynak.url}" target="_blank" rel="noopener noreferrer">${t("official_source")} · ${bilgi.resmi_kaynak.ad} ↗</a>` : ""}`;
}

function gunlukPlaniCiz(plan) {
  aktifGunlukPlan = plan;
  gunlukPlanSonucu.innerHTML = "";
  const ozet = document.createElement("section");
  ozet.className = "gunluk-plan-ozet";
  ozet.innerHTML = `<span>${t("personal_plan")}</span><h3>${plan.baslik}</h3><p>${dakikaYaz(plan.toplam_sure_dk)} · ${t("about")} ${plan.toplam_mesafe_km} km</p><div>${plan.kisisellestirme.map(x => `<em>${x.replaceAll("-", " ")}</em>`).join("")}</div>`;
  if(plan.konum_notu){const k=document.createElement("small");k.className="plan-konum-notu";k.textContent=plan.konum_notu;ozet.appendChild(k);}
  gunlukPlanSonucu.appendChild(ozet);
  const cizelge = document.createElement("div"); cizelge.className = "gunluk-zaman-cizelgesi";
  plan.duraklar.forEach((durak, i) => {
    const kart = document.createElement("article"); kart.className = "gunluk-durak";
    kart.innerHTML = `<div class="gunluk-saat">${durak.saat}</div><div class="gunluk-numara">${i+1}</div><div class="gunluk-durak-govde"><strong>${durak.ad}</strong><span>${durak.tur} · ${durak.sure_dk} ${t("minute")}</span><p>${durak.neden}</p>${i ? `<small>${durak.ulasim.mesafe_km} km · ${t("about")} ${durak.ulasim.sure_dk} ${t("minute")} · ${durak.ulasim.tur.replaceAll("-", " ")}</small>` : ""}</div>`;
    const onceDugme=document.createElement("button"); onceDugme.type="button"; onceDugme.className="gunluk-gitmeden-dugmesi"; onceDugme.textContent=t("before_you_go"); onceDugme.setAttribute("aria-expanded","false");
    const onceIcerik=document.createElement("div"); onceIcerik.className="gunluk-gitmeden-icerik gitmeden-once-icerik"; onceIcerik.innerHTML=gitmedenOnceIcerigiOlustur(durak.gitmeden_once);
    onceDugme.addEventListener("click",()=>{const acik=onceIcerik.classList.toggle("gorunur");onceDugme.setAttribute("aria-expanded",String(acik));onceDugme.textContent=acik?t("close_info"):t("before_you_go");});
    kart.append(onceDugme,onceIcerik);
    cizelge.appendChild(kart);
  });
  gunlukPlanSonucu.appendChild(cizelge);
  const kurtar = document.createElement("section"); kurtar.className="rotami-kurtar";
  kurtar.innerHTML=`<div><strong>${t("rescue_route")}</strong><span>${t("rescue_desc")}</span></div>`;
  const kurtarDugmeleri = document.createElement("div"); kurtarDugmeleri.className="rotami-kurtar-dugmeleri";
  [["yoruldum",t("tired")],["yagmur",t("rain_started")],["aciktim",t("hungry")],["vakit-az",t("time_running")]].forEach(([kosul,etiket])=>{
    const d=document.createElement("button"); d.type="button"; d.textContent=etiket;
    d.addEventListener("click",()=>gunlukPlanIste(kosul,d)); kurtarDugmeleri.appendChild(d);
  });
  kurtar.appendChild(kurtarDugmeleri); gunlukPlanSonucu.appendChild(kurtar);
  if (plan.uyarlama_notu) {
    const not=document.createElement("p"); not.className="rota-uyarlama-notu"; not.textContent=`✦ ${plan.uyarlama_notu}`;
    gunlukPlanSonucu.insertBefore(not, ozet.nextSibling);
  }
  const uyari = document.createElement("p"); uyari.className="gunluk-plan-uyari"; uyari.textContent=plan.uyarilar.join(" "); gunlukPlanSonucu.appendChild(uyari);
  const ac = document.createElement("button"); ac.type="button"; ac.className="plani-haritada-ac"; ac.textContent=t("open_map");
  ac.addEventListener("click", async () => {
    duzenlenenRota = [...plan.rota]; rotaGunleri.clear(); duzenlenenRota.forEach(x => rotaGunleri.set(x, 1));
    if (kartButonu) kartButonu.classList.add("gorunur");
    await rotaPlaniniYenile(); sekmeSec("harita");
  });
  gunlukPlanSonucu.appendChild(ac);
  const baslat = document.createElement("button"); baslat.type="button"; baslat.className="geziyi-baslat-dugmesi"; baslat.textContent=t("start_trip");
  baslat.addEventListener("click", seyahatModunuAc); gunlukPlanSonucu.appendChild(baslat);
  if (seyahatModu && seyahatModu.classList.contains("gorunur")) {
    seyahatDurakIndex=0; seyahatDuraginiCiz();
  }
}

async function gunlukPlanIste(kosul=null, tetikleyen=null) {
  const anaDugme = gunlukPlanFormu.querySelector('[type="submit"]');
  const dugme = tetikleyen || anaDugme; const eskiMetin=dugme.textContent;
  dugme.disabled=true; dugme.textContent=kosul ? t("adjusting_route") : t("evliya_planning");
  try {
    const yanit = await fetch("/gunluk-plan", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
      sehir:planKonumu?.sehir || planSehirGirisi.value, sure:document.getElementById("planSure").value,
      ulasim:document.getElementById("planUlasim").value, ilgi:document.getElementById("planIlgi").value,
      tempo:document.getElementById("planTempo").value, kosul, gecmis, dil:aktifArayuzDili, ...(planKonumu||{}),
    })});
    const plan=await yanit.json(); if(!yanit.ok) throw new Error(plan.hata||t("plan_failed"));
    gunlukPlaniCiz(plan);
    return plan;
  } catch(hata) { gunlukPlanSonucu.innerHTML=`<p class="bos-not">${hata.message}</p>`; }
  finally { dugme.disabled=false; dugme.textContent=eskiMetin; }
}

function seyahatDuraginiCiz() {
  if (!aktifGunlukPlan || !aktifGunlukPlan.duraklar.length) return;
  const toplam=aktifGunlukPlan.duraklar.length;
  if (seyahatDurakIndex >= toplam) {
    seyahatIlerlemeCubugu.style.width="100%"; seyahatIlerlemeMetni.textContent=`${toplam}/${toplam} ${t("stop_completed")}`;
    seyahatDurakAdi.textContent=t("journey_complete"); seyahatDurakTuru.textContent=t("journey_memory");
    seyahatDurakNedeni.textContent=t("journey_finish_note");
    seyahatZiyaretSuresi.textContent=t("completed"); seyahatUlasimBilgisi.textContent=""; seyahatSonraki.innerHTML="";
    seyahatOncesiIcerik.innerHTML=""; seyahatOncesiIcerik.classList.remove("gorunur"); document.querySelector(".seyahat-oncesi-kart").style.display="none";
    [seyahatYolTarifi,seyahatEvliyaAnlat,seyahatGeldim,seyahatGec].forEach(x=>x.style.display="none");
    return;
  }
  [seyahatYolTarifi,seyahatEvliyaAnlat,seyahatGeldim,seyahatGec].forEach(x=>x.style.display="");
  document.querySelector(".seyahat-oncesi-kart").style.display="";
  const durak=aktifGunlukPlan.duraklar[seyahatDurakIndex], sonraki=aktifGunlukPlan.duraklar[seyahatDurakIndex+1];
  seyahatPlanBaslik.textContent=aktifGunlukPlan.baslik; seyahatDurakNo.textContent=String(seyahatDurakIndex+1);
  seyahatDurakAdi.textContent=durak.ad; seyahatDurakTuru.textContent=durak.tur; seyahatDurakNedeni.textContent=durak.neden;
  seyahatZiyaretSuresi.textContent=`◷ ${durak.sure_dk} ${t("minute")} ${t("visit")}`;
  seyahatUlasimBilgisi.textContent=durak.ulasim.mesafe_km ? `${durak.ulasim.mesafe_km} km · ${durak.ulasim.sure_dk} ${t("minute")}` : t("starting_stop");
  seyahatOncesiIcerik.innerHTML=gitmedenOnceIcerigiOlustur(durak.gitmeden_once); seyahatOncesiIcerik.classList.remove("gorunur");
  seyahatOncesiDugmesi.setAttribute("aria-expanded","false"); seyahatOncesiDugmesi.querySelector("b").textContent="+";
  const oncekiDurak=seyahatDurakIndex>0?aktifGunlukPlan.duraklar[seyahatDurakIndex-1]:null;
  const baslangic=seyahatDurakIndex===0 && aktifGunlukPlan.konum_kullanildi ? planKonumu : oncekiDurak;
  seyahatYolTarifi.href=googleMapsYolTarifiOlustur(durak,document.getElementById("planUlasim").value,baslangic,aktifGunlukPlan.sehir,true);
  seyahatIlerlemeCubugu.style.width=`${(seyahatDurakIndex/toplam)*100}%`; seyahatIlerlemeMetni.textContent=`${seyahatDurakIndex+1}/${toplam} · ${toplam-seyahatDurakIndex-1} ${t("stops_left")}`;
  seyahatSonraki.innerHTML=sonraki?`<span>${t("next_stop")}</span><strong>${sonraki.ad}</strong><small>${sonraki.ulasim.mesafe_km} km · ${t("about")} ${sonraki.ulasim.sure_dk} ${t("minute")}</small>`:`<span>${t("final_stop")}</span><strong>${t("final_stop_note")}</strong>`;
  seyahatDurumNotu.textContent=aktifGunlukPlan.uyarlama_notu||"";
}

function seyahatModunuAc() {
  if (!aktifGunlukPlan) return;
  seyahatDurakIndex=0; ziyaretEdilenDuraklar.clear(); seyahatModu.classList.add("gorunur"); seyahatModu.setAttribute("aria-hidden","false");
  document.body.classList.add("seyahat-modu-acik"); seyahatDuraginiCiz();
}
function seyahatModunuKapat() { seyahatModu.classList.remove("gorunur"); seyahatModu.setAttribute("aria-hidden","true"); document.body.classList.remove("seyahat-modu-acik"); sesDurdur(); }
function seyahatSonrakiDuragaGec(geldiMi) {
  const durak=aktifGunlukPlan?.duraklar[seyahatDurakIndex]; if(!durak)return;
  if(geldiMi) ziyaretEdilenDuraklar.add(durak.slug); seyahatDurakIndex+=1;
  seyahatDuraginiCiz(); seyahatDurumNotu.textContent=geldiMi?`${durak.ad} ${t("recorded")}`:`${durak.ad} ${t("skipped")}`;
}

if(seyahatModuKapat)seyahatModuKapat.addEventListener("click",seyahatModunuKapat);
if(seyahatOncesiDugmesi)seyahatOncesiDugmesi.addEventListener("click",()=>{const acik=seyahatOncesiIcerik.classList.toggle("gorunur");seyahatOncesiDugmesi.setAttribute("aria-expanded",String(acik));seyahatOncesiDugmesi.querySelector("b").textContent=acik?"−":"+";});
if(seyahatGeldim)seyahatGeldim.addEventListener("click",()=>seyahatSonrakiDuragaGec(true));
if(seyahatGec)seyahatGec.addEventListener("click",()=>seyahatSonrakiDuragaGec(false));
if(seyahatEvliyaAnlat)seyahatEvliyaAnlat.addEventListener("click",()=>{
  const d=aktifGunlukPlan?.duraklar[seyahatDurakIndex]; if(d) mekanAnlatPenceresiniAc({slug:d.slug,ad:d.ad,tur:d.tur});
});
document.querySelectorAll("[data-seyahat-kosul]").forEach(d=>d.addEventListener("click",async()=>{
  seyahatDurumNotu.textContent=t("adjusting_route"); await gunlukPlanIste(d.dataset.seyahatKosul,d);
}));

if (planKonumButonu) planKonumButonu.addEventListener("click", async () => {
  planKonumButonu.disabled = true; planKonumDurumu.textContent = t("location_wait");
  try {
    const koordinat = await konumuAl();
    const ekMetin = PLAN_KONUM_METINLERI[aktifArayuzDili] || PLAN_KONUM_METINLERI.en;
    planKonumDurumu.textContent = `${t("location_received")} · ${ekMetin.sehir}`;
    try {
      const sehir = await konumdanSehirBul(koordinat);
      planKonumu = {...koordinat, sehir};
      planSehirGirisi.value = sehir;
      planKonumDurumu.textContent = planKonumu.accuracy
        ? `${t("location_received")} · ${sehir} · ${t("accuracy", {value: planKonumu.accuracy})}`
        : `${t("location_received")} · ${sehir}`;
    } catch (_) {
      planKonumu = null;
      planSehirGirisi.value = "";
      planKonumDurumu.textContent = ekMetin.bulunamadi;
    }
  }
  catch (_) { planKonumDurumu.textContent = t("location_failed"); }
  finally { planKonumButonu.disabled = false; }
});

if (planSehirGirisi) planSehirGirisi.addEventListener("input", () => {
  if (!planKonumu) return;
  if (planSehirGirisi.value.trim() !== String(planKonumu.sehir || "").trim()) {
    planKonumu = null;
    planKonumDurumu.textContent = t("location_default");
  }
});

if (gunlukPlanFormu) gunlukPlanFormu.addEventListener("submit", async (olay) => {
  olay.preventDefault();
  await gunlukPlanIste();
});

function mekanDetayiBul(yer) {
  return mekanDetayKayitlari.get(yer) || {
    slug: yer, sehir: yerAdiniYaz(yer), kategori: "kesif", ziyaret_suresi: "2-4 saat", guncel_bilgi: false,
  };
}

function mekanKartiOlustur(yer, medyaOgesi, medyaTuru) {
  const detay = mekanDetayiBul(yer);
  const kart = document.createElement("article");
  kart.className = "mekan-karti";
  kart.dataset.yer = yer;

  const medya = document.createElement("div");
  medya.className = "mekan-kart-medya";
  medya.appendChild(medyaOgesi);

  const govde = document.createElement("div");
  govde.className = "mekan-kart-govde";
  const ust = document.createElement("div");
  ust.className = "mekan-kart-ust";
  ust.innerHTML = `<div><strong>${yerAdiniYaz(yer)}</strong><span>${detay.sehir}</span></div><span class="mekan-sure">◷ ${ziyaretSuresiniCevir(detay.ziyaret_suresi)}</span>`;
  const etiketler = document.createElement("div");
  etiketler.className = "mekan-kart-etiketleri";
  String(detay.kategori || "kesif").split("-").forEach((etiket) => {
    const rozet = document.createElement("span");
    rozet.textContent = etiket;
    etiketler.appendChild(rozet);
  });
  const not = document.createElement("small");
  not.className = "mekan-guncel-not";
  not.textContent = planMetinleri().sureNotu;
  const ekle = document.createElement("button");
  ekle.type = "button";
  ekle.className = "rotaya-ekle-dugmesi";
  ekle.textContent = duzenlenenRota.includes(yer) ? planMetinleri().rotada : planMetinleri().ekle;
  ekle.disabled = duzenlenenRota.includes(yer);
  ekle.addEventListener("click", () => rotayaYerEkle(yer));
  govde.append(ust, etiketler, not, ekle);
  kart.append(medya, govde);
  yerGaleriKayitlari.set(yer, { tur: medyaTuru, element: kart, medya });
  return kart;
}

function mekanKartDugmeleriniGuncelle() {
  yerGaleriKayitlari.forEach((kayit, yer) => {
    const dugme = kayit.element.querySelector(".rotaya-ekle-dugmesi");
    if (!dugme) return;
    const rotada = duzenlenenRota.includes(yer);
    dugme.disabled = rotada;
    dugme.textContent = rotada ? planMetinleri().rotada : planMetinleri().ekle;
  });
}

function medyalariGuncelle(medyalar, mekanDetaylari = []) {
  if (!medyalar || medyalar.length === 0) return;

  (mekanDetaylari || []).forEach((detay) => mekanDetayKayitlari.set(detay.slug, detay));

  medyalar.forEach((ogun) => {
    const yer = ogun.yer;
    if (!yer) return; // genel/joker görseller kalıcı koleksiyona girmez

    const mevcut = yerGaleriKayitlari.get(yer);
    const yukseltmeMi = mevcut && mevcut.tur === "isim_karti" && ogun.tur !== "isim_karti";
    if (mevcut && !yukseltmeMi) return; // zaten var, yükseltme de yok — dokunma

    let oge;
    if (ogun.tur === "video" && ogun.youtube_id) {
      oge = videoOgesiOlustur(ogun.youtube_id, yer);
    } else if (ogun.tur === "gorsel") {
      const urls = ogun.urls || (ogun.url ? [ogun.url] : []);
      if (urls.length === 0) return;
      oge = gorselOgesiOlustur(urls, yer);
    } else {
      oge = document.createElement("div");
      oge.className = "isim-karti";
      const isim = document.createElement("span");
      isim.textContent = yer;
      oge.appendChild(isim);
    }

    if (mevcut) {
      mevcut.medya.innerHTML = "";
      mevcut.medya.appendChild(oge); // isim kartını yerinde gerçek görsele yükselt
      mevcut.tur = ogun.tur;
    } else {
      const bosNot = defterMedya.querySelector(".bos-not");
      if (bosNot) bosNot.remove();
      defterMedya.prepend(mekanKartiOlustur(yer, oge, ogun.tur)); // en yeni en üstte
    }
  });
  mekanKartDugmeleriniGuncelle();
}

// ---- Anlatı sahnesi: Evliya'nın anlatımıyla akan görsel/video -------------
// En son cevabın medyası (video varsa önce video, ardından aynı yerin
// fotoğrafları) tek bir "kare" akışına düzleştirilir ve otomatik ilerler;
// altyazı şeridi TTS ile senkron güncellenir (bkz. metniSesliOku çağrısı).

const ANLATI_FOTO_SURESI_MS = 4500;
const ANLATI_VIDEO_SURESI_MS = 9000;

let anlatiKareleri = [];
let anlatiKareIndeksi = 0;
let anlatiIlerletmeZamanlayici = null;

function anlatiKarelerineDonustur(medyalar) {
  const kareler = [];
  (medyalar || []).forEach((ogun) => {
    if (ogun.tur === "video" && ogun.youtube_id) {
      kareler.push({ tur: "video", youtubeId: ogun.youtube_id, yer: ogun.yer });
      (ogun.urls || []).forEach((url) => kareler.push({ tur: "foto", url, yer: ogun.yer }));
    } else if (ogun.tur === "gorsel") {
      const urls = ogun.urls || (ogun.url ? [ogun.url] : []);
      urls.forEach((url) => kareler.push({ tur: "foto", url, yer: ogun.yer }));
    }
  });
  return kareler;
}

function anlatiKareyiCiz(kare) {
  if (!anlatiMedya) return;

  if (!kare) {
    anlatiMedya.innerHTML = "";
    anlatiMedya.classList.add("bos");
    return;
  }
  anlatiMedya.classList.remove("bos");

  if (kare.tur === "video") {
    anlatiMedya.innerHTML = "";
    const iframe = document.createElement("iframe");
    const id = encodeURIComponent(kare.youtubeId);
    iframe.src = `https://www.youtube.com/embed/${id}?autoplay=1&mute=1&loop=1&playlist=${id}&controls=0`;
    iframe.title = kare.yer ? `${kare.yer} tanıtım videosu` : "Türkiye tanıtım videosu";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.frameBorder = "0";
    anlatiMedya.appendChild(iframe);
    return;
  }

  // foto: önceki kare(ler) varsa üstüne çapraz geçişle yenisini ekle; video
  // gösteriliyorduysa önce temizle (video<->foto arası sert kesme yeterli).
  if (anlatiMedya.querySelector("iframe")) anlatiMedya.innerHTML = "";
  const eskiImgler = [...anlatiMedya.querySelectorAll("img")];

  const img = document.createElement("img");
  img.src = kare.url;
  img.alt = kare.yer ? `${kare.yer} — Türkiye'den bir kare` : "Türkiye'den bir kare";
  anlatiMedya.appendChild(img);
  // rAF yerine senkron reflow zorlaması (bkz. anlatiMetniGoster) — arka
  // plandaki/gizli sekmelerde de crossfade güvenilir tetiklenir.
  void img.offsetWidth;
  img.classList.add("aktif");
  setTimeout(() => eskiImgler.forEach((eski) => eski.remove()), 1300);
}

function anlatiIlerletmeyiKur() {
  if (anlatiIlerletmeZamanlayici) {
    clearTimeout(anlatiIlerletmeZamanlayici);
    anlatiIlerletmeZamanlayici = null;
  }
  if (anlatiKareleri.length <= 1) return;
  const kare = anlatiKareleri[anlatiKareIndeksi];
  const sure = kare && kare.tur === "video" ? ANLATI_VIDEO_SURESI_MS : ANLATI_FOTO_SURESI_MS;
  anlatiIlerletmeZamanlayici = setTimeout(() => {
    anlatiKareIndeksi = (anlatiKareIndeksi + 1) % anlatiKareleri.length;
    anlatiKareyiCiz(anlatiKareleri[anlatiKareIndeksi]);
    anlatiIlerletmeyiKur();
  }, sure);
}

function anlatiSahneyiGuncelle(medyalar) {
  if (anlatiIlerletmeZamanlayici) {
    clearTimeout(anlatiIlerletmeZamanlayici);
    anlatiIlerletmeZamanlayici = null;
  }
  anlatiKareleri = anlatiKarelerineDonustur(medyalar);
  anlatiKareIndeksi = 0;
  anlatiKareyiCiz(anlatiKareleri[0] || null);
  anlatiIlerletmeyiKur();
}

// requestAnimationFrame kullanılmıyor: arka plandaki/gizli sekmelerde rAF
// callback'leri tarayıcı tarafından ertelenebiliyor (throttle), bu da
// altyazının hiç güncellenmemesine yol açabilir. Bunun yerine senkron bir
// reflow zorlaması (offsetWidth okuma) ile CSS geçişi tetiklenir — sekme
// arka planda olsa bile metin her zaman hemen güncellenir.
function anlatiMetniGoster(metin) {
  if (!anlatiMetniEl) return;
  anlatiMetniEl.textContent = metin;
  anlatiMetniEl.classList.remove("belirdi");
  void anlatiMetniEl.offsetWidth;
  anlatiMetniEl.classList.add("belirdi");
}

// ---- Rota haritası (Leaflet) -----------------------------------------------

let haritaOrnegi = null;
let haritaCizimZamanlayici = null;
let sonHaritaNoktalari = [];

function haritaBoyutunuYenile() {
  if (!haritaOrnegi || !defterHarita || !defterHarita.offsetParent) return;
  [0, 120, 400].forEach((gecikme) => setTimeout(() => {
    if (!haritaOrnegi || !defterHarita.offsetParent) return;
    haritaOrnegi.invalidateSize({ pan: false });
    if (sonHaritaNoktalari.length) haritaOrnegi.fitBounds(sonHaritaNoktalari, { padding: [36, 36], maxZoom: 16 });
  }, gecikme));
}

function haritayiTemizle() {
  if (haritaCizimZamanlayici) {
    clearInterval(haritaCizimZamanlayici);
    haritaCizimZamanlayici = null;
  }
  if (haritaOrnegi) {
    haritaOrnegi.remove();
    haritaOrnegi = null;
  }
  sonHaritaNoktalari = [];
  defterHarita.innerHTML = "";
  defterHarita.classList.remove("gorunur");
}

function haritayiGuncelle(rotaKoordinatlari, rotaDetaylari = []) {
  haritayiTemizle();

  if (!rotaKoordinatlari || rotaKoordinatlari.length === 0 || typeof L === "undefined") {
    return;
  }

  // Harita sekmesi yalnızca gerçek bir rota geldiğinde açılır. İlk kez
  // açılıyorsa (önceden devre dışıydı) kullanıcıyı otomatik o sekmeye
  // geçiriyoruz; sonraki rota güncellemelerinde mevcut sekme seçimine
  // dokunmuyoruz (kullanıcı başka bir sekmeye bakıyor olabilir).
  const haritaSekmeDugmesi = document.querySelector('.defter-sekme-dugmesi[data-sekme="harita"]');
  const ilkRotaMi = haritaSekmeDugmesi && haritaSekmeDugmesi.disabled;
  if (haritaSekmeDugmesi) haritaSekmeDugmesi.disabled = false;
  if (ilkRotaMi) sekmeSec("harita");

  defterHarita.classList.add("gorunur");

  haritaOrnegi = L.map(defterHarita, { attributionControl: true });

  // Anahtar gerektirmeyen standart OpenStreetMap karoları. CARTO Voyager
  // anahtarsız isteklerde "API KEY REQUIRED" damgası göstermeye başladığı
  // için doğrudan OSM kullanıyoruz.
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap katkıda bulunanlar",
  }).addTo(haritaOrnegi);

  const noktalar = rotaKoordinatlari.map((n) => [n.lat, n.lon]);
  sonHaritaNoktalari = noktalar;

  rotaKoordinatlari.forEach((nokta, i) => {
    const simge = L.divIcon({
      className: "rota-isaretci-simge",
      html: String(i + 1),
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });
    const oncekiAyak = rotaDetaylari.find((ayak) => ayak.varis === nokta.yer);
    const sonrakiAyak = rotaDetaylari.find((ayak) => ayak.baslangic === nokta.yer);
    const ayrinti = sonrakiAyak || oncekiAyak;
    const popupMetni = ayrinti
      ? `<strong>${yerAdiniYaz(nokta.yer)}</strong><br>${ayrinti.yaklasik_km} km · ${ayrinti.tahmini_sure}<br>${ayrinti.ulasim}`
      : `<strong>${yerAdiniYaz(nokta.yer)}</strong>`;
    L.marker([nokta.lat, nokta.lon], { icon: simge })
      .addTo(haritaOrnegi)
      .bindTooltip(yerAdiniYaz(nokta.yer), {
        permanent: true,
        direction: i % 2 === 0 ? "left" : "right",
        offset: [i % 2 === 0 ? -10 : 10, 0],
        className: "rota-yer-etiketi",
      })
      .bindPopup(popupMetni);
  });

  // Her iki durağın ortasına mesafe rozeti koy. Rozete tıklanınca süre ve
  // önerilen ulaşım şekli de görünür; böylece haritadan ayrılmak gerekmez.
  rotaDetaylari.forEach((ayak) => {
    const baslangic = rotaKoordinatlari.find((n) => n.yer === ayak.baslangic);
    const varis = rotaKoordinatlari.find((n) => n.yer === ayak.varis);
    if (!baslangic || !varis) return;
    const orta = [(baslangic.lat + varis.lat) / 2, (baslangic.lon + varis.lon) / 2];
    const mesafeSimge = L.divIcon({
      className: "rota-mesafe-simge",
      html: `<span>≈ ${ayak.yaklasik_km} km</span>`,
      iconSize: [92, 24],
      iconAnchor: [46, 12],
    });
    L.marker(orta, { icon: mesafeSimge, interactive: true, zIndexOffset: 500 })
      .addTo(haritaOrnegi)
      .bindPopup(`<strong>${yerAdiniYaz(ayak.baslangic)} → ${yerAdiniYaz(ayak.varis)}</strong><br>Yaklaşık ${ayak.yaklasik_km} km · ${ayak.tahmini_sure}<br>${ayak.ulasim}`);
  });

  // Aynı şehirdeki yakın duraklar il/ülke ölçeğinde kalmasın; sokak ve yer
  // adları okunabilecek seviyeye kadar yaklaşabilsin.
  haritaOrnegi.fitBounds(noktalar, { padding: [36, 36], maxZoom: 16 });

  // Noktalar arasını sırayla, ~1.5 sn'de çizerek bağla. Açık haritada net
  // görünsün diye beyaz "halo" altına, koyu kehribar çizgi üstüne çizilir.
  if (noktalar.length > 1) {
    const cizgiHalo = L.polyline([noktalar[0]], { color: "#ffffff", weight: 7, opacity: 0.8 }).addTo(haritaOrnegi);
    const cizgi = L.polyline([noktalar[0]], { color: "#b5651d", weight: 3.5, opacity: 0.95 }).addTo(haritaOrnegi);
    let i = 1;
    const adimSuresi = ROTA_CIZIM_SURESI_MS / (noktalar.length - 1);
    haritaCizimZamanlayici = setInterval(() => {
      const dilim = noktalar.slice(0, i + 1);
      cizgiHalo.setLatLngs(dilim);
      cizgi.setLatLngs(dilim);
      i += 1;
      if (i >= noktalar.length) {
        clearInterval(haritaCizimZamanlayici);
        haritaCizimZamanlayici = null;
      }
    }, adimSuresi);
  }

  // Konteyner submit anında "display:none"dan yeni görünür olduğu için
  // Leaflet'in boyutu doğru hesaplaması adına bir tık gecikmeli invalidate.
  haritaBoyutunuYenile();
}

window.addEventListener("resize", haritaBoyutunuYenile);
window.addEventListener("focus", haritaBoyutunuYenile);
window.addEventListener("pageshow", haritaBoyutunuYenile);
document.addEventListener("visibilitychange", () => { if (!document.hidden) haritaBoyutunuYenile(); });
if (typeof ResizeObserver !== "undefined" && defterHarita) {
  new ResizeObserver(() => haritaBoyutunuYenile()).observe(defterHarita);
}

function lezzetKartiOlustur(ogun) {
  const kart = document.createElement("div");
  kart.className = "lezzet-karti";

  if (ogun.tur === "gorsel") {
    const img = document.createElement("img");
    img.src = ogun.url;
    img.alt = ogun.lezzet || "";
    kart.appendChild(img);
  } else {
    kart.classList.add("lezzet-isim-karti");
  }

  const etiket = document.createElement("span");
  etiket.textContent = ogun.lezzet || "";
  kart.appendChild(etiket);

  return kart;
}

// Yer galerisiyle aynı mantık: lezzet şeridi de birikir, isim kartından
// gerçek görsele yükselir.
const lezzetGaleriKayitlari = new Map();
let lezzetSeridi = null;

function lezzetleriGuncelle(lezzetMedyalari) {
  if (!lezzetMedyalari || lezzetMedyalari.length === 0) return;

  if (!lezzetSeridi) {
    defterLezzet.innerHTML = "";
    const baslik = document.createElement("h3");
    baslik.textContent = t("must_taste");
    defterLezzet.appendChild(baslik);
    lezzetSeridi = document.createElement("div");
    lezzetSeridi.className = "lezzet-serit";
    defterLezzet.appendChild(lezzetSeridi);
  }

  lezzetMedyalari.forEach((ogun) => {
    const lezzet = ogun.lezzet;
    if (!lezzet) return;

    const mevcut = lezzetGaleriKayitlari.get(lezzet);
    const yukseltmeMi = mevcut && mevcut.tur === "isim_karti" && ogun.tur !== "isim_karti";
    if (mevcut && !yukseltmeMi) return;

    const kart = lezzetKartiOlustur(ogun);
    if (mevcut) {
      mevcut.element.replaceWith(kart);
    } else {
      lezzetSeridi.prepend(kart);
    }
    lezzetGaleriKayitlari.set(lezzet, { tur: ogun.tur, element: kart });
  });

  defterLezzet.classList.add("gorunur");
}

function gezginProfiliGuncelle(profil) {
  gezginProfili.innerHTML = "";
  if (!profil) return;

  const baslik = document.createElement("h3");
  baslik.textContent = t("traveler_profile");
  gezginProfili.appendChild(baslik);

  if (profil.etiketler && profil.etiketler.length > 0) {
    const etiketSatiri = document.createElement("div");
    etiketSatiri.className = "profil-etiketleri";
    profil.etiketler.forEach((etiket) => {
      const span = document.createElement("span");
      span.className = "profil-etiket";
      span.textContent = etiket;
      etiketSatiri.appendChild(span);
    });
    gezginProfili.appendChild(etiketSatiri);
  }

  const aciklama = document.createElement("p");
  aciklama.className = "profil-aciklama";
  aciklama.textContent = profil.aciklama || "";
  gezginProfili.appendChild(aciklama);
}

async function rotaPlaniniYenile() {
  if (duzenlenenRota.length === 0) {
    duzenlenenRotaDetaylari = [];
    rotaGuncelle([], [], true);
    haritayiTemizle();
    mekanKartDugmeleriniGuncelle();
    return;
  }
  try {
    const yanit = await fetch("/rota-detay", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rota: duzenlenenRota, dil: aktifArayuzDili }),
    });
    const veri = await yanit.json();
    duzenlenenRotaDetaylari = veri.rota_detaylari || [];
    rotaGuncelle(duzenlenenRota, duzenlenenRotaDetaylari, true);
    haritayiGuncelle(veri.rota_koordinatlari || [], duzenlenenRotaDetaylari);
    if (sonRotaVerisi) sonRotaVerisi.rota = [...duzenlenenRota];
  } catch (hata) {
    console.error("Rota yenilenemedi:", hata);
    rotaGuncelle(duzenlenenRota, duzenlenenRotaDetaylari, true);
  }
  mekanKartDugmeleriniGuncelle();
}

function rotayaYerEkle(yer) {
  if (!yer || duzenlenenRota.includes(yer)) return;
  duzenlenenRota.push(yer);
  rotaGunleri.set(yer, Math.max(1, ...rotaGunleri.values(), 1));
  if (!sonRotaVerisi) sonRotaVerisi = { rota: [...duzenlenenRota], medyalar: [], panel: { dil: "tr", temalar: [] } };
  if (kartButonu) kartButonu.classList.add("gorunur");
  rotaPlaniniYenile();
}

function rotaDuraginiTasi(index, yon) {
  const hedef = index + yon;
  if (hedef < 0 || hedef >= duzenlenenRota.length) return;
  [duzenlenenRota[index], duzenlenenRota[hedef]] = [duzenlenenRota[hedef], duzenlenenRota[index]];
  rotaPlaniniYenile();
}

function rotaDuraginiSil(index) {
  const [silinen] = duzenlenenRota.splice(index, 1);
  rotaGunleri.delete(silinen);
  rotaPlaniniYenile();
}

function rotaGuncelle(rota, detaylar = [], dahiliGuncelleme = false) {
  const metinler = planMetinleri();
  defterRota.innerHTML = "";
  if (!rota || rota.length === 0) {
    if (!dahiliGuncelleme) {
      duzenlenenRota = [];
      duzenlenenRotaDetaylari = [];
      rotaGunleri.clear();
    }
    return;
  }

  if (!dahiliGuncelleme) {
    duzenlenenRota = [...new Set(rota)];
    duzenlenenRotaDetaylari = detaylar || [];
    const gunSayisi = Math.max(1, Number(yolculukSecimleri && yolculukSecimleri.gun) || Math.min(3, duzenlenenRota.length));
    duzenlenenRota.forEach((yer, i) => {
      if (!rotaGunleri.has(yer)) rotaGunleri.set(yer, Math.min(gunSayisi, i + 1));
    });
  }

  const baslikSatiri = document.createElement("div");
  baslikSatiri.className = "rota-baslik-satiri";
  baslikSatiri.innerHTML = `<div><h3>${metinler.rota}</h3><small>${metinler.aciklama}</small></div><span>${duzenlenenRota.length} ${metinler.durak}</span>`;
  defterRota.appendChild(baslikSatiri);

  const liste = document.createElement("ul");
  liste.className = "rota-listesi";
  duzenlenenRota.forEach((yer, i) => {
    const li = document.createElement("li");
    li.dataset.gun = String(rotaGunleri.get(yer) || 1);
    const durak = document.createElement("div");
    durak.className = "rota-durak";
    const sira = document.createElement("span");
    sira.className = "rota-sira";
    sira.textContent = i + 1;
    const ad = document.createElement("strong");
    ad.textContent = yerAdiniYaz(yer);
    const adKutusu = document.createElement("div");
    adKutusu.className = "rota-durak-adi";
    const detay = mekanDetayiBul(yer);
    adKutusu.appendChild(ad);
    const alt = document.createElement("small");
    alt.textContent = `${detay.sehir} · ${ziyaretSuresiniCevir(detay.ziyaret_suresi)}`;
    adKutusu.appendChild(alt);
    const gun = document.createElement("select");
    gun.className = "rota-gun-secimi";
    gun.setAttribute("aria-label", `${yerAdiniYaz(yer)} günü`);
    const enFazlaGun = Math.max(3, ...rotaGunleri.values());
    for (let g = 1; g <= Math.min(7, enFazlaGun); g += 1) {
      const secenek = document.createElement("option");
      secenek.value = String(g); secenek.textContent = `${g}. ${metinler.gun}`;
      secenek.selected = g === (rotaGunleri.get(yer) || 1);
      gun.appendChild(secenek);
    }
    gun.addEventListener("change", () => { rotaGunleri.set(yer, Number(gun.value)); rotaGuncelle(duzenlenenRota, duzenlenenRotaDetaylari, true); });
    const aksiyonlar = document.createElement("div");
    aksiyonlar.className = "rota-durak-aksiyonlari";
    [["↑", -1, metinler.yukari], ["↓", 1, metinler.asagi]].forEach(([simge, yon, baslik]) => {
      const dugme = document.createElement("button");
      dugme.type = "button"; dugme.textContent = simge; dugme.title = baslik;
      dugme.disabled = (yon === -1 && i === 0) || (yon === 1 && i === duzenlenenRota.length - 1);
      dugme.addEventListener("click", () => rotaDuraginiTasi(i, yon));
      aksiyonlar.appendChild(dugme);
    });
    const sil = document.createElement("button");
    sil.type = "button"; sil.textContent = "×"; sil.title = metinler.sil; sil.className = "rota-sil";
    sil.addEventListener("click", () => rotaDuraginiSil(i));
    aksiyonlar.appendChild(sil);
    durak.append(sira, adKutusu, gun, aksiyonlar);
    li.appendChild(durak);

    const ayak = detaylar.find((detay) => detay.baslangic === yer && detay.varis === duzenlenenRota[i + 1]);
    if (ayak) {
      const yol = document.createElement("div");
      yol.className = "rota-yolculuk-ayagi";
      yol.innerHTML = `<span class="rota-yol-cizgisi">↓</span><div><strong>${metinler.yaklasik} ${ayak.yaklasik_km} km · ${ayak.tahmini_sure}</strong><small>${ayak.ulasim}</small></div>`;
      li.appendChild(yol);
    }
    liste.appendChild(li);
  });
  const not = document.createElement("p");
  not.className = "rota-tahmin-notu";
  not.textContent = metinler.tahmin;
  defterRota.appendChild(liste);
  defterRota.appendChild(not);
  mekanKartDugmeleriniGuncelle();
}

// ---- Paylaşılabilir rota kartı (Canvas) ------------------------------------
// html2canvas gibi bir dış kütüphane gerekmez; kart doğrudan <canvas> 2D API
// ile çiziliyor. Tüm görseller kendi /assets/ sunucumuzdan geldiği için
// same-origin'dir, bu yüzden canvas.toDataURL() CORS'a takılmadan çalışır.

let sonRotaVerisi = null; // { rota, medyalar, panel } — en son rota içeren cevap

const KART_METINLERI = {
  tr: {
    baslik: (ilgi) => `Evliya Çelebi'nin ${ilgi} için önerdiği rota`,
    not: "goturkiye.com'dan ilhamla",
    indir: "Kartı İndir",
    kapat: "Kapat",
    varsayilanIlgi: "keşif",
    eksikGorselNotu: "Bazı durakların görseli hâlâ hazırlanıyor — birkaç dakika sonra tekrar sorup kartı yeniden oluşturursan daha eksiksiz olur.",
  },
  en: {
    baslik: (ilgi) => `Evliya Çelebi's route for ${ilgi} lovers`,
    not: "inspired via goturkiye.com",
    indir: "Download Card",
    kapat: "Close",
    varsayilanIlgi: "discovery",
    eksikGorselNotu: "Photos for some stops are still being prepared — ask again in a few minutes and remake the card for a more complete result.",
  },
  de: {
    baslik: (ilgi) => `Evliya Çelebis Route für ${ilgi}-Liebhaber`,
    not: "inspiriert von goturkiye.com",
    indir: "Karte herunterladen",
    kapat: "Schließen",
    varsayilanIlgi: "Entdeckung",
    eksikGorselNotu: "Fotos für einige Stopps werden noch vorbereitet — frag in ein paar Minuten erneut und erstelle die Karte neu für ein vollständigeres Ergebnis.",
  },
  ja: {
    baslik: (ilgi) => `エヴリヤ・チェレビが薦める${ilgi}の旅`,
    not: "goturkiye.com からの着想",
    indir: "カードを保存",
    kapat: "閉じる",
    varsayilanIlgi: "発見",
    eksikGorselNotu: "一部の場所の写真はまだ準備中です — 数分後にもう一度尋ねてカードを作り直すと、より完全になります。",
  },
};

const KART_TEMA_ADLARI = {
  tr: { tarih: "tarih", doga: "doğa", yemek: "yemek", deniz: "deniz", sanat: "sanat", sakin: "huzur", macera: "macera", aile: "aile" },
  en: { tarih: "history", doga: "nature", yemek: "food", deniz: "the sea", sanat: "art", sakin: "tranquility", macera: "adventure", aile: "family" },
  de: { tarih: "Geschichte", doga: "Natur", yemek: "Essen", deniz: "das Meer", sanat: "Kunst", sakin: "Ruhe", macera: "Abenteuer", aile: "Familie" },
  ja: { tarih: "歴史", doga: "自然", yemek: "グルメ", deniz: "海", sanat: "芸術", sakin: "静けさ", macera: "冒険", aile: "家族" },
};

function kartMetinleriGetir(dilKodu) {
  return KART_METINLERI[dilKodu] || KART_METINLERI.en;
}

function kartResimYukle(url) {
  return new Promise((resolve) => {
    if (!url) {
      resolve(null);
      return;
    }
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => resolve(null);
    img.src = url;
  });
}

function yuvarlatilmisDikdortgenCiz(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

function kartKelimeKaydirarakYaz(ctx, metin, x, y, maxGenislik, satirYuksekligi) {
  const kelimeler = metin.split(" ");
  let satir = "";
  let mevcutY = y;
  let satirSayisi = 1;
  for (let i = 0; i < kelimeler.length; i++) {
    const denemeSatir = satir + kelimeler[i] + " ";
    if (ctx.measureText(denemeSatir).width > maxGenislik && i > 0) {
      ctx.fillText(satir.trim(), x, mevcutY);
      satir = kelimeler[i] + " ";
      mevcutY += satirYuksekligi;
      satirSayisi += 1;
    } else {
      satir = denemeSatir;
    }
  }
  ctx.fillText(satir.trim(), x, mevcutY);
  return satirSayisi;
}

async function rotaKartiCiz(canvas, rotaVerisi) {
  const { rota, medyalar, panel } = rotaVerisi;
  const dilKodu = (panel && panel.dil) || "en";
  const metinler = kartMetinleriGetir(dilKodu);
  const temaAdlari = KART_TEMA_ADLARI[dilKodu] || KART_TEMA_ADLARI.en;
  const temalar = (panel && panel.temalar) || [];
  const ilgi = temalar.length > 0 ? (temaAdlari[temalar[0]] || temalar[0]) : metinler.varsayilanIlgi;

  const genislik = 1000;
  const yukseklik = 1250;
  canvas.width = genislik;
  canvas.height = yukseklik;
  const ctx = canvas.getContext("2d");

  // Zemin
  const zeminGradyan = ctx.createLinearGradient(0, 0, 0, yukseklik);
  zeminGradyan.addColorStop(0, "#241c15");
  zeminGradyan.addColorStop(1, "#14100c");
  ctx.fillStyle = zeminGradyan;
  ctx.fillRect(0, 0, genislik, yukseklik);

  // Dış kehribar çerçeve (çift çizgi, zarif)
  ctx.strokeStyle = "#d9a04b";
  ctx.lineWidth = 4;
  yuvarlatilmisDikdortgenCiz(ctx, 24, 24, genislik - 48, yukseklik - 48, 24);
  ctx.stroke();
  ctx.strokeStyle = "rgba(217, 160, 75, 0.4)";
  ctx.lineWidth = 1.5;
  yuvarlatilmisDikdortgenCiz(ctx, 36, 36, genislik - 72, yukseklik - 72, 18);
  ctx.stroke();

  // Evliya minyatürü (yuvarlak, sol üst köşe)
  const avatarResmi = await kartResimYukle("/assets/evliya-avatar.jpg");
  const avatarYaricap = 70;
  const avatarMerkezX = 130;
  const avatarMerkezY = 145;
  if (avatarResmi) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(avatarMerkezX, avatarMerkezY, avatarYaricap, 0, Math.PI * 2);
    ctx.closePath();
    ctx.clip();
    ctx.drawImage(avatarResmi, avatarMerkezX - avatarYaricap, avatarMerkezY - avatarYaricap, avatarYaricap * 2, avatarYaricap * 2);
    ctx.restore();
  }
  ctx.strokeStyle = "#d9a04b";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(avatarMerkezX, avatarMerkezY, avatarYaricap, 0, Math.PI * 2);
  ctx.stroke();

  // Başlık (Evliya'nın sağında, kelime kaydırmalı)
  ctx.fillStyle = "#d9a04b";
  ctx.font = "bold 38px Georgia, 'Yu Mincho', serif";
  ctx.textBaseline = "top";
  const baslikX = avatarMerkezX + avatarYaricap + 30;
  const baslikGenislik = genislik - baslikX - 60;
  kartKelimeKaydirarakYaz(ctx, metinler.baslik(ilgi), baslikX, 75, baslikGenislik, 46);

  // Üst ayırıcı
  ctx.strokeStyle = "rgba(217, 160, 75, 0.5)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(60, 250);
  ctx.lineTo(genislik - 60, 250);
  ctx.stroke();

  // Rota yeri -> ilk görsel url eşlemesi
  const medyaHaritasi = {};
  (medyalar || []).forEach((m) => {
    if (m.yer) medyaHaritasi[m.yer] = (m.urls && m.urls[0]) || m.url || null;
  });

  const gorulecekRota = (rota || []).slice(0, 6);
  const satirYuksekligi = 130;
  let satirY = 290;
  let eksikGorselSayisi = 0;

  for (let i = 0; i < gorulecekRota.length; i++) {
    const yer = gorulecekRota[i];
    const gorsel = await kartResimYukle(medyaHaritasi[yer]);
    if (!gorsel) eksikGorselSayisi += 1;

    // Numara rozeti
    ctx.fillStyle = "#d9a04b";
    ctx.beginPath();
    ctx.arc(90, satirY + 48, 26, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#201408";
    ctx.font = "bold 24px Georgia, serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(String(i + 1), 90, satirY + 49);
    ctx.textAlign = "left";
    ctx.textBaseline = "top";

    // Küçük görsel (yuvarlatılmış kare, cover-benzeri kırpma)
    const gorselX = 140;
    const gorselBoyut = 96;
    yuvarlatilmisDikdortgenCiz(ctx, gorselX, satirY, gorselBoyut, gorselBoyut, 12);
    if (gorsel) {
      ctx.save();
      ctx.clip();
      const olcek = Math.max(gorselBoyut / gorsel.width, gorselBoyut / gorsel.height);
      const cizilenGenislik = gorsel.width * olcek;
      const cizilenYukseklik = gorsel.height * olcek;
      ctx.drawImage(
        gorsel,
        gorselX - (cizilenGenislik - gorselBoyut) / 2,
        satirY - (cizilenYukseklik - gorselBoyut) / 2,
        cizilenGenislik,
        cizilenYukseklik,
      );
      ctx.restore();
    } else {
      ctx.fillStyle = "#2a2015";
      ctx.fill();
    }
    ctx.strokeStyle = "rgba(217, 160, 75, 0.5)";
    ctx.lineWidth = 1.5;
    yuvarlatilmisDikdortgenCiz(ctx, gorselX, satirY, gorselBoyut, gorselBoyut, 12);
    ctx.stroke();

    // Yer adı
    ctx.fillStyle = "#f0e4d0";
    ctx.font = "32px Georgia, 'Yu Mincho', serif";
    const yerAdi = yer.charAt(0).toUpperCase() + yer.slice(1).replace(/-/g, " ");
    ctx.fillText(yerAdi, gorselX + gorselBoyut + 24, satirY + gorselBoyut / 2 - 16);

    satirY += satirYuksekligi;
  }

  // Alt ayırıcı + goturkiye notu
  const altY = yukseklik - 90;
  ctx.strokeStyle = "rgba(217, 160, 75, 0.5)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(60, altY);
  ctx.lineTo(genislik - 60, altY);
  ctx.stroke();

  ctx.fillStyle = "#b8a888";
  ctx.font = "italic 22px Georgia, serif";
  ctx.textAlign = "center";
  ctx.fillText(metinler.not, genislik / 2, altY + 26);
  ctx.textAlign = "left";

  return { eksikGorselSayisi };
}

if (kartButonu) {
  kartButonu.addEventListener("click", async () => {
    if (!sonRotaVerisi) return;

    kartOverlay.classList.add("gorunur");
    kartYukleniyor.style.display = "block";
    kartCanvas.style.display = "none";
    if (kartEksikNotu) kartEksikNotu.classList.remove("gorunur");

    const dilKodu = (sonRotaVerisi.panel && sonRotaVerisi.panel.dil) || "en";
    const metinler = kartMetinleriGetir(dilKodu);
    kartIndirButonu.textContent = metinler.indir;
    kartKapatButonu.textContent = metinler.kapat;

    try {
      const { eksikGorselSayisi } = await rotaKartiCiz(kartCanvas, sonRotaVerisi);
      kartYukleniyor.style.display = "none";
      kartCanvas.style.display = "block";
      if (kartEksikNotu) {
        kartEksikNotu.textContent = eksikGorselSayisi > 0 ? metinler.eksikGorselNotu : "";
        kartEksikNotu.classList.toggle("gorunur", eksikGorselSayisi > 0);
      }
    } catch (hata) {
      console.error("Rota kartı çizilemedi:", hata);
      kartYukleniyor.textContent = "Kart oluşturulamadı, tekrar dener misin?";
    }
  });
}

if (kartIndirButonu) {
  kartIndirButonu.addEventListener("click", () => {
    const baglanti = document.createElement("a");
    baglanti.download = "evliya-celebi-rota-karti.png";
    baglanti.href = kartCanvas.toDataURL("image/png");
    document.body.appendChild(baglanti);
    baglanti.click();
    baglanti.remove();
  });
}

if (kartKapatButonu) {
  kartKapatButonu.addEventListener("click", () => {
    kartOverlay.classList.remove("gorunur");
  });
}

if (kartOverlay) {
  kartOverlay.addEventListener("click", (olay) => {
    if (olay.target === kartOverlay) kartOverlay.classList.remove("gorunur");
  });
}

// ---- Seslendirme (TTS) ----------------------------------------------------
// Prototip için tarayıcının kendi Web Speech API'si kullanılıyor (ücretsiz,
// anahtar gerekmez). İleride ElevenLabs/Gemini TTS gibi bir servise geçmek
// istenirse yalnızca metniSesliOku fonksiyonunun içini değiştirmek yeterli —
// çağıran yerler (submit handler, ses düğmesi) aynı kalabilir.

const DIL_KODU_ESLESTIRME = { en: "en", de: "de", ja: "ja", tr: "tr" };
const ERKEK_SES_IPUCLARI = /\b(male|erkek|david|mark|daniel|fred|alex|guy|george|thomas|yannick|jorge|ryo|takumi)\b/i;

// Yaşlı, bilge bir gezginin tonu: hafif yavaş, hafif kalın.
const SES_HIZI = 0.9;
const SES_PERDESI = 0.85;

let sesAcik = localStorage.getItem("evliyaSesAcik") !== "false"; // varsayılan: açık
let sesListesi = [];
let manuelSesURI = null; // "ses seç" menüsünden gelen elle seçim — sayfa içi, localStorage'a yazılmaz

function sesListesiniYenile() {
  sesListesi = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
  console.log(`[Evliya TTS] ${sesListesi.length} ses bulundu:`, sesListesi.map((s) => `${s.name} (${s.lang})`));
  sesSecimiOlustur();
}

if (window.speechSynthesis) {
  sesListesiniYenile();
  window.speechSynthesis.onvoiceschanged = sesListesiniYenile;
}

// Öncelik sırası: cevap diliyle eşleşen sesler içinde önce adında
// "Natural"/"Online" geçenler, sonra "Google" geçenler, en son geri kalan
// (varsayılan) sesler. Her katmanda erkek ses ipucu varsa o tercih edilir.
function sesSec(dilKodu) {
  if (manuelSesURI) {
    const manuelSes = sesListesi.find((s) => s.voiceURI === manuelSesURI);
    if (manuelSes) return manuelSes;
  }

  const hedefDil = DIL_KODU_ESLESTIRME[dilKodu] || "en";
  const adaylar = sesListesi.filter((s) => s.lang && s.lang.toLowerCase().startsWith(hedefDil));
  if (adaylar.length === 0) return null;

  const katmanlar = [
    adaylar.filter((s) => /natural|online/i.test(s.name)),
    adaylar.filter((s) => /google/i.test(s.name)),
    adaylar,
  ];

  for (const katman of katmanlar) {
    if (katman.length > 0) {
      return katman.find((s) => ERKEK_SES_IPUCLARI.test(s.name)) || katman[0];
    }
  }
  return null;
}

function avatarKonusuyorAyarla(konusuyorMu) {
  document.body.classList.toggle("evliya-konusuyor", konusuyorMu);
}

// Web Speech API uzun metinlerde cümle ortasında kesilebiliyor; metni
// cümlelere bölüp sırayla (kuyruğa alarak) okutmak bunu önlüyor.
function cumlelereBol(metin) {
  const parcalar = metin.match(/[^.!?。!?…]+[.!?。!?…]*(\s+|$)/g);
  return parcalar ? parcalar.map((s) => s.trim()).filter(Boolean) : [metin];
}

// TEK NOKTADAN TTS: ileride ElevenLabs/Gemini TTS gibi bir servise geçmek
// istenirse yalnızca bu fonksiyonun içini değiştirmek yeterli — çağıran
// yerler (submit handler, ses düğmesi) aynı kalabilir.
// parcaBaslayinca (opsiyonel): her cümle sırası geldiğinde çağrılır — anlatı
// sahnesindeki altyazı şeridini TTS ile senkron tutmak için kullanılır (bkz.
// anlatiMetniGoster). SpeechSynthesisUtterance.onstart bazı tarayıcı/ortamlarda
// güvenilir tetiklenmediği için (denendi, sessiz kaldı) kelime sayısına
// dayalı KABA bir süre tahminiyle setTimeout zincirlemesi kullanılıyor —
// mükemmel değil ama her ortamda çalışır. Ses kapalıysa/desteklenmiyorsa
// senkronize edecek bir şey olmadığından metnin tamamıyla bir kez çağrılır.
function metniSesliOku(metin, dilKodu, parcaBaslayinca) {
  if (!sesAcik || !window.speechSynthesis || !metin) {
    if (typeof parcaBaslayinca === "function" && metin) parcaBaslayinca(metin);
    return;
  }
  window.speechSynthesis.cancel();

  const secilenSes = sesSec(dilKodu);
  const dil = secilenSes ? secilenSes.lang : (DIL_KODU_ESLESTIRME[dilKodu] || "en");
  const cumleler = cumlelereBol(metin);
  if (cumleler.length === 0) return;

  console.log(`[Evliya TTS] dil=${dilKodu} -> ses="${secilenSes ? secilenSes.name : "(tarayıcı varsayılanı, " + dil + ")"}", ${cumleler.length} cümle kuyruklandı.`);

  avatarKonusuyorAyarla(true);

  let tahminiGecikme = 0;
  cumleler.forEach((cumle, i) => {
    const konusma = new SpeechSynthesisUtterance(cumle);
    konusma.rate = SES_HIZI;
    konusma.pitch = SES_PERDESI;
    konusma.lang = dil;
    if (secilenSes) konusma.voice = secilenSes;

    if (i === cumleler.length - 1) {
      konusma.onend = () => avatarKonusuyorAyarla(false);
      konusma.onerror = () => avatarKonusuyorAyarla(false);
    }

    window.speechSynthesis.speak(konusma);

    if (typeof parcaBaslayinca === "function") {
      setTimeout(() => parcaBaslayinca(cumle), tahminiGecikme);
    }
    const kelimeSayisi = cumle.split(/\s+/).filter(Boolean).length;
    tahminiGecikme += Math.max(700, (kelimeSayisi / (2.3 * SES_HIZI)) * 1000);
  });
}

function sesDurdur() {
  if (window.speechSynthesis) window.speechSynthesis.cancel();
  avatarKonusuyorAyarla(false);
}

function sesSecimiOlustur() {
  if (!sesSecimi) return;
  const oncekiDeger = sesSecimi.value;
  sesSecimi.innerHTML = "";

  const otomatikSecenek = document.createElement("option");
  otomatikSecenek.value = "";
  otomatikSecenek.textContent = t("voice_auto");
  sesSecimi.appendChild(otomatikSecenek);

  sesListesi.forEach((s) => {
    const secenek = document.createElement("option");
    secenek.value = s.voiceURI;
    secenek.textContent = `${s.name} (${s.lang})`;
    sesSecimi.appendChild(secenek);
  });

  if (oncekiDeger && sesListesi.some((s) => s.voiceURI === oncekiDeger)) {
    sesSecimi.value = oncekiDeger;
  }
}

function sesDugmesiniGuncelle() {
  if (!sesDugmesi) return;
  sesDugmesi.innerHTML = sesAcik
    ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 10v4h4l5 4V6l-5 4H5Z"/><path d="M17 9c1.7 1.7 1.7 4.3 0 6M19.5 6.5c3 3 3 8 0 11"/></svg>'
    : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 10v4h4l5 4V6l-5 4H5Z"/><path d="m17 10 4 4M21 10l-4 4"/></svg>';
  sesDugmesi.setAttribute("aria-pressed", String(sesAcik));
  sesDugmesi.title = sesAcik ? t("voice_off") : t("voice_on");
  sesDugmesi.setAttribute("aria-label", sesDugmesi.title);
}

if (sesDugmesi) {
  sesDugmesiniGuncelle();
  sesDugmesi.addEventListener("click", () => {
    sesAcik = !sesAcik;
    localStorage.setItem("evliyaSesAcik", String(sesAcik));
    sesDugmesiniGuncelle();
    if (!sesAcik) sesDurdur();
  });
}

if (sesSecimi) {
  sesSecimi.addEventListener("change", () => {
    manuelSesURI = sesSecimi.value || null;
  });
}

// ---- Başlangıç kartları -----------------------------------------------
// Henüz bir sohbet dili belirlenmediği için (ilk mesajdan önce) tarayıcının
// dilini (navigator.language) baz alıp en yakın desteklenen dile düşer.

const BASLANGIC_IKONLARI = {
  tarih: '<svg viewBox="0 0 24 24"><path d="M3.5 9h17M5 9V7l7-4 7 4v2M6 9v8M10 9v8M14 9v8M18 9v8M4 17h16M3 20h18"/></svg>',
  deniz: '<svg viewBox="0 0 24 24"><path d="M3 10c2.2 0 2.2-1.6 4.4-1.6s2.2 1.6 4.4 1.6 2.2-1.6 4.4-1.6 2.2 1.6 4.4 1.6M3 14c2.2 0 2.2-1.6 4.4-1.6s2.2 1.6 4.4 1.6 2.2-1.6 4.4-1.6 2.2 1.6 4.4 1.6M3 18c2.2 0 2.2-1.6 4.4-1.6s2.2 1.6 4.4 1.6 2.2-1.6 4.4-1.6 2.2 1.6 4.4 1.6"/><path d="M16.5 4.5h.01M12 4.5h.01"/></svg>',
  lezzet: '<svg viewBox="0 0 24 24"><path d="M4 12h16c-.4 4.6-3.1 7-8 7s-7.6-2.4-8-7ZM3 21h18"/><path d="M8 9c-1.3-1.3.8-2.1-.3-3.5M12 9c-1.3-1.3.8-2.1-.3-3.5M16 9c-1.3-1.3.8-2.1-.3-3.5"/></svg>',
  aile: '<svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="2.5"/><circle cx="5.5" cy="9" r="2"/><circle cx="18.5" cy="9" r="2"/><path d="M7.5 20v-4.5c0-2.2 1.8-4 4-4h1c2.2 0 4 1.8 4 4V20M2.5 20v-4c0-1.8 1.4-3.2 3.2-3.2h1.5M21.5 20v-4c0-1.8-1.4-3.2-3.2-3.2h-1.5"/></svg>',
  gizli: '<svg viewBox="0 0 24 24"><circle cx="8" cy="9" r="4"/><path d="m11 12 8 8M15 16l2-2M17 18l2-2"/><path d="M8 7v4M6 9h4"/></svg>',
};

const BASLANGIC_KARTLARI = {
  tr: [
    { ikon: "tarih", baslik: "3 günlük tarih rotası", mesaj: "Bana 3 günlük bir tarih rotası önerir misin?" },
    { ikon: "deniz", baslik: "Sakin sahil kasabaları", mesaj: "Sakin, sessiz sahil kasabaları önerir misin?" },
    { ikon: "lezzet", baslik: "Türkiye'nin lezzet durakları", mesaj: "Türkiye'nin mutlaka tadılması gereken lezzet duraklarını anlatır mısın?" },
    { ikon: "aile", baslik: "Çocuklarla aile gezisi", mesaj: "Çocuklarımla gidebileceğimiz aile dostu yerler önerir misin?" },
    { ikon: "gizli", baslik: "Az bilinen yerler", mesaj: "Az bilinen, gizli kalmış yerleri anlatır mısın?" },
  ],
  en: [
    { ikon: "tarih", baslik: "3-day history route", mesaj: "Can you suggest a 3-day history route?" },
    { ikon: "deniz", baslik: "Calm coastal towns", mesaj: "Can you recommend some calm, quiet coastal towns?" },
    { ikon: "lezzet", baslik: "Turkey's flavor stops", mesaj: "Tell me about Turkey's must-try food stops." },
    { ikon: "aile", baslik: "Family trip with kids", mesaj: "Can you suggest family-friendly places to visit with kids?" },
    { ikon: "gizli", baslik: "Hidden gems", mesaj: "Tell me about some lesser-known, hidden places." },
  ],
  de: [
    { ikon: "tarih", baslik: "3-tägige Geschichtsroute", mesaj: "Kannst du mir eine 3-tägige Geschichtsroute vorschlagen?" },
    { ikon: "deniz", baslik: "Ruhige Küstenstädte", mesaj: "Kannst du ruhige, stille Küstenstädte empfehlen?" },
    { ikon: "lezzet", baslik: "Türkeis kulinarische Stationen", mesaj: "Erzähl mir von den kulinarischen Highlights der Türkei, die man unbedingt probieren muss." },
    { ikon: "aile", baslik: "Familienausflug mit Kindern", mesaj: "Kannst du familienfreundliche Orte für einen Ausflug mit Kindern vorschlagen?" },
    { ikon: "gizli", baslik: "Versteckte Orte", mesaj: "Erzähl mir von wenig bekannten, versteckten Orten." },
  ],
  ja: [
    { ikon: "tarih", baslik: "3日間の歴史ルート", mesaj: "3日間の歴史ルートを提案してもらえますか?" },
    { ikon: "deniz", baslik: "静かな海辺の町", mesaj: "静かで落ち着いた海辺の町を教えてください。" },
    { ikon: "lezzet", baslik: "トルコの絶品グルメ", mesaj: "トルコで絶対食べるべきグルメスポットを教えてください。" },
    { ikon: "aile", baslik: "子連れ家族旅行", mesaj: "子供と一緒に行ける家族向けの場所を教えてください。" },
    { ikon: "gizli", baslik: "穴場スポット", mesaj: "あまり知られていない穴場スポットを教えてください。" },
  ],
};

function tarayiciDiliniBul() {
  return BASLANGIC_KARTLARI[aktifArayuzDili] ? aktifArayuzDili : "en";
}

function baslangicKartlariniOlustur() {
  if (!baslangicKartlari) return;
  const kartlar = BASLANGIC_KARTLARI[tarayiciDiliniBul()];
  baslangicKartlari.innerHTML = "";

  kartlar.forEach((kart) => {
    const dugme = document.createElement("button");
    dugme.type = "button";
    dugme.className = "baslangic-karti";

    const ikon = document.createElement("span");
    ikon.className = "baslangic-karti-ikon";
    ikon.innerHTML = BASLANGIC_IKONLARI[kart.ikon] || BASLANGIC_IKONLARI.gizli;
    dugme.appendChild(ikon);

    const baslik = document.createElement("span");
    baslik.textContent = kart.baslik;
    dugme.appendChild(baslik);

    dugme.addEventListener("click", () => {
      mesajGirisi.value = kart.mesaj;
      mesajFormu.requestSubmit();
    });

    baslangicKartlari.appendChild(dugme);
  });
}

baslangicKartlariniOlustur();

// ---- Kültür sekmesi: "Yabancılar Soruyor, Evliya Cevaplıyor" ----------
// Hazır tıklanabilir kültür soruları — tıklanınca doğrudan Evliya'ya
// gönderilir. Sohbet dili netleşene kadar tarayıcı dili baz alınır; ilk
// cevap geldiğinde panel.dil'e göre yeniden çizilir (bkz. submit handler).

let kulturGosterilenDil = null;

const MERAK_IKONLARI = {
  "cay-ikrami": '<svg viewBox="0 0 24 24"><path d="M6 8h9l-1 9H7L6 8ZM15 10h2a2 2 0 0 1 0 4h-2M5 20h11"/><path d="M9 5c-1-1 .7-1.7 0-3M12 5c-1-1 .7-1.7 0-3"/></svg>',
  "cami-ziyareti": '<svg viewBox="0 0 24 24"><path d="M5 20V10h14v10M3 20h18M8 10V7l4-3 4 3v3M12 4V2M9 14h6M12 14v6M4 10V6M20 10V6"/></svg>',
  "nazar-boncugu": '<svg viewBox="0 0 24 24"><path d="M2.5 12s3.5-5 9.5-5 9.5 5 9.5 5-3.5 5-9.5 5-9.5-5-9.5-5Z"/><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="1"/></svg>',
  "evde-ayakkabi": '<svg viewBox="0 0 24 24"><path d="m3 11 9-7 9 7M5.5 10v10h13V10M9 20v-6h6v6"/><path d="M2.5 21.5h19"/></svg>',
  "turk-kahvaltisi": '<svg viewBox="0 0 24 24"><path d="M4 13h16c-.5 4-3.2 6-8 6s-7.5-2-8-6ZM3 21h18"/><circle cx="9" cy="9" r="2.5"/><path d="M14 6h5M16.5 4v4"/></svg>',
  "pazarlik": '<svg viewBox="0 0 24 24"><path d="M5 8h14l-1 12H6L5 8ZM9 9V6a3 3 0 0 1 6 0v3"/><path d="M9 13h6M12 11v4"/></svg>',
  "bahsis": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M14.5 8.5h-3a2 2 0 0 0 0 4h1a2 2 0 0 1 0 4h-3M12 6v12"/></svg>',
  "misafirperverlik": '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.2-7-9a3.8 3.8 0 0 1 7-2 3.8 3.8 0 0 1 7 2c0 4.8-7 9-7 9Z"/><path d="M3 21h18"/></svg>',
  "ramazanda-seyahat": '<svg viewBox="0 0 24 24"><path d="M17 15.5A7 7 0 1 1 10.5 5 6 6 0 0 0 17 15.5Z"/><path d="m18.5 5 .5 1.3 1.3.5-1.3.5-.5 1.3-.5-1.3-1.3-.5 1.3-.5.5-1.3Z"/></svg>',
  "yalniz-seyahat": '<svg viewBox="0 0 24 24"><path d="M7 9h10a2 2 0 0 1 2 2v9H5v-9a2 2 0 0 1 2-2ZM9 9V6a3 3 0 0 1 6 0v3M8 13v4M16 13v4"/></svg>',
  "hamam-adabi": '<svg viewBox="0 0 24 24"><path d="M4 14h16c-.5 4-3.2 6-8 6s-7.5-2-8-6Z"/><path d="M8 11c-1.4-1.4.9-2.2-.2-4M12 11c-1.4-1.4.9-2.2-.2-4M16 11c-1.4-1.4.9-2.2-.2-4"/></svg>',
  "kahve-fali": '<svg viewBox="0 0 24 24"><path d="M5 8h11v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8ZM16 10h2a3 3 0 0 1 0 6h-2M4 22h15"/><path d="M9 5c-1-1 .7-1.7 0-3M13 5c-1-1 .7-1.7 0-3"/></svg>',
  "sokak-kedileri": '<svg viewBox="0 0 24 24"><path d="m6 9-1-5 4 2a9 9 0 0 1 6 0l4-2-1 5a7 7 0 1 1-12 0Z"/><circle cx="9.5" cy="12" r=".7"/><circle cx="14.5" cy="12" r=".7"/><path d="m10 15 2 1 2-1M4 14H1M20 14h3M4.5 17 2 18M19.5 17l2.5 1"/></svg>',
  "abi-abla-hitabi": '<svg viewBox="0 0 24 24"><path d="M4 5h11v8H9l-4 3v-3H4V5ZM12 10h8v7h-2v3l-4-3h-2"/></svg>',
  "dolmus-kullanimi": '<svg viewBox="0 0 24 24"><path d="M5 4h14l2 7v7H3v-7l2-7ZM5 11h14M7 7h10M6 18v2M18 18v2"/><circle cx="7" cy="15" r="1"/><circle cx="17" cy="15" r="1"/></svg>',
  "kolonya-ikrami": '<svg viewBox="0 0 24 24"><path d="M9 3h6v4l2 2v11H7V9l2-2V3ZM9 6h6M10 13h4M10 16h4"/><path d="M18.5 5.5c1.7 2 1.7 3.3 0 4.5-1.7-1.2-1.7-2.5 0-4.5Z"/></svg>',
  "yolcuya-su-dokmek": '<svg viewBox="0 0 24 24"><path d="M12 3s5 5.6 5 10a5 5 0 0 1-10 0c0-4.4 5-10 5-10Z"/><path d="M4 20c2 0 2-1 4-1s2 1 4 1 2-1 4-1 2 1 4 1"/></svg>',
  "kilim-desenleri": '<svg viewBox="0 0 24 24"><path d="M5 3h14v18H5zM5 6h14M5 18h14"/><path d="m12 8 4 4-4 4-4-4 4-4ZM7 3V1M11 3V1M15 3V1M19 3V1M7 23v-2M11 23v-2M15 23v-2M19 23v-2"/></svg>',
  "meze-sofrasi": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="8" cy="10" r="2.2"/><circle cx="16" cy="10" r="2.2"/><circle cx="12" cy="16" r="2.2"/></svg>',
  "dugun-gelenekleri": '<svg viewBox="0 0 24 24"><circle cx="9" cy="12" r="5"/><circle cx="15" cy="12" r="5"/><path d="m12 5 1-2h3l1 2"/></svg>',
  "tavla-kulturu": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/><circle cx="6" cy="6" r=".6"/><circle cx="8" cy="8" r=".6"/><circle cx="16" cy="16" r=".6"/><circle cx="18" cy="18" r=".6"/></svg>',
  "kahvenin-yaninda-su": '<svg viewBox="0 0 24 24"><path d="M3 9h9v7a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9ZM12 11h1.5a2.5 2.5 0 0 1 0 5H12M16 6h5l-1 14h-3L16 6ZM17 10h3.7"/></svg>',
};

const MERAK_NEDENLERI = {
  tr: { "ilgi-alanina-gore": "İlgine göre", "dilinde-sik-soruluyor": "Dilinde sık soruluyor", kesfet: "Evliya'dan keşfet" },
  en: { "ilgi-alanina-gore": "Based on your interests", "dilinde-sik-soruluyor": "Often asked in your language", kesfet: "Discover with Evliya" },
  de: { "ilgi-alanina-gore": "Passend zu deinen Interessen", "dilinde-sik-soruluyor": "In deiner Sprache oft gefragt", kesfet: "Mit Evliya entdecken" },
  ja: { "ilgi-alanina-gore": "興味に合わせて", "dilinde-sik-soruluyor": "あなたの言語でよくある質問", kesfet: "エヴリヤと発見" },
};

async function kulturSorulariniOlustur(dilKodu, oneriler = null) {
  if (!kulturSorulari) return;
  const dil = ["tr", "en", "de", "ja"].includes(dilKodu) ? dilKodu : "tr";
  if (!oneriler && dil === kulturGosterilenDil) return;
  kulturGosterilenDil = dil;

  if (!oneriler) {
    try {
      const yanit = await fetch(`/meraklar?dil=${encodeURIComponent(dil)}`);
      oneriler = (await yanit.json()).merak_onerileri || [];
    } catch (hata) {
      console.error("Merak önerileri alınamadı:", hata);
      oneriler = [];
    }
  }

  kulturSorulari.innerHTML = "";
  oneriler.forEach((soru) => {
    const dugme = document.createElement("button");
    dugme.type = "button";
    dugme.className = "kultur-soru-karti";

    const ikon = document.createElement("span");
    ikon.className = "kultur-soru-karti-ikon";
    ikon.innerHTML = MERAK_IKONLARI[soru.slug] || BASLANGIC_IKONLARI.gizli;
    dugme.appendChild(ikon);

    const metin = document.createElement("span");
    metin.className = "kultur-soru-karti-metni";
    metin.textContent = soru.soru;
    dugme.appendChild(metin);

    const neden = document.createElement("small");
    neden.className = "merak-neden";
    neden.textContent = (MERAK_NEDENLERI[dil] || MERAK_NEDENLERI.en)[soru.neden] || "";
    dugme.appendChild(neden);

    dugme.addEventListener("click", () => {
      sekmeSec("gorseller");
      mesajGirisi.value = soru.soru;
      mesajFormu.requestSubmit();
    });

    kulturSorulari.appendChild(dugme);
  });
}

kulturSorulariniOlustur(tarayiciDiliniBul());

function merakIzinDurumunuGuncelle() {
  if (!merakGizlilikNotu) return;
  merakGizlilikNotu.textContent = merakAnalitikIzni
    ? "Anonim konu eğilimleri açık · Mesaj metni ve kimlik bilgileri saklanmaz."
    : "Kişiselleştirilmiş kartlar açık · Anonim eğilim paylaşımı kapalı.";
}

function merakIzinPenceresiniKapat() {
  merakIzinOverlay.classList.remove("gorunur");
  merakIzinOverlay.setAttribute("aria-hidden", "true");
}

if (!localStorage.getItem("evliyaMerakIzni")) {
  setTimeout(() => {
    merakIzinOverlay.classList.add("gorunur");
    merakIzinOverlay.setAttribute("aria-hidden", "false");
  }, 700);
}
if (merakUlke) merakUlke.value = merakUlkeKodu;
merakIzinVer.addEventListener("click", () => {
  merakAnalitikIzni = true;
  merakUlkeKodu = merakUlke.value;
  localStorage.setItem("evliyaMerakIzni", "evet");
  localStorage.setItem("evliyaMerakUlke", merakUlkeKodu);
  merakIzinDurumunuGuncelle();
  merakIzinPenceresiniKapat();
});
merakIzinReddet.addEventListener("click", () => {
  merakAnalitikIzni = false;
  merakUlkeKodu = "";
  localStorage.setItem("evliyaMerakIzni", "hayir");
  localStorage.removeItem("evliyaMerakUlke");
  merakIzinDurumunuGuncelle();
  merakIzinPenceresiniKapat();
});
merakIzinDurumunuGuncelle();

// ---- Yeni Yolculuk sihirbazı -----------------------------------------
// Alternatifleri istemcide kuruyoruz; seçilen omurga mevcut /sohbet motoruna
// ayrıntılı bir istek olarak gider. Böylece karakter, profil ve medya akışı
// tek bir yerde kalır ve fazladan Gemini isteği harcanmaz.
const YOLCULUK_ADIMLARI = [
  { anahtar: "gun", soru: "Kaç günün var?", secenekler: [["2", "2 gün"], ["3", "3 gün"], ["5", "5 gün"], ["7", "1 hafta"]] },
  { anahtar: "baslangic", soru: "Yola nereden çıkacaksın?", giris: true },
  { anahtar: "ilgi", soru: "Yolculuğunun ruhu ne olsun?", secenekler: [["tarih", "🏛️ Tarih"], ["doga", "🌿 Doğa"], ["yemek", "🍽️ Lezzet"], ["deniz", "🌊 Deniz"], ["sanat", "🎨 Sanat"], ["macera", "⛰️ Macera"], ["aile", "👨‍👩‍👧 Aile"]] },
  { anahtar: "tempo", soru: "Hangi tempoda gezelim?", secenekler: [["sakin", "Sakin"], ["dengeli", "Dengeli"], ["yogun", "Dolu dolu"]] },
];

const ROTA_HAVUZU = {
  tarih: [
    ["Payitahtın İzleri", "istanbul", "bursa", "iznik", "safranbolu"],
    ["Anadolu'nun Kadim Taşları", "ankara", "hattusa", "amasya", "tokat"],
    ["Mezopotamya Kapısı", "sanliurfa", "gobeklitepe", "mardin", "diyarbakir"],
  ],
  doga: [
    ["Yeşil Yaylalar", "trabzon", "rize", "ayder", "kackar"],
    ["Göller ve Antik Patikalar", "pamukkale", "egirdir", "sagalassos", "antalya"],
    ["Gökova'nın Sessizliği", "akyaka", "datca", "koycegiz", "marmaris"],
  ],
  yemek: [
    ["Bereketli Sofralar", "gaziantep", "sanliurfa", "hatay", "adana"],
    ["Marmara Lezzet Yolu", "istanbul", "bursa", "eskisehir", "iznik"],
    ["İç Anadolu Sofrası", "kayseri", "kapadokya", "konya", "ankara"],
  ],
  deniz: [
    ["Ege'nin Sakin Koyları", "akyaka", "datca", "marmaris", "fethiye"],
    ["Taş Evler ve Mavi Sular", "assos", "ayvalik", "foca", "cesme"],
    ["Akdeniz Günlüğü", "antalya", "kas", "kalkan", "cirali"],
  ],
  sanat: [
    ["İmparatorlukların Sanatı", "istanbul", "bursa", "kutahya", "eskisehir"],
    ["Taş İşçiliğinin İzinde", "mardin", "midyat", "sanliurfa", "gaziantep"],
    ["Ege Atölyeleri", "izmir", "urla", "sirince", "bodrum"],
  ],
  macera: [
    ["Dağların Çağrısı", "rize", "ayder", "kackar", "artvin"],
    ["Kanyon ve Patikalar", "antalya", "koprulu-kanyon", "sagalassos", "egirdir"],
    ["Volkanik Masal", "kayseri", "erciyes", "kapadokya", "ihlara"],
  ],
  aile: [
    ["Ailece Marmara", "istanbul", "bursa", "eskisehir", "sapanca"],
    ["Masal Gibi Kapadokya", "ankara", "kapadokya", "kayseri", "konya"],
    ["Güneşli Akdeniz", "antalya", "side", "belek", "burdur"],
  ],
};

let yolculukAdimi = 0;
let yolculukSecimleri = {};

function yerAdiniYaz(slug) {
  return slug.split("-").map((parca) => parca.charAt(0).toUpperCase() + parca.slice(1)).join(" ");
}

function yolculukIlerle(anahtar, deger) {
  yolculukSecimleri[anahtar] = deger;
  yolculukAdimi += 1;
  yolculukAdiminiGoster();
}

function yolculukAdiminiGoster() {
  yolculukIlerleme.innerHTML = "";
  for (let i = 0; i < YOLCULUK_ADIMLARI.length; i += 1) {
    const nokta = document.createElement("span");
    nokta.className = i <= yolculukAdimi ? "aktif" : "";
    yolculukIlerleme.appendChild(nokta);
  }

  if (yolculukAdimi >= YOLCULUK_ADIMLARI.length) {
    rotaAlternatifleriniGoster();
    return;
  }

  const adim = YOLCULUK_ADIMLARI[yolculukAdimi];
  yolculukIcerik.innerHTML = `<h3>${adim.soru}</h3>`;
  if (adim.giris) {
    const form = document.createElement("form");
    form.className = "yolculuk-giris-formu";
    form.innerHTML = '<input aria-label="Başlangıç şehri" placeholder="Örn. İstanbul" required autofocus><button type="submit">Devam et →</button>';
    form.addEventListener("submit", (olay) => {
      olay.preventDefault();
      const deger = form.querySelector("input").value.trim();
      if (deger) yolculukIlerle(adim.anahtar, deger);
    });
    yolculukIcerik.appendChild(form);
    setTimeout(() => form.querySelector("input").focus(), 50);
    return;
  }

  const secenekler = document.createElement("div");
  secenekler.className = "yolculuk-secenekleri";
  adim.secenekler.forEach(([deger, etiket]) => {
    const dugme = document.createElement("button");
    dugme.type = "button";
    dugme.textContent = etiket;
    dugme.addEventListener("click", () => yolculukIlerle(adim.anahtar, deger));
    secenekler.appendChild(dugme);
  });
  yolculukIcerik.appendChild(secenekler);
}

function rotaAlternatifleriniGoster() {
  yolculukIcerik.innerHTML = "<h3>Üç seyahatname sayfasından birini seç</h3><p class=\"yolculuk-aciklama\">Evliya seçtiğin rotayı gün gün; tatları ve yerel deneyimleriyle anlatacak.</p>";
  const liste = document.createElement("div");
  liste.className = "rota-alternatifleri";
  (ROTA_HAVUZU[yolculukSecimleri.ilgi] || ROTA_HAVUZU.tarih).forEach(([baslik, ...rota]) => {
    const dugme = document.createElement("button");
    dugme.type = "button";
    dugme.className = "rota-alternatifi";
    dugme.innerHTML = `<strong>${baslik}</strong><span>${rota.map(yerAdiniYaz).join(" → ")}</span>`;
    dugme.addEventListener("click", () => yolculuguBaslat(baslik, rota));
    liste.appendChild(dugme);
  });
  yolculukIcerik.appendChild(liste);
}

function yeniSohbetiSifirla() {
  gecmis = [];
  sesDurdur();
  anlatiSahneyiGuncelle([]);
  anlatiMetniGoster("");
  yerGaleriKayitlari.clear();
  mekanDetayKayitlari.clear();
  duzenlenenRota = [];
  duzenlenenRotaDetaylari = [];
  rotaGunleri.clear();
  lezzetGaleriKayitlari.clear();
  defterMedya.innerHTML = '<p class="bos-not">Yeni yolculuğun durakları burada birikecek.</p>';
  defterLezzet.innerHTML = "";
  defterLezzet.classList.remove("gorunur");
  rotaGuncelle([]);
  haritayiTemizle();
  const haritaSekmesi = document.querySelector('.defter-sekme-dugmesi[data-sekme="harita"]');
  if (haritaSekmesi) haritaSekmesi.disabled = true;
  gezginProfiliGuncelle({ etiketler: [], aciklama: "Evliya seni tanımaya başlıyor..." });
  sonRotaVerisi = null;
  kartButonu.classList.remove("gorunur");
  sekmeSec("gorseller");
  mesajAkisi.innerHTML = '<div class="balon evliya"><p>Yeni bir seyahatname sayfası açtım, yolcu. Seçtiğin rotayı şimdi birlikte işleyelim.</p></div>';
}

function yolculuguBaslat(baslik, rota) {
  const tempo = { sakin: "sakin", dengeli: "dengeli", yogun: "dolu dolu" }[yolculukSecimleri.tempo];
  const mesaj = `${yolculukSecimleri.gun} günlük, ${yolculukSecimleri.ilgi} ağırlıklı ve ${tempo} tempolu bir Türkiye rotası planla. Başlangıç şehrim: ${yolculukSecimleri.baslangic}. Seçtiğim yaklaşım: ${baslik}. Rota omurgası: ${rota.map(yerAdiniYaz).join(" → ")}. Günleri somut biçimde anlat; her gün için mutlaka bir yöresel tat ve yerel deneyim öner; panel.rota alanını ziyaret sırasıyla doldur.`;
  yeniSohbetiSifirla();
  yolculukOverlay.classList.remove("gorunur");
  yolculukOverlay.setAttribute("aria-hidden", "true");
  mesajGirisi.value = mesaj;
  mesajFormu.requestSubmit();
}

function yolculukPenceresiniAc() {
  yolculukAdimi = 0;
  yolculukSecimleri = {};
  yolculukOverlay.classList.add("gorunur");
  yolculukOverlay.setAttribute("aria-hidden", "false");
  yolculukAdiminiGoster();
}

yeniYolculukButonu.addEventListener("click", yolculukPenceresiniAc);
function yolculukPenceresiniKapat() {
  yolculukOverlay.classList.remove("gorunur");
  yolculukOverlay.setAttribute("aria-hidden", "true");
}

yolculukKapat.addEventListener("click", yolculukPenceresiniKapat);
yolculukOverlay.addEventListener("click", (olay) => {
  if (olay.target === yolculukOverlay) yolculukPenceresiniKapat();
});
document.addEventListener("keydown", (olay) => {
  if (olay.key === "Escape" && yolculukOverlay.classList.contains("gorunur")) yolculukPenceresiniKapat();
});

mesajFormu.addEventListener("submit", async (olay) => {
  olay.preventDefault();
  const mesaj = mesajGirisi.value.trim();
  if (!mesaj) return;

  if (baslangicKartlari) baslangicKartlari.remove(); // sohbet başladı, kartlar gizlensin

  balonEkle("konuk", mesaj);
  mesajGirisi.value = "";
  mesajGirisi.disabled = true;
  mesajFormu.querySelector("button").disabled = true;

  const yukleniyorBalonu = balonEkle("yukleniyor", t("thinking"));

  const kontrolci = new AbortController();
  const zamanAsimiId = setTimeout(() => kontrolci.abort(), ISTEK_ZAMAN_ASIMI_MS);

  try {
    const yanit = await fetch("/sohbet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mesaj,
        gecmis,
        analitik_izin: merakAnalitikIzni,
        oturum_id: merakOturumId,
        ulke: merakUlkeKodu,
        demo_modu: demoModu,
      }),
      signal: kontrolci.signal,
    });
    const veri = await yanit.json();

    yukleniyorBalonu.remove();

    if (!yanit.ok || veri.hata) {
      // Teknik ayrıntı yalnızca konsola — sohbette hep karakter içinden
      // zarif bir cevap görünür, kullanıcı ham hata görmez.
      console.error("Sohbet hatası:", veri.hata || yanit.status);
      const yogunlukMesaji = YOGUNLUK_MESAJI();
      balonEkle("evliya", yogunlukMesaji);
      metniSesliOku(yogunlukMesaji, aktifArayuzDili);
      return;
    }

    balonEkle("evliya", veri.reply);
    const cevapDili = (veri.panel && veri.panel.dil) || "tr";
    arayuzDiliniAyarla(cevapDili, true);
    kulturSorulariniOlustur(cevapDili, veri.merak_onerileri);
    kulturCevabiEkle(veri.panel && veri.panel.kultur, cevapDili, veri.merak_konusu, veri.kultur_kaynagi);
    gecmis.push({ rol: "user", icerik: mesaj });
    // temalar: gezgin profilinin oturum-içi hesaplanabilmesi için geçmişle
    // birlikte taşınır — sunucuda hiçbir yerde saklanmaz (bkz. profil_hesapla).
    gecmis.push({ rol: "evliya", icerik: veri.reply, temalar: (veri.panel && veri.panel.temalar) || [] });

    haritayiGuncelle(veri.rota_koordinatlari, veri.rota_detaylari);
    anlatiSahneyiGuncelle(veri.medyalar);
    medyalariGuncelle(veri.medyalar, veri.mekan_detaylari);
    lezzetleriGuncelle(veri.lezzet_medyalari);
    gezginProfiliGuncelle(veri.gezgin_profili);
    rotaGuncelle(veri.rota, veri.rota_detaylari);
    metniSesliOku(veri.reply, veri.panel && veri.panel.dil, anlatiMetniGoster);

    if (veri.rota && veri.rota.length > 0) {
      sonRotaVerisi = { rota: veri.rota, medyalar: veri.medyalar, panel: veri.panel };
      if (kartButonu) kartButonu.classList.add("gorunur");
    }
  } catch (hata) {
    yukleniyorBalonu.remove();
    if (hata.name === "AbortError") {
      console.error("Sohbet isteği zaman aşımına uğradı (" + ISTEK_ZAMAN_ASIMI_MS + "ms).");
    } else {
      console.error("Sohbet bağlantı hatası:", hata);
    }
    const yogunlukMesaji = YOGUNLUK_MESAJI();
    balonEkle("evliya", yogunlukMesaji);
    metniSesliOku(yogunlukMesaji, aktifArayuzDili);
  } finally {
    clearTimeout(zamanAsimiId);
    mesajGirisi.disabled = false;
    mesajFormu.querySelector("button").disabled = false;
    mesajGirisi.focus();
  }
});
