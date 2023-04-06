import json
import glob

# tüm text dosyalarını bul
dosya_listesi = glob.glob("*.txt")
soru_cevap_id = 1
checker = []
sonuclar = {}

# her dosya için işlem yap
for dosyalar in dosya_listesi:
    with open(dosyalar, "r", encoding="utf-8") as dosya:
        
        context = ""
        soru = ""
        cevap = ""
        sonuclar[soru_cevap_id] = {"name":dosyalar, "context":[], "soru":[], "cevap":[]}
        
        for satir in dosya:
            if satir.startswith("Hukuki metin(Context):"):
                s = (satir.rfind("Hukuki metin(Context):"))
                context = satir[(s+22):-1].strip()

            elif satir.startswith("Soru:"):
                s = (satir.rfind("Soru:"))
                soru = satir[(s+5):-1].strip()

            elif satir.startswith("S:"):
                s = (satir.rfind("S:"))
                soru = satir[(s + 2):-1].strip()

            elif satir.startswith("Cevap:"):
                s = (satir.rfind("Cevap:"))
                cevap = satir[(s + 6):-1].strip()

                if len(cevap) != 0 and len(soru) != 0 and len(context) != 0:
                    
                    if soru[-1] != "?" or cevap[-1] != "." or satir in checker:
                        continue
                    else:
                        checker.append(satir)
                        sonuclar[soru_cevap_id]["context"].append(context)
                        sonuclar[soru_cevap_id]["soru"].append(soru)
                        sonuclar[soru_cevap_id]["cevap"].append(cevap)
                        

            elif satir.startswith("C:"):
                s = (satir.rfind("C:"))
                cevap = satir[(s + 2):-1].strip()

                if len(cevap) != 0 and len(soru) != 0 and len(context) != 0:
                    
                    if soru[-1] != "?" or cevap[-1] != "." or satir in checker:
                        continue
                    else:
                        checker.append(satir)
                        sonuclar[soru_cevap_id]["context"].append(context)
                        sonuclar[soru_cevap_id]["soru"].append(soru)
                        sonuclar[soru_cevap_id]["cevap"].append(cevap)
                        
        soru_cevap_id += 1
            

with open("dataset.json", "w", encoding="utf-8") as dataset:
    json.dump(sonuclar, dataset, sort_keys=False, ensure_ascii=False)
    
dataset.close()