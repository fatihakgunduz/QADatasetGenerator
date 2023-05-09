import json
import glob

# tüm text dosyalarını bul
dosya_listesi = glob.glob("*.txt")

soru_cevap_id = 1

context_count = 0
soru_count = 0
cevap_count = 0

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
            
            if satir.startswith("Son işlenen madde:"):               
                context_count = 0
                soru_count = 0
                cevap_count = 0
                
            elif satir.startswith("Hukuki metin(Context):") and context_count == 0:
                context_count += 1
                s = (satir.rfind("Hukuki metin(Context):"))
                context = satir[(s+22):-1].strip()

            elif satir.startswith("Soru:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Soru:"))
                soru = satir[(s+5):-1].strip()
                    
            elif satir.startswith("Bu metinden soru ve cevap olarak:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metinden soru ve cevap olarak:"))
                soru = satir[(s+33):-1].strip()
                
            elif satir.startswith("Bu metinden 1 adet daha soru ve cevap üret:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metinden 1 adet daha soru ve cevap üret:"))
                soru = satir[(s+44):-1].strip()
                    
            elif satir.startswith("Bu metindeki bir kural hakkında soru:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metindeki bir kural hakkında soru:"))
                soru = satir[(s+37):-1].strip()
    
            elif satir.startswith("Bu metinden soru:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metinden soru:"))
                soru = satir[(s+17):-1].strip()      
           
            elif satir.startswith("Bu metinde sorulan soru:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metinde sorulan soru:"))
                soru = satir[(s+24):-1].strip()
        
            elif satir.startswith("**Soru:**") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("**Soru:**"))
                soru = satir[(s+9):-1].strip()
                    
            elif satir.startswith("Bu metinden türkçe olarak 1 adet soru ve cevap üret:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Bu metinden türkçe olarak 1 adet soru ve cevap üret:"))
                soru = satir[(s+52):-1].strip()
                    
            elif satir.startswith("S:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("S:"))
                soru = satir[(s + 2):-1].strip()
                
            elif satir.startswith("Q:") and soru_count == 0:
                soru_count += 1
                s = (satir.rfind("Q:"))
                soru = satir[(s + 2):-1].strip()
                
            elif (satir.strip().replace('"', '').endswith("?") and soru_count == 0):
                if ("metinde" not in satir.strip().replace('"', '').lower()):
                    if ("malesef" not in satir.strip().replace('"', '').lower()):
                        if ("maalesef" not in satir.strip().replace('"', '').lower()):
                            soru_count += 1
                            soru = satir.strip().replace('"', '')

            elif satir.startswith("Cevap:") and cevap_count == 0:
                cevap_count += 1
                s = (satir.rfind("Cevap:"))
                cevap = satir[(s + 6):-1].strip()

                if len(cevap) != 0 and len(soru) != 0 and len(context) != 0:
                    soru = soru.replace('"', '')
                    cevap = cevap.replace('"', '')
                    if soru[-1] != "?": 
                        continue
                    if cevap[-1] != ".":
                        continue
                    if satir in checker:
                        continue
                    elif "Bu metinde" in soru:
                        continue
                    else:
                        checker.append(satir)
                        sonuclar[soru_cevap_id]["context"].append(context)
                        sonuclar[soru_cevap_id]["soru"].append(soru)
                        sonuclar[soru_cevap_id]["cevap"].append(cevap)
                        
                        context = ""
                        soru = ""
                        cevap = ""

            elif satir.startswith("C:") and cevap_count == 0:
                cevap_count += 1
                s = (satir.rfind("C:"))
                cevap = satir[(s + 2):-1].strip()

                if len(cevap) != 0 and len(soru) != 0 and len(context) != 0:
                    soru = soru.replace('"', '')
                    cevap = cevap.replace('"', '')
                    if soru[-1] != "?" or cevap[-1] != "." or satir in checker:
                        continue
                    elif "Bu metinde" in soru:
                        continue
                    else:
                        checker.append(satir)
                        sonuclar[soru_cevap_id]["context"].append(context)
                        sonuclar[soru_cevap_id]["soru"].append(soru)
                        sonuclar[soru_cevap_id]["cevap"].append(cevap)
                        
                        context = ""
                        soru = ""
                        cevap = ""
            
        soru_cevap_id += 1            

with open("dataset.json", "w", encoding="utf-8") as dataset:
    json.dump(sonuclar, dataset, sort_keys=False, ensure_ascii=False)
    
dataset.close()
