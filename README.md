# Evliya Çelebi AI

Yabancı turistlerle kendi dillerinde sohbet edip Türkiye'yi tanıtan, Evliya
Çelebi karakterli bir web uygulaması. Motor `evliya_test.py`'de test edilmiş
(10/10) sistem promptu ve model yedekleme mantığını kullanır; bu proje o
motoru bir Flask backend + sade HTML/CSS/JS frontend'e taşır.

## Kurulum

1. Bağımlılıkları kur:

   ```bash
   pip install -r requirements.txt
   ```

2. `.env.example` dosyasını `.env` olarak kopyala ve kendi Gemini API
   anahtarınla değiştir:

   ```
   GEMINI_API_KEY=senin_anahtarin
   ```

   `.env` ve `assets/` klasörü `.gitignore` içinde — anahtar ve görseller
   repoya asla gitmez.

## Çalıştırma

```bash
python app.py
```

Sunucu `http://127.0.0.1:5000` adresinde açılır. Tarayıcıda bu adrese
gidince sohbet ekranı gelir.

### API kotası olmadan arayüz testi

Sohbet başlığındaki **Demo: Kapalı** düğmesine basınca yerel demo modu açılır.
Bu mod Gemini'ye hiç istek göndermez; tarih, doğa/sakinlik ve gastronomi
ifadelerine göre hazır örnek cevaplar üretir. Görseller, mekân kartları, rota,
harita, gün atama, mesafe hesabı ve paylaşım kartı bu şekilde sınırsız test
edilebilir. Gerçek yapay zekâyı kullanmak için aynı düğmeyle demo modunu tekrar
kapat. Tercih yalnızca tarayıcıda saklanır.

### Yakınımda modu

Seyahat Defteri'ndeki **Yakınımda** sekmesi, kullanıcı düğmeye bastığında
tarayıcıdan konum izni ister ve seçilen 1, 3 veya 5 km çevredeki müze, tarihî
yapı, ibadet yeri, park ve manzara noktalarını gösterir. Konum kalıcı olarak
saklanmaz. Sonuçlarda kuş uçuşu mesafe, yaklaşık yürüme süresi, yol tarifi ve
**Rotama ekle** işlemi bulunur.

Canlı sonuçlar küçük ve süre sınırı olan bir OpenStreetMap Overpass sorgusuyla
alınır ve aynı bölge için 10 dakika bellekte tutulur. Demo Modu açıkken konum
izni ve dış servis kullanılmadan Sultanahmet çevresindeki örnek noktalar gelir.

### Telefondan açma (aynı Wi-Fi üzerinden)

Sunucu `host="0.0.0.0"` ile başladığı için aynı Wi-Fi ağındaki bir telefon
da bilgisayarın yerel IP adresi üzerinden siteye girebilir:

1. Bilgisayarın yerel IP adresini öğren:

   ```powershell
   ipconfig
   ```

   "IPv4 Address" satırındaki değeri kullan (örn. `192.168.1.24`).

2. `python app.py` ile sunucuyu başlat.

3. Telefonun **bilgisayarla aynı Wi-Fi ağına** bağlı olduğundan emin ol,
   sonra telefon tarayıcısında şu adresi aç:

   ```
   http://192.168.1.24:5000
   ```

   (IP'yi kendi bilgisayarınınkiyle değiştir.)

   Windows Güvenlik Duvarı ilk bağlantıda izin isteyebilir; "İzin ver"i
   seç. Görünmüyorsa bilgisayar ve telefonun gerçekten aynı ağda olduğunu
   ve güvenlik duvarının 5000 portunu engellemediğini kontrol et.

## Yeni Yolculuk akışı

Sohbetin üstündeki **Yeni Yolculuk** düğmesi; gün sayısı, başlangıç şehri,
ilgi alanı ve gezi temposunu sorar. Ardından üç rota omurgası sunar. Seçilen
rota mevcut `/sohbet` motoruna gönderilir; Evliya rotayı gün gün, yöresel
tatlar ve yerel deneyimlerle ayrıntılandırır. Yeni yolculuk açıldığında önceki
oturumun sohbeti, gezgin profili ve seyahat defteri tarayıcı içinde sıfırlanır.

## Kültürel Merak Motoru

**Meraklar** sekmesi, `meraklar.json` kataloğundaki çok dilli kültür
sorularını sohbetin dili, panel temaları ve bahsedilen yerlere göre sıralar.
Karta dokunulduğunda soru mevcut Evliya sohbetine gönderilir.

İlk açılışta anonim eğilim paylaşımı için açık izin sorulur. İzin verilirse
`merak_db.py`, SQLite tabanlı `evliya.db` dosyasına yalnızca rastgele oturum
kimliği, dil, isteğe bağlı ülke ve `cami-ziyareti` gibi katalog konu slug'ını
yazar. Ham mesaj, ad, IP veya kesin konum kaydedilmez. İzin reddedildiğinde
Meraklar özelliği çalışır fakat hiçbir eğilim ya da geri bildirim saklanmaz.

- `GET /meraklar` — dil, tema ve yer bağlamına göre öneriler
- `POST /geri-bildirim` — yalnızca izinli oturumlarda yararlı/yararsız sinyali
- `POST /sohbet` — cevaba `merak_onerileri` ve eşleşirse `merak_konusu` ekler

## Yönetim paneli

Anonim merak eğilimleri parola korumalı `/admin` adresinden izlenir. Giriş
yapılmamış bir ziyaretçi otomatik olarak `/admin/giris` adresine yönlendirilir;
analitik API de oturumsuz isteklere `401` döner.

`.env` dosyasına iki değer ekle:

```env
ADMIN_PASSWORD=buraya_guclu_bir_parola_yaz
FLASK_SECRET_KEY=buraya_uzun_rastgele_bir_deger_yaz
```

Uygulamayı yeniden başlattıktan sonra `http://127.0.0.1:5000/admin` adresine
git ve `ADMIN_PASSWORD` değerini kullan. Oturum sekiz saat geçerlidir; panelin
sağ üstündeki **Çıkış** düğmesi oturumu hemen kapatır. Panel internete
açılacaksa HTTPS kullanılmalı ve bu iki değer güçlü, benzersiz tutulmalıdır.

Panel; toplam anonim merak, izinli oturum, 7/30 günlük hareket, dil dağılımı,
gizlilik eşiğini geçen ülke grupları, en sık konular ve yararlı cevap oranını
gösterir. Beşten az kayıt içeren ülke grupları anonimlik için gösterilmez.

### Deneyim Haritası

GoTürkiye deneyim listesindeki 61 başlık, özgün Excel dosyası değiştirilmeden
`deneyimler.json` kataloğuna aktarılır. Bir deneyim tek bir ile zorlanmaz:
uygun olduğunda aynı deneyim birden çok ille eşleşebilir. Örneğin gastronomi,
UNESCO ve doğa başlıkları birden fazla il içerirken Efes gibi belirli bir yere
ait deneyimler tek ille başlayabilir.

Kaynak Excel ve ondan türetilen tam `deneyimler.json` özel tutulur; GitHub
deposuna eklenmez. Bu katalog bulunmayan yeni kurulumlarda yönetici paneli
boş deneyim tablolarıyla açılır, uygulamanın diğer bölümleri çalışır. Kataloğu
yerel proje klasörüne ekleyip uygulamayı yeniden başlatınca kayıtlar içe alınır.

İlk eşleşmeler editoryal **öneri** durumundadır; doğrulanmış bilgi sayılmaz.
Yönetici panelindeki **Deneyim Haritası** bölümünden her il eşleşmesi ayrı ayrı
onaylanabilir, reddedilebilir veya yeniden öneri durumuna alınabilir. Yönetici
ayrıca deneyime yeni bir il ekleyebilir. Yüksek güvenli öneriler için toplu
onay düğmesi vardır; düşük güvenli ve genel başlıkların elle gözden geçirilmesi
önerilir.

Veriler mevcut `evliya.db` içinde çoktan çoğa ilişkili iki tabloda tutulur:

- `deneyimler` — deneyimin Türkçe/İngilizce adı ve tema etiketleri
- `deneyim_il_eslesmeleri` — il, güven puanı, kaynak notu ve yönetici kararı

Bu yapı daha sonra Evliya'nın önerilerini yalnızca genel ilgi alanına değil,
onaylanmış deneyim-il ilişkilerine göre önceliklendirmek için kullanılabilir.

## Yapı

- `app.py` — Flask backend. `SISTEM_PROMPTU` ve `llm_cevapla` mantığı
  `evliya_test.py`'den olduğu gibi taşındı (model yedekleme zinciri,
  429/503/404 davranışları, JSON parse, panel varsayılanları).
- `POST /sohbet` — `{mesaj, gecmis}` alır, Gemini'ye sistem promptu +
  konuşma geçmişiyle gider, `{reply, panel, medyalar, rota}` döner.
- `assets.json` — görsel katalogu (yer/tema etiketleri). Yoksa `app.py`
  ilk çalıştırmada 5-6 kayıtlık bir örnek oluşturur.
- `assets/` — katalogdaki görseller (şimdilik basit SVG yer tutucular).
  Panelde geçen `yerler` ile eşleşen görsel +3 puan, `temalar` eşleşmesi +1
  puan alır; en yüksek puanlı 3 görsel `medyalar` olarak döner. Hiçbir
  eşleşme yoksa `genel: true` etiketli joker görsel(ler) döner.
- `static/` — tek sayfalık frontend (`index.html`, `style.css`, `app.js`).
  Sol tarafta sohbet, sağ tarafta "Seyahat Defteri" paneli (görseller +
  varsa sıralı rota listesi).

## Gitmeden Önce kartları

Günlük plan durakları ve Mobil Seyahat Modu; alan tipi, önerilen ziyaret
zamanı, çocuklarla kullanım, erişilebilirlik, rezervasyon, ziyaret adabı ve
resmî kaynak bağlantısını açılır bir kartta gösterir. Bu içerik
`mekan_rehber.py` tarafından üretilir. Saat, ücret, bilet uygunluğu ve erişim
koşulları değişken kabul edilir; kesin değer saklanmaz ve kullanıcı resmî
kaynağa yönlendirilir. Karttaki son kontrol tarihi operasyon bilgilerinin
güncellik garantisi değil, genel rehber metninin editoryal kontrol tarihidir.

## Doğrulanmış kültür bilgisi

`kultur-bilgileri.json`, Evliya'nın kültürel sorulara verdiği cevapları
destekleyen editoryal bilgi kataloğudur. Her kayıtta konu slug'ı, doğrulanmış
olgular, ziyaret adabı, kaynaklar, inceleme durumu ve son kontrol tarihi bulunur.
Yalnızca `onayli` durumundaki kayıtlar Gemini'ye ek bağlam olarak verilir;
`incelemede` durumundaki bilgiler kesin gerçek gibi modele aktarılmaz.

Kültürel bir konu eşleştiğinde sohbet cevabında açılır bir **Kaynakları göster**
alanı görünür. Buradaki bağlantılar doğrudan ilgili kurum sayfasına gider.
Yönetim panelindeki **İçerik Sağlığı** bölümü; onaylı, incelemede, kaynaksız ve
180 günden eski kayıt sayılarını gösterir. Yeni bir kültür kaydı eklerken önce
`incelemede` durumunda oluşturup güvenilir birincil kaynaklarla doğruladıktan
sonra `onayli` yapılması önerilir.

- `kultur_bilgi.py` — kataloğu okur, güvenli LLM bağlamını ve istemci kaynak
  bilgisini üretir, içerik sağlığı ölçülerini hesaplar.
- `kultur-bilgileri.json` — kültür konuları ve kaynak kataloğu.
- `POST /sohbet` — eşleşen konu için ayrıca `kultur_kaynagi` döndürür.

Başlangıç kataloğunda 12 konu vardır: 7 konu kaynaklarıyla onaylı, yeterli
birincil kaynak bulunmayan 5 konu ise dürüstçe `incelemede` tutulur.

## Zengin Seyahat Defteri ve düzenlenebilir rota

Seyahat Defteri'ne gelen yerler artık yalnızca fotoğraf olarak değil; şehir,
kategori, önerilen ziyaret süresi ve güncel saat/ücret uyarısı bulunan mekân
kartları olarak gösterilir. Karttaki **Rotama ekle** düğmesi yeri mevcut plana
ekler. Sabit planlama bilgileri `mekan_bilgi.py` içinde tutulur; bilinmeyen
yerler için yanıltıcı güncel bilgi üretmeden güvenli varsayılanlar kullanılır.

Rota durakları günlere atanabilir, yukarı-aşağı taşınabilir ve plandan
çıkarılabilir. Her değişiklikten sonra `POST /rota-detay` yaklaşık mesafeleri,
süreleri ve harita çizimini yeniden hesaplar. Bu değerler yol tarifi değil,
açıkça işaretlenmiş yaklaşık planlama bilgileridir.

## Notlar

- Ücretsiz Gemini katmanı kullanılıyor: `MODELLER` listesindeki modeller
  sırayla denenir; 429/503 hatalarında bekleyip tekrar dener, 404'te
  sıradaki modele geçer.
- `SISTEM_PROMPTU` içeriği değiştirilmedi; konuşma geçmişi her istekte
  `system_instruction` olarak ayrıca gönderilmeye devam eder, geçmiş
  mesajlar `contents` listesine `user`/`model` rolleriyle eklenir.
