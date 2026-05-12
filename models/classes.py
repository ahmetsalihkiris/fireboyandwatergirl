import pygame
import csv
from models.muzik import ses_motoru

class AnimasyonluKare(pygame.sprite.Sprite):
    def __init__(self, x, y, kareler):
        super().__init__()
        self.frameler = kareler  
        self.guncel_frame = 0     
        self.image = self.frameler[self.guncel_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animasyon_hizi = 0.05

    def update(self):
        
        self.guncel_frame += self.animasyon_hizi
        
        
        if self.guncel_frame >= len(self.frameler):
            self.guncel_frame = 0
            
        
        self.image = self.frameler[int(self.guncel_frame)]

class Elmas(pygame.sprite.Sprite):
    def __init__(self, x, y, resim):
        super().__init__()
        self.image = resim
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = self.rect.inflate(-8, -8)


class Oyuncu(pygame.sprite.Sprite):
    def karakter_kes(self, resim_yolu, x, y):
        sheet = pygame.image.load(resim_yolu).convert_alpha()
        parca = pygame.Surface((24,24), pygame.SRCALPHA)
        parca.blit(sheet, (0,0), (x, y, 24, 24))

        parca = pygame.transform.scale(parca, (18,18))
        return parca

class Ates1(Oyuncu):
    def __init__(self, x, y):
        super().__init__()

        resim_yolu = "Tilemap/tilemap-characters_packed.png"
        self.sola_bakarken = [
            self.karakter_kes(resim_yolu, 96, 0),
            self.karakter_kes(resim_yolu, 120, 0)
        ]

        self.saga_bakarken = [
            pygame.transform.flip(self.sola_bakarken[0], True, False),
            pygame.transform.flip(self.sola_bakarken[1], True, False)
        ]

        self.guncel_kare = 0
        self.animasyon_hizi = 0.15
        self.yuz_saga_donuk = True

        self.image = self.saga_bakarken[0]

        self.oldu_mu = False
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = self.rect.inflate(-8, 0)

        self.baslangic_x = x
        self.baslangic_y = y

        self.hiz_x = 0
        self.hiz_y = 0 
        self.hareket_hizi = 2
        self.merdiven_hizi = 1
        self.ziplama_gucu = -7
        self.yer_cekimi = 0.5
        self.havada_mi = True

        self.ziplama_sayaci = 0

    def update(self, engeller, merdivenler,  su_havuzlari,lav_havuzlari, zehir_havuzlari, kirmizi_elmaslar, mavi_elmaslar):
        
        if self.ziplama_sayaci > 0:
            self.ziplama_sayaci -= 1
        
        self.hiz_x = 0
        tuslar = pygame.key.get_pressed()

        merdivende_mi = False
        for merdiven in merdivenler:
            if self.hitbox.colliderect(merdiven):
                merdivende_mi = True
                break
        
        if merdivende_mi:
            aktif_hiz = self.merdiven_hizi
        else:
            aktif_hiz = self.hareket_hizi

        if tuslar[pygame.K_LEFT]:
            self.hiz_x = -aktif_hiz
            
        if tuslar[pygame.K_RIGHT]:
            self.hiz_x = aktif_hiz

        self.hitbox.x += self.hiz_x
        for engel in engeller:
            if self.hitbox.colliderect(engel):
                if self.hiz_x > 0:
                    self.hitbox.right = engel.left
                elif self.hiz_x < 0:
                    self.hitbox.left = engel.right
            

        if merdivende_mi:
            self.havada_mi = False
            self.hiz_y = 0
            if tuslar[pygame.K_UP]:
                self.hiz_y -= self.merdiven_hizi
            elif tuslar[pygame.K_DOWN]:
                self.hiz_y += self.merdiven_hizi
            
        else:
            if tuslar[pygame.K_UP] and not self.havada_mi and self.ziplama_sayaci == 0:
                self.hiz_y = self.ziplama_gucu
                self.havada_mi = True

                ses_motoru.ziplama_cal()  
                self.ziplama_sayaci = 30

            self.hiz_y += self.yer_cekimi
        self.hitbox.y += self.hiz_y

        self.havada_mi = True

        for engel in engeller:
            if self.hitbox.colliderect(engel):
                if self.hiz_y >0:
                    self.hitbox.bottom = engel.top
                    self.hiz_y = 0
                    self.havada_mi = False
                elif self.hiz_y < 0:
                    self.hitbox.top = engel.bottom 
                    self.hiz_y = 0
        
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        
        if self.hitbox.right > 810:
            self.hitbox.right = 810
        
        

        for su in su_havuzlari:
            if self.hitbox.colliderect(su):
                self.oldu_mu = True
                self.hiz_y = 0  # 
                self.havada_mi = True

        for zehir in zehir_havuzlari:
            if self.hitbox.colliderect(zehir):
                self.oldu_mu = True
                self.hiz_y = 0  
                self.havada_mi = True
        
        for elmas in kirmizi_elmaslar:
            if self.hitbox.colliderect(elmas.hitbox):
                elmas.kill()
                ses_motoru.elmas_cal()

        
        if self.hiz_x > 0:
            self.yuz_saga_donuk = True
            self.guncel_kare += self.animasyon_hizi

        elif self.hiz_x < 0:
            self.yuz_saga_donuk = False
            self.guncel_kare += self.animasyon_hizi
        
        elif merdivende_mi and self.hiz_y != 0:
            self.guncel_kare += self.animasyon_hizi
        
        else:
            self.guncel_kare = 0
        
        if self.guncel_kare >= len(self.sola_bakarken):
            self.guncel_kare = 0
        
        if self.yuz_saga_donuk:
            self.image = self.saga_bakarken[int(self.guncel_kare)]
        
        else:
            self.image = self.sola_bakarken[int(self.guncel_kare)]
        
        self.rect.topleft = self.hitbox.topleft

        self.rect.centerx -= 4


class Su1(Oyuncu):
    def __init__(self, x, y,):
        super().__init__()
        
        resim_yolu = "Tilemap/Tilemap-characters_packed.png"
        self.sola_bakarken = [
            self.karakter_kes(resim_yolu, 48, 0),
            self.karakter_kes(resim_yolu, 72, 0)
        ]

        self.saga_bakarken = [
            pygame.transform.flip(self.sola_bakarken[0], True, False),
            pygame.transform.flip(self.sola_bakarken[1], True, False)

        ]

        self.guncel_kare = 0
        self.animasyon_hizi = 0.15
        self.yuz_saga_donuk = True

        self.image = self.saga_bakarken[0]

        self.oldu_mu = False  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-8, 0)


        self.baslangic_x = 0
        self.baslangic_y = 0

        self.hiz_x = 0
        self.hiz_y = 0 
        self.hareket_hizi = 2
        self.merdiven_hizi = 1
        self.ziplama_gucu = -7
        self.yer_cekimi = 0.5
        self.havada_mi = True

        self.ziplama_sayaci = 0

    def update(self, engeller, merdivenler, su_havuzlari, lav_havuzlari, zehir_havuzlari, kirmizi_elmaslar, mavi_elmaslar):
        
        if self.ziplama_sayaci > 0:
            self.ziplama_sayaci -= 1
        
        self.hiz_x = 0
        tuslar = pygame.key.get_pressed()

        merdivende_mi = False
        for merdiven in merdivenler:
            if self.hitbox.colliderect(merdiven):
                merdivende_mi = True
                break
            
        if merdivende_mi:
            aktif_hiz = self.merdiven_hizi
        else:
            aktif_hiz = self.hareket_hizi

        if tuslar[pygame.K_a]:
            self.hiz_x = -aktif_hiz
            
        if tuslar[pygame.K_d]:
            self.hiz_x = aktif_hiz

        self.hitbox.x += self.hiz_x
        for engel in engeller:
            if self.hitbox.colliderect(engel):
                if self.hiz_x > 0:
                    self.hitbox.right = engel.left
                elif self.hiz_x < 0:
                    self.hitbox.left = engel.right
            
        if merdivende_mi:
            self.havada_mi = False
            self.hiz_y = 0
            if tuslar[pygame.K_w]:
                self.hiz_y -= self.merdiven_hizi
            elif tuslar[pygame.K_s]:
                self.hiz_y += self.merdiven_hizi
            
        else:
            if tuslar[pygame.K_w] and not self.havada_mi and self.ziplama_sayaci == 0:
                self.hiz_y = self.ziplama_gucu
                self.havada_mi = True

                ses_motoru.ziplama_cal()
                self.ziplama_sayaci = 30

            self.hiz_y += self.yer_cekimi
            
        self.hitbox.y += self.hiz_y
        self.havada_mi = True


        for engel in engeller:
            if self.hitbox.colliderect(engel):
                if self.hiz_y >0:
                    self.hitbox.bottom = engel.top
                    self.hiz_y = 0
                    self.havada_mi = False
                elif self.hiz_y < 0:
                    self.hitbox.top = engel.bottom 
                    self.hiz_y = 0
        
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        
        if self.hitbox.right > 810:
            self.hitbox.right = 810
            

        for lav in lav_havuzlari:
            if self.hitbox.colliderect(lav):
                self.oldu_mu = True
                self.hiz_y = 0  
                self.havada_mi = True

        for zehir in zehir_havuzlari:
            if self.hitbox.colliderect(zehir):
                self.oldu_mu = True
                self.hiz_y = 0
                self.havada_mi = True    
        
        for elmas in mavi_elmaslar:
            if self.hitbox.colliderect(elmas.hitbox):
                elmas.kill()
                ses_motoru.elmas_cal()

        if self.hiz_x > 0:
            self.yuz_saga_donuk = True
            self.guncel_kare += self.animasyon_hizi
        
        elif self.hiz_x < 0:
            self.yuz_saga_donuk = False
            self.guncel_kare += self.animasyon_hizi
        
        elif merdivende_mi and self.hiz_y != 0:
            self.guncel_kare += self.animasyon_hizi
        
        else:
            self.guncel_kare = 0
        
        if self.guncel_kare >= len(self.sola_bakarken):
            self.guncel_kare = 0
        
        if self.yuz_saga_donuk:
            self.image = self.saga_bakarken[int(self.guncel_kare)]
        
        else:
            self.image = self.sola_bakarken[int(self.guncel_kare)]

        self.rect.topleft = self.hitbox.topleft

        self.rect.centerx -= 4


class CSVHarita:

    def __init__(self,seviye = 1):
        self.tile_size = 18

        self.arkaplan = None
        arkaplan_yolu = f"map/harita_{seviye}/harita_{seviye}_arkaplan.png"
        try:
            bg_resim = pygame.image.load(arkaplan_yolu).convert()

            self.arkaplan = pygame.transform.scale(bg_resim, (810, 630))
        except FileNotFoundError:
            pass

        
        try:
            self.tileset = pygame.image.load("Tilemap/tilemap_packed.png").convert_alpha()
        except FileNotFoundError:
            pass
        
        self.engeller = []
        self.merdivenler = []
        self.su_havuzlari = []
        self.lav_havuzlari = []
        self.zehir_havuzlari = []
        self.ev_alanlari = []
        self.animasyon_grubu = pygame.sprite.Group()

        self.kirmizi_elmaslar = pygame.sprite.Group()
        self.mavi_elmaslar = pygame.sprite.Group()
        
        self.cizim_verileri = []
        
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_agac.csv")
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_sus.csv")
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_tabela.csv")
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_ev.csv",self.ev_alanlari)

        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_blok.csv", self.engeller)
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_sarmasik.csv", self.merdivenler)
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_merdiven.csv", self.merdivenler)
        self.katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_zemin.csv", self.engeller)

        self.animasyonlu_katman_yukle(f"map/harita_{seviye}/harita_{seviye}_su_suyu.csv", self.su_havuzlari, [33, 53])
        self.animasyonlu_katman_yukle(f"map/harita_{seviye}/harita_{seviye}_ates_suyu.csv", self.lav_havuzlari, [181, 185])
        self.animasyonlu_katman_yukle(f"map/harita_{seviye}/harita_{seviye}_zehir_suyu.csv", self.zehir_havuzlari, [180, 184])

        self.elmas_katmani_yukle(f"map/harita_{seviye}/harita_{seviye}_elmas.csv", [44], [67])
    
    def elmas_katmani_yukle(self, dosya_yolu, kirmizi_id_listesi, mavi_id_listesi):
        try:
            with open(dosya_yolu, mode='r', encoding='utf-8') as dosya:
                okuyucu = csv.reader(dosya)
                for y_indeks, satir in enumerate(okuyucu):
                    for x_indeks, tile_id in enumerate(satir):
                        val = tile_id.strip()
                        if val != "" and int(val) > -1:
                            _id = int(val)
                            x_poz = x_indeks * self.tile_size
                            y_poz = y_indeks * self.tile_size

                            tile_resmi = self.tile_kes(_id)
                            yeni_elmas = Elmas(x_poz, y_poz, tile_resmi)

                            if _id in kirmizi_id_listesi:
                                self.kirmizi_elmaslar.add(yeni_elmas)
                            
                            elif _id in mavi_id_listesi:
                                self.mavi_elmaslar.add(yeni_elmas)
                        
        except FileNotFoundError:
            pass

    def katmani_yukle(self, dosya_yolu, fizik_listesi=None):
        try:
            with open(dosya_yolu, mode='r', encoding='utf-8') as dosya:
                okuyucu = csv.reader(dosya)
                for y_indeks, satir in enumerate(okuyucu):
                    for x_indeks, tile_id in enumerate(satir):
                        val = tile_id.strip()
                        if val != "" and int(val) > -1:
                            _id = int(val)
                            x_poz = x_indeks * self.tile_size
                            y_poz = y_indeks * self.tile_size
                            rect = pygame.Rect(x_poz, y_poz, self.tile_size, self.tile_size)
                            
                            if fizik_listesi is not None:
                                fizik_listesi.append(rect)
                                
                            tile_resmi = self.tile_kes(_id)
                            self.cizim_verileri.append((tile_resmi, rect))
        except FileNotFoundError:
            pass
    
    
    def animasyonlu_katman_yukle(self, dosya_yolu, fizik_listesi, frame_idleri):
        kareler = []
        for f_id in frame_idleri:
            kareler.append(self.tile_kes(f_id))
    

        try:
            with open(dosya_yolu, mode='r', encoding='utf-8') as dosya:
                okuyucu = csv.reader(dosya)
                for y_indeks, satir in enumerate(okuyucu):
                    for x_indeks, tile_id in enumerate(satir):
                        val = tile_id.strip()
                        if val != "" and int(val) > -1:
                            x_poz = x_indeks * self.tile_size
                            y_poz = y_indeks * self.tile_size
                            rect = pygame.Rect(x_poz, y_poz, self.tile_size, self.tile_size)

                            if fizik_listesi is not None:
                                fizik_listesi.append(rect)
                            
                            yeni_su = AnimasyonluKare(x_poz, y_poz, kareler)
                            self.animasyon_grubu.add(yeni_su)
        
        except FileNotFoundError:
            pass

    def tile_kes(self, tile_id):
        sutun_sayisi = 20
        x = (tile_id % sutun_sayisi) * self.tile_size
        y = (tile_id // sutun_sayisi) * self.tile_size
        
        parca = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        parca.blit(self.tileset, (0, 0), (x, y, self.tile_size, self.tile_size))
        return parca

    def ciz(self, ekran):
        if self.arkaplan:
            ekran.blit(self.arkaplan, (0,0))

        for resim, rect in self.cizim_verileri:
            ekran.blit(resim, rect)
        
        self.animasyon_grubu.update()
        self.animasyon_grubu.draw(ekran)
        self.kirmizi_elmaslar.draw(ekran)
        self.mavi_elmaslar.draw(ekran)