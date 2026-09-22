"""Kotasız mekân anlatımı için doğrulanması kolay, sabit prototip metinleri."""

KAYITLAR = {
    "ayasofya": {
        "tr": ("Ayasofya, yüzyıllar boyunca farklı dönemlerin izlerini aynı kubbe altında taşıyan İstanbul'un en tanınmış yapılarındandır.", "Kubbenin altında durduğunda yalnız taşlara değil, şehrin değişen yüzyıllarına da bakarsın. Mozaikleri, mermer yüzeyleri ve yapının farklı dönemlerden kalan katmanlarını acele etmeden incele."),
        "en": ("Hagia Sophia is one of Istanbul's best-known monuments, carrying traces of different eras beneath the same dome.", "Under its dome you are not only looking at stone, but at centuries of a changing city. Notice the mosaics, marble surfaces and layers left by different periods."),
    },
    "sultanahmet-camii": {
        "tr": ("Sultanahmet Camii, altı minaresi ve iç mekânındaki İznik çinileriyle İstanbul'un klasik Osmanlı mimarisinin önemli örneklerindendir.", "Avludan kubbelerin yükselişini izle; içeride ise çinilerin desenlerine ve ışığın mekâna nasıl yayıldığına dikkat et. İbadet saatlerinde sessiz ol, kıyafet kurallarına ve görevlilerin yönlendirmesine uy."),
        "en": ("The Blue Mosque is a major example of classical Ottoman architecture, known for its six minarets and İznik tiles.", "Watch the domes rise from the courtyard, then notice the tile patterns and the changing light inside. Remain quiet during prayer and follow dress rules and staff guidance."),
    },
    "yerebatan-sarnici": {
        "tr": ("Yerebatan Sarnıcı, Bizans döneminde şehrin su ihtiyacını desteklemek için yapılmış büyük bir yeraltı yapısıdır.", "Sütunların suya düşen yansımalarını izle ve farklı yapılardan yeniden kullanıldığı düşünülen başlıklara dikkat et. Medusa başlarını görmeden çıkma; zemin ıslak olabileceği için sakin yürü."),
        "en": ("The Basilica Cistern is a vast Byzantine underground structure built to support the city's water supply.", "Watch the columns reflected in the water and notice capitals thought to have been reused from earlier buildings. Do not miss the Medusa heads, and walk carefully on damp surfaces."),
    },
    "topkapi-sarayi": {
        "tr": ("Topkapı Sarayı, Osmanlı yönetiminin ve saray yaşamının yüzyıllar boyunca merkezlerinden biri olmuştur.", "Saray tek bir bina değil, avlular boyunca açılan bir dünyadır. Divan, mutfaklar, koleksiyonlar ve Boğaz manzarası için en az birkaç saat ayır; Harem için ayrı bilet ve sıra olabileceğini kontrol et."),
        "en": ("Topkapı Palace was one of the centers of Ottoman government and court life for centuries.", "It is not a single building but a world unfolding through courtyards. Allow several hours for the council spaces, kitchens, collections and Bosphorus views; check whether the Harem requires a separate ticket."),
    },
    "gulhane-parki": {
        "tr": ("Gülhane Parkı, Topkapı Sarayı'nın dış bahçeleriyle ilişkili tarihî bir yeşil alandır.", "Yoğun tarih rotasının arasında burada soluklan. Ağaçlı yolları takip edip Sarayburnu yönüne yürüyebilir, bahar aylarında çiçek düzenlemelerini görebilirsin."),
        "en": ("Gülhane Park is a historic green space connected with the outer gardens of Topkapı Palace.", "Pause here between major monuments. Follow its tree-lined paths toward Sarayburnu and look for seasonal flower displays in spring."),
    },
    "istanbul-arkeoloji-muzeleri": {
        "tr": ("İstanbul Arkeoloji Müzeleri, farklı coğrafya ve dönemlerden eserleri bir araya getiren önemli bir müze topluluğudur.", "Her salonu hızla bitirmeye çalışma. İlgini çeken bir dönem seç; lahitler, heykeller, yazıtlar ve çiniler arasında birkaç esere uzun süre bakmak daha iyi bir deneyim verir."),
        "en": ("The Istanbul Archaeological Museums bring together important objects from many regions and historical periods.", "Do not rush every gallery. Choose a period that interests you and spend longer with a few sarcophagi, sculptures, inscriptions or tiles."),
    },
}


def anlat(slug, ad, mod, dil="tr"):
    kayit = KAYITLAR.get(slug)
    if not kayit:
        return None
    kisa, detay = kayit.get(dil, kayit.get("en"))
    if mod == "kisa":
        metin = kisa
    elif mod == "hikaye":
        giris = "Ey yolcu, bu mekâna benimle yaklaş: " if dil == "tr" else "Traveler, approach this place with me: "
        metin = f"{giris}{kisa} {detay}"
    else:
        baslik = "Dikkat etmen gerekenler: " if dil == "tr" else "What to notice: "
        metin = f"{kisa}\n\n{baslik}{detay}"
    return {"reply": metin, "kaynak_turu": "yerel-katalog", "yer": ad}
