# Çocuk Atölyesi – Otomatik Video Kurulumu

Bu klasör her gün 18:00'de (Türkiye saati) bir video üretip YouTube'a yükler.
Şu an 9 günlük içerik hazır (pizza, bisiklet, pasta, robot, hamburger, fincan, dondurma, ayıcık, krep).
Kalan günler yayındayken eklenecek; o zamana kadar hazır videolar sırayla tekrar eder.

## Adım 1 – GitHub'a yükle (terminal gerekmez)
1. github.com'da yeni bir depo (repository) aç. Adı: cocuk-atolyesi. Gizli (Private) olsun.
2. "uploading an existing file" bağlantısına tıkla.
3. Bu klasörün İÇİNDEKİ her şeyi sürükle-bırak yap (fonts klasörü ve .github klasörü dahil).
   Not: .github klasörü Windows'ta gizli görünebilir; Dosya Gezgini > Görünüm > Gizli öğeler'i aç.
4. "Commit changes" düğmesine bas.

## Adım 2 – YouTube izni (bir kerelik, adım adım yanındayım)
Bu adım için Google Cloud Console'da proje açılıp 3 gizli anahtar alınacak:
YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
Hazır olduğunda bana "Adım 2'ye geçelim" yaz, ekran ekran anlatırım.

## Adım 3 – Anahtarları GitHub'a ekle
Depo > Settings > Secrets and variables > Actions > New repository secret
ile üç anahtarı aynı isimlerle ekle.

## Adım 4 – Deneme
Depo > Actions > "Günlük video" > Run workflow. Gizlilik "private" kalsın, gün kutusuna 1 yaz.
Video YouTube Studio'da gizli olarak görünürse sistem çalışıyor demektir.

## Başlangıç tarihi
baslangic.txt dosyasındaki tarihten itibaren her gün sıradaki video üretilir (şu an 2026-10-03).
