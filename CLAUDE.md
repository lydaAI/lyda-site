# Lyda AI — site (lyda.info)

Bu dosya, depoda çalışacak her Claude Code oturumu için bağlam. Sohbet geçmişi
olmadan da projeye devam edilebilsin diye yazıldı. Bir karar değişirse burayı da
güncelle, yoksa bir sonraki oturum eski kurala göre çalışır.

## Proje

**Lyda AI**, temelinde Türkçe yapay zekâ — özellikle ComfyUI — içeriği üreten bir
YouTube kanalı. Bu depo kanalın web yüzü: bağlantı paneli + ComfyUI rehberi +
çalışan araçlar. Hedef kitle Türkçe konuşan, ComfyUI'a yeni başlayan insanlar.

İçerik **ComfyUI'a sıkıştırılmamalı** — kanal daha geniş bir yapay zekâ
alanını kapsıyor, site de buna yer bırakacak şekilde kurulmalı.

Dil: **tamamı Türkçe**. Kod içindeki değişken/sınıf adları da Türkçe
(`.baglantilar`, `--kirmizi`, `hesapla()`). Yeni kod yazarken bu düzeni koru,
İngilizce sınıf adı karıştırma.

## Yayın

GitHub Pages, `lydaAI/lyda-site`, `main` / `(root)`. **`main`'e push = canlı.**
Ara aşama, staging, build adımı yok. Yayın 30–60 saniye içinde geçer.

- `CNAME` dosyası `lyda.info` içerir — **silme, değiştirme.** Silinirse özel
  alan adı düşer.
- Kayıt şirketi Squarespace (Google Domains göçünden miras).
- Apex A kayıtları: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
  `185.199.111.153`. `www` CNAME → `lydaai.github.io`.
- Mail: Google Workspace, `lyda@lyda.info`. MX `smtp.google.com` (öncelik 1),
  SPF `v=spf1 include:_spf.google.com ~all`, DKIM `google._domainkey`,
  DMARC `v=DMARC1; p=none; rua=mailto:lyda@lyda.info`. DKIM'in Admin
  Console'dan **başlatılmış** olması gerekiyor, yoksa Google `*.gappssmtp.com`
  adına imzalar ve mailler spama düşer. Bu çözüldü; bir daha spam sorunu olursa
  ilk bakılacak yer burası.

## Dosya ve URL haritası

```
index.html                   → lyda.info            ana sayfa
sozluk/index.html            → /sozluk/             45 terimlik ComfyUI sözlüğü
rehber/index.html            → /rehber/             rehber yol haritası
araclar/stil.css             →                      araç + rehber sayfalarının paylaşılan stili
araclar/cozunurluk/          → /araclar/cozunurluk/ çözünürlük seçici
araclar/model-adi/           → /araclar/model-adi/  model dosya adı çözücü
araclar/hatalar/             → /araclar/hatalar/    hata sözlüğü
gorseller/01.jpg … 09.jpg    →                      arka plandaki akan görsel duvarı
paylasim.png                 →                      1200×624 sosyal kart
favicon*.{ico,png}           →                      site ikonları
CNAME                        →                      özel alan adı (dokunma)
dogrula.py                   →                      commit öncesi doğrulama betiği
```

## Marka

**Renkler** (`:root`, her sayfada aynı):

| Değişken | Değer | Kullanım |
|---|---|---|
| `--siyah` | `#0A0A0A` | zemin |
| `--beyaz` | `#FFFFFF` | ana metin |
| `--kirmizi` | `#E8332C` | tek vurgu rengi — kablo, simgeler, aktif süzgeç |
| `--gri` | `#2B2B2B` | çerçeve, ayırıcı |
| `--acikgri` | `#8F8F8F` | ikincil metin |
| `--sonuk` | `#5E5E5E` | en soluk metin (yalnız `stil.css`) |

Markanın asıl paletindeki `#E5E5E5` siyah üstünde ikincil metin için fazla
parlak kaldığı için `--acikgri` ve `--sonuk` sonradan eklendi. **Kırmızı tek
vurgu rengi** — ikinci bir aksan rengi ekleme.

**Yazı tipleri** (Google Fonts):
- Fraunces 600 — başlıklar, `font-variation-settings:"SOFT" 40,"WONK" 1`
- IBM Plex Sans 400/500 — gövde

**Simgeler**: Font Awesome 6.5.2, cdnjs'ten. Hugging Face logosu FA'da yok,
`svg.hf` olarak satır içi SVG gömülü.

**Ses tonu**: samimi ama abartısız, ikinci tekil şahıs ("öğren", "kur").
Pazarlama dili, ünlem yağmuru, emoji yok.

## Tasarım dili

Sayfanın omurgası **dikey kırmızı bir "kablo"** ve üstündeki içi boş node
noktaları — ComfyUI'ın node grafiğine gönderme. Yeni bir bölüm eklerken bu
metaforu sürdür, paralel ikinci bir görsel sistem kurma. (Bir kez yatay kart
şeridi denendi, tam da bu yüzden reddedildi.)

Ana sayfanın iki alanı var ve **birbirine karışmamalı**: üstte YouTube/kanal
bağlantı paneli, altta ComfyUI rehberi. Aralarında `.ayrac` var — iki yana
solan 1px çizgi ve ortada içi boş kırmızı node noktası (kablonun noktalarıyla
aynı dil).

Arka plan: 5 kolon halinde akan görsel duvarı (`.fon`), üstünde ortası
koyulaştırılmış perde (`.perde`) — metin görselin üstünde okunabilsin diye.
Ayarlanabilir tek düğme `--fon-perde` (şu an `.76`). Yükseltirsen görseller
belirginleşir, metin okunaksızlaşır.

Bilinen CSS incelikleri — bozmadan önce nedenini bil:
- Akordeonlarda yumuşak yükseklik için `grid-template-rows: 0fr → 1fr`.
- `scroll-snap` kapsayıcı dolgusunu yiyor; `scroll-padding-inline` ile çözüldü.
- Mobil medya sorgusu `.uc{top:1.32rem}`'den **sonra** gelmeli, yoksa kaynak
  sırasında kaybediyor ve kablo noktaları yanlarda kalıyor.
- `@view-transition { navigation: auto }` sayfalar arası geçiş için — yalnız
  Chrome/Edge'de çalışır, diğerlerinde sessizce düşer.
- Türkçe arama her yerde `toLocaleLowerCase("tr")` ile ("İ" sorunu).
- `prefers-reduced-motion` altında bütün animasyonlar sıfırlanıyor; yeni
  animasyon eklersen oraya da ekle.

## Kod düzeni

Build adımı, bağımlılık, framework **yok** — düz HTML/CSS/JS. Öyle kalsın;
bir araç zinciri eklemek bu projenin boyutuna göre net bir kayıp.

- `index.html` ve `sozluk/index.html`: stil satır içi `<style>` bloğunda.
- `rehber/` ve `araclar/*/`: paylaşılan `/araclar/stil.css` + sayfaya özel
  satır içi ek. Ortak jetonları (`.sayfa`, `.geri`, `h1`, `.panel`, `.tablo`,
  `.secenek`, `footer`, `.komsu`) orada ara, kopyalama.
- JS yok denecek kadar az ve ES5 ağırlıklı (`var`, fonksiyon bildirimi). Mevcut
  dosyalarda bu üslubu sürdür.
- Dış bağlantılar her zaman `target="_blank" rel="noopener"`.
- Sayfa `<!DOCTYPE html>` ile başlamalı, önünde tek boşluk bile olmasın
  (quirks mode'a düşüyor — bir kez oldu).

## Çalışma kuralları

Bu bölüm Emir'le çalışırken öğrenilenler. Teknik kurallar kadar bağlayıcı.

1. **Soru sorulduğunda değişiklik yapma.** "Şu nasıl olur?", "bu ne?",
   "başvuru ne tam olarak?" — bunlar soru. Cevap ver, dur, onay bekle. İki kez
   bu yüzden fırça yedim: *"Oğlum niye hemen değiştirdin amk soru sormuştum."*
2. **Belirsiz sinyalle silme.** "Şuan yok" bir şeyin kaldırılması talebi
   değildi; oynatma listesi satırını ve X simgesini silince *"lan niyer sildin
   kalsın öyle"* geldi. Silmek geri alması en pahalı iş; emin değilsen sor.
3. **Dürüst teşhis koy.** Beğenmediği bir tasarımda "neden olmadığını" açıkça
   söylemek işe yarıyor; savunmak yaramıyor.
4. **Darboğazı hatırlat.** Sitenin cilası değil, **video içeriği** eksik. Site
   işi sonsuza kadar genişletilebilir; buna harcanan zaman içerikten çalıyor.
5. **Kendi alanında ona güven.** Sözlük, hata açıklamaları, model adı
   çözümlemeleri benim yazdığım metinler ama **onun** alanı — doğruluk
   kontrolü ondan geçmeli.
6. Windows uzantıları gizliyor: dosya adı isterken `01.jpg` gibi tam ad verme,
   `01` de — yoksa `01.jpg.jpg` oluyor (bir kez oldu).

## Değişiklik öncesi doğrulama

Her commit öncesi:

```bash
python3 dogrula.py          # etiket dengesi + iç bağlantılar + DOCTYPE
```

Görsel kontrol için yerel sunucu:

```bash
python3 -m http.server 8777     # depo kökünden
```

Playwright ile ekran görüntüsü alırken iki tuzak var:
- Chromium `/opt/pw-browsers/` altında, `executablePath` ile verilmeli;
  `playwright install` **çalıştırma**.
- Bu kutuda bütün CDN'ler (cdnjs/jsdelivr/unpkg) ve `lyda.info` 403 dönüyor.
  Font Awesome'ı görebilmek için `context.route()` ile CSS ve webfont
  isteklerini `node_modules/@fortawesome/fontawesome-free` içinden karşıla.
  npm ve GitHub erişimi açık.

## Commit

Mesajlar Türkçe, emir kipi, tek satır: *"İki alan arasına ayraç ekle"*,
*"Hata sözlüğü aracı ekle"*. Gövde gerekiyorsa boş satırdan sonra.

Commit'in "Verified" görünmesi için yazar `Claude <noreply@anthropic.com>`
olmalı. Yanlış yazarla commit attıysan:
`git commit --amend --no-edit --reset-author`.

## Bilinen eksikler ve yer tutucular

Bunlar **canlıda** ve gerçek değerle doldurulmayı bekliyor:

- `index.html` oynatma listesi bağlantısı: `playlist?list=OYNATMA_LISTESI_ID`
  — gerçek liste kimliği yok.
- `discord.gg/lyda` — davet bağlantısının doğruluğu teyit edilmedi.
- Rehber bölümlerinin 7'si "yakında" etiketli; içerik yok. İlk bölümler
  yayınlanınca varsayılan süzgeç `Hepsi` yerine `Başlangıç` olacak (tek
  satırlık değişiklik, kararlaştırıldı).
- "Modeller" konu başlığı benim koyduğum geçici bir ad; değişebilir.
- Rehber bölüm simgeleri geçici.
- `og:url` `https://lyda.info` (sonda eğik çizgi yok), canlı bağlantı
  `lyda.info/` olarak görünüyor — kozmetik tutarsızlık, dokunulmadı.
- Maskot (kedi) sitede kullanılmıyor; yalnız `paylasim.png` içinde var.

## Sırada ne var

Emir'in onayladığı ama **girdi beklediği** işler:

- **Sampler/scheduler karşılaştırma aracı** — sabit seed'de örnek görsel
  ızgarasını onun üretmesi lazım.
- **Workflow galerisi** — onun `.json` workflow dosyaları lazım.
- Sözlük / hata sözlüğü / model adı metinlerinin doğruluk kontrolü.
