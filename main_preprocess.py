import json
import glob
# -*- coding: utf-8 -*-
# klasör yolunu belirle
# klasor_yolu = "./"

# tüm text dosyalarını bul
# dosya_listesi = glob.glob("/Users/fatihakgunduz/Documents/Önyazıları çıkarılmış veriler/Koca-Üzülmez- Ceza Özel Hükümler/9- Özel hayata karşı suçlar.txt")
dosya_listesi = glob.glob("/Users/fatihakgunduz/Documents/Önyazıları çıkarılmış veriler/*/*.txt")
print(dosya_listesi)
# sonuçları saklamak için boş bir sözlük oluştur

soru_cevap_id = 1

checker=[]

sonuclar = {}

# sonuçları dosyaya yaz

#soru cevapların kaymadığına emin olmak için
context_count = 0
soru_count = 0
cevap_count = 0
yanlıs_count = 0
yanlıs_count_2 = 0

# her dosya için işlem yap
for dosyalar in dosya_listesi:
    with open(dosyalar, "r", encoding="utf-8") as dosya:
        context = ""
        soru = ""
        cevap = ""
        indis = ""
        sorunlu = 0
        sorunlu_2 = 0
        satir_last = ""
        satir_last_1 = ""
        name = dosyalar.split("/")
        file1 = open(f'sorunlu/{name[-2]}-{name[-1]}', "a")  # append mode
        file1.write(dosyalar)
        file1.write("\n\n")

        file2 = open(f'sorunlu-2/{name[-2]}-{name[-1]}', "a")  # append mode
        file2.write(dosyalar)
        file2.write("\n\n")

        sonuclar[soru_cevap_id] = {"name":dosyalar, "context":[], "soru":[], "cevap":[]}

        for satir in dosya:
            
            if satir.startswith("Son işlenen indis:"):
                
                if((soru_count == 0 and cevap_count == 0 and context_count == 1) or ((soru_count == 1 and cevap_count == 0 and context_count == 1) or (soru_count == 0 and cevap_count == 1 and context_count == 1))):
                    
                    if (satir_last_1 == indis):
                        continue
                
                    satir_last_1 = indis
                    
                    sorunlu=1
                    yanlıs_count += 1
                    file1.write(indis)
                    file1.write("\n")
                
                indis = satir
                context_count = 0
                soru_count = 0
                cevap_count = 0

            elif satir.startswith("Son işlenen madde:"):
                
                if((soru_count == 0 and cevap_count == 0 and context_count == 1) or ((soru_count == 1 and cevap_count == 0 and context_count == 1) or (soru_count == 0 and cevap_count == 1 and context_count == 1))):
                    sorunlu=1
                    yanlıs_count += 1
                    file1.write(indis)
                    file1.write("\n")
                
                indis = satir
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
                    
            # elif satir.startswith("Bu metinden soru ve cevap olarak:") and soru_count == 0:
            #     soru_count += 1
            #     s = (satir.rfind("Bu metinden soru ve cevap olarak:"))
            #     soru = satir[(s+33):-1].strip()
                
            # elif satir.startswith("Bu metinden 1 adet daha soru ve cevap üret:") and soru_count == 0:
            #     soru_count += 1
            #     s = (satir.rfind("Bu metinden 1 adet daha soru ve cevap üret:"))
            #     soru = satir[(s+44):-1].strip()
                    
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
                if ("üzgünüm" not in satir.strip().replace('"', '').lower()):
                    if ("malesef" not in satir.strip().replace('"', '').lower()):
                        if ("maalesef" not in satir.strip().replace('"', '').lower()):
                            soru_count += 1
                            soru = satir.strip().replace('"', '')

            elif satir.startswith("Cevap:") and cevap_count == 0 and soru_count ==1 and context_count == 1:
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

            elif satir.startswith("C:") and cevap_count == 0 and soru_count ==1 and context_count == 1:
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

            elif satir == "\n":
                continue

            elif satir == " Bu metinden 1 adet soru ve cevap üret.\n":
                continue

            else:
                if (satir_last == indis):
                    continue
                
                satir_last = indis
                
                sorunlu_2 = 1
                yanlıs_count_2 += 1
                
                file2.write(indis)
                file2.write("\n")


        soru_cevap_id += 1
        
        file1.write("\n")
        file1.close()
        
        if(not sorunlu):
            import os
            os.remove(f'sorunlu/{name[-2]}-{name[-1]}')

        file2.write("\n")
        file2.close()
        
        if(not sorunlu_2):
            import os
            os.remove(f'sorunlu-2/{name[-2]}-{name[-1]}')

print(yanlıs_count)
print(yanlıs_count_2)
with open("new_dataset_batuhan.json", "w", encoding="utf-8") as dataset:
    json.dump(sonuclar,dataset,sort_keys=False,ensure_ascii=False,indent=4)
dataset.close()