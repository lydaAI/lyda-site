# lyda.info

[Lyda AI](https://lyda.info) — Türkçe yapay zekâ ve ComfyUI içeriği üreten
YouTube kanalının sitesi.

- **Ana sayfa** — kanal bağlantıları ve ComfyUI rehber yol haritası
- **[/sozluk/](https://lyda.info/sozluk/)** — ComfyUI terimleri sözlüğü
- **[/rehber/](https://lyda.info/rehber/)** — rehber bölümleri
- **[/araclar/cozunurluk/](https://lyda.info/araclar/cozunurluk/)** — modele göre çözünürlük seçici
- **[/araclar/model-adi/](https://lyda.info/araclar/model-adi/)** — model dosya adı çözücü
- **[/araclar/hatalar/](https://lyda.info/araclar/hatalar/)** — hata sözlüğü

## Geliştirme

Build adımı yok, düz HTML/CSS/JS. Depoyu klonla, yerel sunucu başlat:

```bash
python3 -m http.server 8777
```

Commit öncesi:

```bash
python3 dogrula.py
```

`main`'e push edilen her şey birkaç dakika içinde canlıya geçer (GitHub Pages).

Projenin kuralları, marka paleti ve açık işler [`CLAUDE.md`](CLAUDE.md) içinde.
