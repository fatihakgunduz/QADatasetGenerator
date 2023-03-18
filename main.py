# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 15:25:23 2023

@author: batuh
"""

import json
import glob

# klasör yolunu belirle
#klasor_yolu = "./"

# tüm text dosyalarını bul
dosya_listesi = glob.glob("*.txt")

# sonuçları saklamak için boş bir sözlük oluştur
sonuclar = {}

# her dosya için işlem yap
for dosyalar in dosya_listesi:
    with open(dosyalar, "r", encoding="utf-8") as dosya:
        context = ""
        soru = ""
        cevap = ""
        soru_cevap_id = 1
        sonuclar[dosyalar] = {}
        
        for satir in dosya:
            if satir.startswith("Hukuki metin(Context):"):
                context = satir[22:].strip()
            elif satir.startswith("Soru:"):
                soru = satir[5:].strip()
            elif satir.startswith("Cevap:"):
                cevap = satir[6:].strip()   
                
                # sonuçları dictionary'e ekle
                sonuclar[dosyalar][str(soru_cevap_id)] = {}
                sonuclar[dosyalar][str(soru_cevap_id)] = {"Context": context, "Soru": soru, "Cevap": cevap}
                soru_cevap_id += 1

# sonuçları dosyaya yaz
with open("dataset.json", "w") as dosya:
    json.dump(sonuclar, dosya)