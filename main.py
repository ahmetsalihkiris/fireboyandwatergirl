"""import pygame
import sys 
from models.classes import Ates1,Su1,CSVHarita
from models.arayuz import Buton

def main():
    pygame.init()
    # İstediğin ekran boyutu
    ekran = pygame.display.set_mode((810, 630))
    pygame.display.set_caption("Ateş ve Su - CSV Test")
    saat = pygame.time.Clock()

    # Haritayı yükle (Dosya adının doğru olduğundan emin ol)
    try:
        arkaplan = pygame.image.load("b.jpg")
        arkaplan = pygame.transform.scale(arkaplan,(810,630))
    except:
        arkaplan = pygame.Surface((810, 630))
        arkaplan.fill((20, 20, 20))
        print("Harita bulunamadı! CSV dosyalarını ve Tileset'i kontrol et.")
    
    harita = CSVHarita()

    # Oyuncular (Haritada boş bir yere koy)
    ates = Ates1(50, 50)
    su = Su1(100, 50)
    oyuncular = pygame.sprite.Group(ates, su)


  

    durum = "MENU"

    font = pygame.font.SysFont(None, 48)

    basla_butonu = Buton("Başla", 305, 250, 200, 80, font)
    cikis_butonu = Buton("Çıkış", 305, 350, 200, 80, font)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if durum == "MENU":
            if basla_butonu.tiklandi_mi(event):
                durum = "OYUN"
            elif cikis_butonu.tiklandi_mi(event):
                pygame.quit()
                sys.exit()
        
        if durum  == "MENU":
            #ekran.fill((20, 20, 20))
            oyun_basligi = font.render("ATEŞ VE SU", True, (255, 215, 0))
            baslik_rect = oyun_basligi.get_rect(center=(400, 100))
            ekran.blit(arkaplan,(0,0))
            ekran.blit(oyun_basligi, baslik_rect)
            
            basla_butonu.ciz(ekran)
            cikis_butonu.ciz(ekran)
            pygame.display.flip()
            saat.tick(60)
            
        elif durum == "OYUN":
            # Güncelleme
            oyuncular.update(
                harita.engeller,
                harita.merdivenler,
                harita.su_havuzlari,
                harita.lav_havuzlari,
                harita.zehir_havuzlari
            )

        # Çizim
            ekran.fill((20, 20, 20)) # Arka plan
            harita.ciz_prototip(ekran)
            oyuncular.draw(ekran)

            pygame.display.flip()
            saat.tick(60)
    while True:
        # 1. OLAY (EVENT) DÖNGÜSÜ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # DİKKAT: Tıklama kontrolleri artık bu 'for' döngüsünün İÇİNDE!
            if durum == "MENU":
                if basla_butonu.tiklandi_mi(event):
                    durum = "OYUN"
                elif cikis_butonu.tiklandi_mi(event):
                    pygame.quit()
                    sys.exit()
        
        # 2. ÇİZİM VE GÜNCELLEME DÖNGÜSÜ (For döngüsünün dışında)
        if durum == "MENU":
            ekran.blit(arkaplan, (0,0))
            oyun_basligi = font.render("ATEŞ VE SU", True, (255, 215, 0))
            baslik_rect = oyun_basligi.get_rect(center=(400, 100))
            ekran.blit(oyun_basligi, baslik_rect)
            
            basla_butonu.ciz(ekran)
            cikis_butonu.ciz(ekran)
            pygame.display.flip()
            saat.tick(60)
            
        elif durum == "OYUN":
            # Güncelleme
            oyuncular.update(
                harita.engeller, 
                harita.merdivenler, 
                harita.su_havuzlari, 
                harita.lav_havuzlari, 
                harita.zehir_havuzlari
            )

            # Çizim
            ekran.fill((30, 30, 30)) 
            harita.ciz_prototip(ekran) 
            oyuncular.draw(ekran)

            pygame.display.flip()
            saat.tick(60)


if __name__ == "__main__":
    main()"""

import pygame
import sys 
from models.classes import Ates1, Su1, CSVHarita
from models.arayuz import Buton
import traceback

def main():
    pygame.init()
    ekran = pygame.display.set_mode((810, 630))
    pygame.display.set_caption("Ateş ve Su - CSV Prototip Debug")
    saat = pygame.time.Clock()

    # --- DEBUG 1: Arka Plan Kontrolü ---
    try:
        arkaplan = pygame.image.load("b.jpg")
        arkaplan = pygame.transform.scale(arkaplan, (810, 630))
        print("SİSTEM: Arka plan resmi (b.jpg) başarıyla yüklendi.")
    except Exception as e:
        arkaplan = pygame.Surface((810, 630))
        arkaplan.fill((20, 20, 20))
        print(f"HATA: b.jpg yüklenemedi! Dosya ana klasörde mi? Detay: {e}")

    # Haritayı ve oyuncuları yüklüyoruz
    harita = CSVHarita()
    ates = Ates1(50, 605)
    su = Su1(100, 555)
    oyuncular = pygame.sprite.Group(ates, su)

    durum = "MENU"
    font = pygame.font.SysFont(None, 48)

    basla_butonu = Buton("Başla", 305, 250, 200, 80, font)
    cikis_butonu = Buton("Çıkış", 305, 350, 200, 80, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if durum == "MENU":
                # --- DEBUG 2: Buton Tıklama Kontrolü ---
                if basla_butonu.tiklandi_mi(event):
                    print("SİSTEM: 'Başla' butonuna tıklandı! Oyun sahnesine geçiliyor...")
                    durum = "OYUN"
                elif cikis_butonu.tiklandi_mi(event):
                    print("SİSTEM: 'Çıkış' butonuna tıklandı! Kapatılıyor...")
                    pygame.quit()
                    sys.exit()
        
        if durum == "MENU":
            ekran.blit(arkaplan, (0,0))
            oyun_basligi = font.render("ATEŞ VE SU", True, (255, 215, 0))
            baslik_rect = oyun_basligi.get_rect(center=(400, 100))
            ekran.blit(oyun_basligi, baslik_rect)
            
            basla_butonu.ciz(ekran)
            cikis_butonu.ciz(ekran)
            pygame.display.flip()
            saat.tick(60)
            
        elif durum == "OYUN":
            oyuncular.update(
                harita.engeller, 
                harita.merdivenler, 
                harita.su_havuzlari, 
                harita.lav_havuzlari, 
                harita.zehir_havuzlari,
                
            )

            ekran.fill((30, 30, 30)) 
            harita.ciz(ekran) 
            oyuncular.draw(ekran)

            pygame.display.flip()
            saat.tick(60)


if __name__ == "__main__":
    main()