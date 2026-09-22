const sayi = new Intl.NumberFormat("tr-TR");
const adminCsrf = document.querySelector('meta[name="admin-csrf"]')?.content || "";

function ozetKartlariniCiz(kartlar) {
  const tanimlar = [
    ["toplam_merak", "Toplam merak", "✦"], ["izinli_oturum", "İzinli oturum", "◉"],
    ["son_7_gun", "Son 7 gün", "↗"], ["son_30_gun", "Son 30 gün", "▦"],
    ["yararli_orani", "Yararlı cevap", "♡"],
  ];
  const alan = document.getElementById("ozetKartlari");
  tanimlar.forEach(([anahtar, baslik, ikon]) => {
    const kart = document.createElement("article"); kart.className = "ozet-karti";
    const deger = kartlar[anahtar];
    kart.innerHTML = `<span class="ozet-ikon">${ikon}</span><small>${baslik}</small><strong>${deger == null ? "—" : sayi.format(deger)}${anahtar === "yararli_orani" && deger != null ? "%" : ""}</strong>`;
    alan.appendChild(kart);
  });
}

function icerikSagliginiCiz(saglik) {
  const alan = document.getElementById("icerikSagligi");
  const degerler = [
    ["Doğrulanmış kültür konusu", saglik.onayli, "iyi"],
    ["İnceleme bekleyen", saglik.incelemede, saglik.incelemede ? "uyari" : "iyi"],
    ["Kaynağı eksik", saglik.kaynaksiz, saglik.kaynaksiz ? "uyari" : "iyi"],
    ["180 günü geçen", saglik.eski, saglik.eski ? "kritik" : "iyi"],
  ];
  const baslik = document.createElement("div"); baslik.className = "icerik-sagligi-baslik";
  const ust = document.createElement("span"); ust.textContent = "İçerik sağlığı";
  const toplam = document.createElement("strong"); toplam.textContent = `${saglik.toplam} kültür konusu izleniyor`;
  baslik.append(ust, toplam); alan.appendChild(baslik);
  degerler.forEach(([etiket, deger, durum]) => {
    const oge = document.createElement("div"); oge.className = `saglik-oge ${durum}`;
    const sayac = document.createElement("b"); sayac.textContent = deger;
    const metin = document.createElement("span"); metin.textContent = etiket;
    oge.append(sayac, metin); alan.appendChild(oge);
  });
}

function yatayGrafikCiz(id, veriler, bosMetin) {
  const alan = document.getElementById(id); alan.innerHTML = "";
  if (!veriler.length) { alan.innerHTML = `<p class="bos-veri">${bosMetin}</p>`; return; }
  const enYuksek = Math.max(...veriler.map((x) => x.adet), 1);
  veriler.forEach((veri) => {
    const satir = document.createElement("div"); satir.className = "yatay-satir";
    const etiket = document.createElement("span"); etiket.textContent = veri.etiket || "Belirsiz";
    const cubuk = document.createElement("div"); cubuk.className = "yatay-cubuk";
    const dolgu = document.createElement("i"); dolgu.style.width = `${(veri.adet / enYuksek) * 100}%`; cubuk.appendChild(dolgu);
    const adet = document.createElement("strong"); adet.textContent = sayi.format(veri.adet);
    satir.append(etiket, cubuk, adet); alan.appendChild(satir);
  });
}

function gunlukGrafikCiz(veriler) {
  const alan = document.getElementById("gunlukGrafik");
  const enYuksek = Math.max(...veriler.map((x) => x.adet), 1);
  veriler.forEach((veri, index) => {
    const cubuk = document.createElement("div"); cubuk.className = "gun-cubugu";
    cubuk.style.height = `${Math.max(3, (veri.adet / enYuksek) * 100)}%`;
    cubuk.title = `${veri.gun}: ${veri.adet}`;
    if (index % 5 === 0 || index === veriler.length - 1) cubuk.dataset.gun = veri.gun.slice(5);
    alan.appendChild(cubuk);
  });
}

function konuTablosuCiz(konular) {
  const alan = document.getElementById("konuTablosu");
  if (!konular.length) { alan.innerHTML = '<p class="bos-veri">Henüz izinli merak verisi yok.</p>'; return; }
  konular.forEach((konu, i) => {
    const satir = document.createElement("div"); satir.className = "konu-satiri";
    const sira = document.createElement("span"); sira.className = "konu-sira"; sira.textContent = i + 1;
    const metin = document.createElement("div");
    const baslik = document.createElement("strong"); baslik.textContent = `${konu.ikon} ${konu.baslik}`;
    const slug = document.createElement("small"); slug.textContent = konu.slug; metin.append(baslik, slug);
    const adet = document.createElement("b"); adet.textContent = `${konu.adet} soru`;
    const fayda = document.createElement("em"); fayda.textContent = konu.fayda == null ? "Geri bildirim yok" : `%${konu.fayda} yararlı`;
    satir.append(sira, metin, adet, fayda); alan.appendChild(satir);
  });
}

async function paneliYukle() {
  const yanit = await fetch("/admin/api/ozet", { credentials: "same-origin" });
  if (yanit.status === 401) { location.href = "/admin/giris"; return; }
  if (!yanit.ok) throw new Error(`Analitik API: ${yanit.status}`);
  const veri = await yanit.json();
  ozetKartlariniCiz(veri.kartlar); icerikSagliginiCiz(veri.icerik_sagligi); gunlukGrafikCiz(veri.gunluk);
  yatayGrafikCiz("dilGrafik", veri.diller, "Henüz dil verisi yok.");
  yatayGrafikCiz("ulkeGrafik", veri.ulkeler, "Gizlilik eşiğini geçen ülke verisi yok.");
  konuTablosuCiz(veri.konular);
  document.getElementById("gizlilikNotu").textContent = veri.gizlilik_notu;
  document.getElementById("adminGuncelleme").textContent = `Son güncelleme: ${new Date(veri.uretildi).toLocaleString("tr-TR")}`;
  document.getElementById("adminGovde").setAttribute("aria-busy", "false");
}

let deneyimAramaZamanlayici = null;
let acikDeneyimId = null;

function deneyimOzetiniCiz(ozet) {
  const alan = document.getElementById("deneyimOzet");
  const kartlar = [
    [ozet.toplam_deneyim, "Deneyim"],
    [ozet.coklu_il_deneyimi, "Birden fazla ili olan"],
    [ozet.onerilen_eslesme, "Onay bekleyen"],
    [ozet.onayli_eslesme, "Onaylı eşleşme"],
    [ozet.reddedilen_eslesme, "Reddedilen"],
  ];
  alan.innerHTML = "";
  kartlar.forEach(([deger, etiket]) => {
    const kart = document.createElement("div");
    const guclu = document.createElement("strong"); guclu.textContent = sayi.format(deger || 0);
    const metin = document.createElement("span"); metin.textContent = etiket;
    kart.append(guclu, metin); alan.appendChild(kart);
  });
}

async function deneyimDurumuKaydet(deneyimId, il, durum) {
  const yanit = await fetch(`/admin/api/deneyimler/${deneyimId}/il`, {
    method: "POST", credentials: "same-origin",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": adminCsrf },
    body: JSON.stringify({ il, durum }),
  });
  if (yanit.status === 401) { location.href = "/admin/giris"; return; }
  const veri = await yanit.json();
  if (!yanit.ok) throw new Error(veri.hata || "Eşleşme kaydedilemedi");
  acikDeneyimId = deneyimId;
  await deneyimleriYukle();
}

function deneyimKartiniOlustur(deneyim, tumIller) {
  const kart = document.createElement("details");
  kart.className = "deneyim-karti"; kart.dataset.deneyimId = deneyim.id;
  if (acikDeneyimId === deneyim.id) kart.open = true;
  kart.addEventListener("toggle", () => { if (kart.open) acikDeneyimId = deneyim.id; });

  const ozet = document.createElement("summary");
  const baslik = document.createElement("div");
  const no = document.createElement("small"); no.textContent = `#${deneyim.no} · ${deneyim.ad_en}`;
  const ad = document.createElement("strong"); ad.textContent = deneyim.ad_tr;
  const temalar = document.createElement("span"); temalar.textContent = deneyim.temalar.map((x) => x.replaceAll("-", " ")).join(" · ");
  baslik.append(no, ad, temalar);
  const sayaclar = document.createElement("div"); sayaclar.className = "deneyim-sayaclar";
  [["oneri", deneyim.sayilar.oneri, "öneri"], ["onayli", deneyim.sayilar.onayli, "onaylı"], ["reddedildi", deneyim.sayilar.reddedildi, "red"]].forEach(([sinif, adet, etiket]) => {
    const rozet = document.createElement("b"); rozet.className = sinif; rozet.textContent = `${adet} ${etiket}`; sayaclar.appendChild(rozet);
  });
  ozet.append(baslik, sayaclar); kart.appendChild(ozet);

  const govde = document.createElement("div"); govde.className = "deneyim-kart-govde";
  const ilListesi = document.createElement("div"); ilListesi.className = "deneyim-il-listesi";
  deneyim.iller.forEach((eslesme) => {
    const satir = document.createElement("article"); satir.className = `deneyim-il ${eslesme.durum}`;
    const bilgi = document.createElement("div");
    const il = document.createElement("strong"); il.textContent = eslesme.il;
    const alt = document.createElement("small"); alt.textContent = `${Math.round(eslesme.guven * 100)}% güven · ${eslesme.kaynak_adi || "Kaynak bekliyor"}`;
    bilgi.append(il, alt);
    const aksiyon = document.createElement("div"); aksiyon.className = "deneyim-il-aksiyon";
    const onay = document.createElement("button"); onay.type = "button"; onay.textContent = "✓ Onayla"; onay.className = "onay"; onay.disabled = eslesme.durum === "onayli";
    const red = document.createElement("button"); red.type = "button"; red.textContent = "× Reddet"; red.className = "red"; red.disabled = eslesme.durum === "reddedildi";
    const beklet = document.createElement("button"); beklet.type = "button"; beklet.textContent = "↶ Öneriye al"; beklet.className = "beklet"; beklet.disabled = eslesme.durum === "oneri";
    [onay, red, beklet].forEach((dugme) => { dugme.addEventListener("click", async () => {
      aksiyon.querySelectorAll("button").forEach((x) => { x.disabled = true; });
      try { await deneyimDurumuKaydet(deneyim.id, eslesme.il, dugme === onay ? "onayli" : dugme === red ? "reddedildi" : "oneri"); }
      catch (hata) { alert(hata.message); await deneyimleriYukle(); }
    }); });
    aksiyon.append(onay, red, beklet); satir.append(bilgi, aksiyon); ilListesi.appendChild(satir);
  });
  if (!deneyim.iller.length) ilListesi.innerHTML = '<p class="bos-veri">Bu filtrede eşleşme görünmüyor.</p>';

  const ekleme = document.createElement("form"); ekleme.className = "deneyim-il-ekle";
  const secim = document.createElement("select"); secim.setAttribute("aria-label", "İl seç");
  const baslangic = document.createElement("option"); baslangic.value = ""; baslangic.textContent = "Başka bir il ekle…"; secim.appendChild(baslangic);
  const mevcutIller = new Set(deneyim.iller.map((x) => x.il));
  tumIller.filter((il) => !mevcutIller.has(il)).forEach((il) => { const o = document.createElement("option"); o.value = il; o.textContent = il; secim.appendChild(o); });
  const ekle = document.createElement("button"); ekle.type = "submit"; ekle.textContent = "+ Öneri olarak ekle";
  ekleme.append(secim, ekle);
  ekleme.addEventListener("submit", async (olay) => {
    olay.preventDefault(); if (!secim.value) return;
    ekle.disabled = true;
    try { await deneyimDurumuKaydet(deneyim.id, secim.value, "oneri"); }
    catch (hata) { alert(hata.message); ekle.disabled = false; }
  });
  govde.append(ilListesi, ekleme); kart.appendChild(govde);
  return kart;
}

async function deneyimleriYukle() {
  const alan = document.getElementById("deneyimListesi");
  const q = document.getElementById("deneyimArama").value.trim();
  const durum = document.getElementById("deneyimDurum").value;
  alan.setAttribute("aria-busy", "true");
  const yanit = await fetch(`/admin/api/deneyimler?q=${encodeURIComponent(q)}&durum=${encodeURIComponent(durum)}`, { credentials: "same-origin" });
  if (yanit.status === 401) { location.href = "/admin/giris"; return; }
  if (!yanit.ok) throw new Error(`Deneyim API: ${yanit.status}`);
  const veri = await yanit.json();
  deneyimOzetiniCiz(veri.ozet); alan.innerHTML = "";
  veri.deneyimler.forEach((deneyim) => alan.appendChild(deneyimKartiniOlustur(deneyim, veri.iller)));
  if (!veri.deneyimler.length) alan.innerHTML = '<p class="bos-veri">Bu aramayla eşleşen deneyim bulunamadı.</p>';
  alan.setAttribute("aria-busy", "false");
  document.getElementById("deneyimHaritasi").setAttribute("aria-busy", "false");
}

document.getElementById("deneyimArama").addEventListener("input", () => {
  clearTimeout(deneyimAramaZamanlayici); deneyimAramaZamanlayici = setTimeout(() => deneyimleriYukle().catch(console.error), 250);
});
document.getElementById("deneyimDurum").addEventListener("change", () => deneyimleriYukle().catch(console.error));
document.getElementById("yuksekGuvenOnayla").addEventListener("click", async () => {
  if (!confirm("Güveni %85 ve üzerindeki bütün bekleyen eşleşmeler onaylansın mı?")) return;
  const dugme = document.getElementById("yuksekGuvenOnayla"); dugme.disabled = true;
  try {
    const yanit = await fetch("/admin/api/deneyimler/toplu-onay", { method:"POST", credentials:"same-origin", headers:{"Content-Type":"application/json","X-CSRF-Token":adminCsrf}, body:JSON.stringify({esik:0.85}) });
    const veri = await yanit.json(); if (!yanit.ok) throw new Error(veri.hata || "Toplu onay başarısız");
    alert(`${veri.onaylanan} eşleşme onaylandı.`); await deneyimleriYukle();
  } catch (hata) { alert(hata.message); } finally { dugme.disabled = false; }
});

paneliYukle().catch((hata) => {
  console.error(hata);
  const uyari = document.createElement("div"); uyari.className = "admin-uyari"; uyari.innerHTML = '<strong>Analitik bölüm yüklenemedi</strong><span>Uygulama günlüğünü kontrol et.</span>';
  document.getElementById("adminGovde").prepend(uyari);
});
deneyimleriYukle().catch((hata) => {
  console.error(hata); document.getElementById("deneyimListesi").innerHTML = '<div class="admin-uyari"><strong>Deneyimler yüklenemedi</strong><span>Uygulama günlüğünü kontrol et.</span></div>';
});
