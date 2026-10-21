#!/usr/bin/env python3
"""Commit öncesi doğrulama: etiket dengesi, iç bağlantılar, DOCTYPE.

Kullanım:  python3 dogrula.py        (depo kökünden)

Hiçbir bağımlılığı yok. Regex ile etiket saymak HTML yorumlarının içindeki
etiket görünümlü metinler yüzünden yanlış alarm veriyordu; bu yüzden gerçek
bir ayrıştırıcı (HTMLParser) kullanıyor.
"""

import os
import sys
from html.parser import HTMLParser

KOK = os.path.dirname(os.path.abspath(__file__))

# Kapanışı olmayan etiketler
BOS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

hatalar = []
uyarilar = []


class Denge(HTMLParser):
    """Etiket yığınını takip eder, eşleşmeyenleri bildirir."""

    def __init__(self, yol):
        super().__init__(convert_charrefs=True)
        self.yol = yol
        self.yigin = []
        self.baglantilar = []   # (satır, href/src)

    def handle_starttag(self, etiket, ozellikler):
        d = dict(ozellikler)
        for anahtar in ("href", "src"):
            if d.get(anahtar):
                self.baglantilar.append((self.getpos()[0], d[anahtar]))
        if etiket not in BOS:
            self.yigin.append((etiket, self.getpos()[0]))

    def handle_startendtag(self, etiket, ozellikler):
        self.handle_starttag(etiket, ozellikler)
        if etiket not in BOS and self.yigin and self.yigin[-1][0] == etiket:
            self.yigin.pop()

    def handle_endtag(self, etiket):
        if etiket in BOS:
            return
        if not self.yigin:
            hatalar.append(
                "%s:%d  fazla kapanış </%s>" % (self.yol, self.getpos()[0], etiket)
            )
            return
        if self.yigin[-1][0] == etiket:
            self.yigin.pop()
            return
        # Yığında geride kalmış mı? Varsa aradakiler kapatılmamış.
        for i in range(len(self.yigin) - 1, -1, -1):
            if self.yigin[i][0] == etiket:
                for ad, satir in self.yigin[i + 1:]:
                    hatalar.append(
                        "%s:%d  <%s> kapatılmamış (</%s> ile karşılaştı)"
                        % (self.yol, satir, ad, etiket)
                    )
                del self.yigin[i:]
                return
        hatalar.append(
            "%s:%d  </%s> açılmamış" % (self.yol, self.getpos()[0], etiket)
        )


def hedef_var(href):
    """İç bağlantının karşılığı depoda var mı?"""
    yol = href.split("#")[0].split("?")[0]
    if not yol:
        return True
    tam = os.path.join(KOK, yol.lstrip("/"))
    if yol.endswith("/") or os.path.isdir(tam):
        return os.path.isfile(os.path.join(tam, "index.html"))
    return os.path.exists(tam)


def dosyalari_bul():
    for kok, klasorler, dosyalar in os.walk(KOK):
        klasorler[:] = [k for k in klasorler if k not in (".git", "node_modules")]
        for d in sorted(dosyalar):
            if d.endswith(".html"):
                yield os.path.join(kok, d)


def main():
    sayac = 0
    for tam in sorted(dosyalari_bul()):
        goreli = os.path.relpath(tam, KOK)
        sayac += 1
        with open(tam, encoding="utf-8") as f:
            metin = f.read()

        # DOCTYPE en başta olmalı — önünde boşluk bile quirks mode'a düşürüyor
        if not metin.startswith("<!DOCTYPE html>"):
            hatalar.append(
                "%s:1  dosya <!DOCTYPE html> ile başlamıyor (%r ile başlıyor)"
                % (goreli, metin[:20])
            )

        ayristirici = Denge(goreli)
        ayristirici.feed(metin)
        ayristirici.close()
        for ad, satir in ayristirici.yigin:
            hatalar.append("%s:%d  <%s> hiç kapatılmamış" % (goreli, satir, ad))

        # Yalnız iç bağlantılar; http(s), mailto, data, # atlanıyor
        for satir, href in ayristirici.baglantilar:
            if href.startswith(("http://", "https://", "//", "mailto:", "tel:",
                                "data:", "#")):
                continue
            if not hedef_var(href):
                hatalar.append("%s:%d  kırık bağlantı → %s" % (goreli, satir, href))
            if "OYNATMA_LISTESI_ID" in href:
                uyarilar.append("%s:%d  yer tutucu bağlantı → %s"
                                % (goreli, satir, href))

    # Yer tutucular dış bağlantılarda da olabilir, ayrıca tara
    for tam in sorted(dosyalari_bul()):
        goreli = os.path.relpath(tam, KOK)
        with open(tam, encoding="utf-8") as f:
            for no, satir in enumerate(f, 1):
                if "OYNATMA_LISTESI_ID" in satir:
                    kayit = "%s:%d  yer tutucu: OYNATMA_LISTESI_ID" % (goreli, no)
                    if kayit not in uyarilar:
                        uyarilar.append(kayit)

    if not os.path.isfile(os.path.join(KOK, "CNAME")):
        hatalar.append("CNAME dosyası yok — özel alan adı düşer")

    print("%d HTML dosyası tarandı." % sayac)
    for u in uyarilar:
        print("  uyarı:  " + u)
    if hatalar:
        print("\n%d HATA:" % len(hatalar))
        for h in hatalar:
            print("  " + h)
        return 1
    print("Temiz.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
