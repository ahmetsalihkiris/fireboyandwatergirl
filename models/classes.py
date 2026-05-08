import pygame
import csv

class Oyuncu(pygame.sprite.Sprite):
    pass

class Ates1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((18, 18))
        self.image.fill((255, 69, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.baslangic_x = x
        self.baslangic_y = y

        self.hiz_x = 0
        self.hiz_y = 0 
        self.hareket_hizi = 4
        self.ziplama_gucu = -9
        self.yercekimi = 0.5
        self.havada_mi = True

        def guncelle(self, engeller, merdivenler, su_havuzlari, zehir_havuzlari):
            self.hiz_x = 0
            tuslar = pygame.key.get_pressed()

            merdivende_mi = False
            for merdiven in merdivenler:
                if self.rect.colliderect(merdiven):
                    merdivende_mi = True
                    break
            
            if tuslar[pygame.K_LEFT]:
                self.hiz_x = -self.hareket_hizi
            
            if tuslar[pygame.K_RIGHT]:
                self.hiz_x = self.hareket_hizi

            self.rect.x += self.hiz_x
            for engel in engeller:
                if self.rect.colliderect(engel):
                    if self.hiz_x > 0:
                        self.rect.right = engel.left
                    elif self.hiz_x < 0:
                        self.rect.left = engel.right
            

            if merdivende_mi:
                self.havada_mi = False
                self.hiz_y = 0
                if tuslar[pygame.K_UP]:
                    self.hiz_y += self.hareket_hizi
                elif tuslar[pygame.K_DOWN]:
                    self.hiz_y -= self.hareket_hizi
            
            else:
                if tuslar[pygame.K_UP] and not self.havada_mi:
                    self.hiz_y = self.ziplama_gucu
                    self.havada_mi = True

                self.hiz_y += self.yer_cekimi
                self.rect.y += self.hiz_y

            self.havada_mi = True

            for engel in engeller:
                if self.rect.colliderect(engel):
                    if self.hiz_y >0:
                        self.rect.bottom = engel.top
                        self.hiz_y = 0
                        self.havada_mi = False
                    elif self.hiz_y < 0:
                        self.rect.top = engel.bottom 
                        self.hiz_y = 0
            

            for su in su_havuzlari:
                if self.rect.colliderect(su):
                    self.rect.topleft = (self.baslangic_x, self.baslangic_y)

            for zehir in zehir_havuzlari:
                if self.rect.colliderect(zehir):
                    self.rect.topleft = (self.baslangic_x, self.baslangic_y)

class Su1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((18, 18))
        self.image.fill((30, 144,255))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.baslangic_x = 0
        self.baslangic_y = 0

        self.hiz_x = 0
        self.hiz_y = 0 
        self.hareket_hizi = 4
        self.ziplama_gucu = -9
        self.yercekimi = 0.5
        self.havada_mi = True

        def guncelle(self, engeller, merdivenler, su_havuzlari, lav_havuzlari, zehir_havuzlari):
            self.hiz_x = 0
            tuslar = pygame.key.get_pressed()

            merdivende_mi = False
            for merdiven in merdivenler:
                if self.rect.colliderect(merdiven):
                    merdivende_mi = True
                    break
            
            if tuslar[pygame.K_a]:
                self.hiz_x = -self.hareket_hizi
            
            if tuslar[pygame.K_d]:
                self.hiz_x = self.hareket_hizi

            self.rect.x += self.hiz_x
            for engel in engeller:
                if self.rect.colliderect(engel):
                    if self.hiz_x > 0:
                        self.rect.right = engel.left
                    elif self.hiz_x < 0:
                        self.rect.left = engel.right
            

            if merdivende_mi:
                self.havada_mi = False
                self.hiz_y = 0
                if tuslar[pygame.K_w]:
                    self.hiz_y += self.hareket_hizi
                elif tuslar[pygame.K_s]:
                    self.hiz_y -= self.hareket_hizi
            
            else:
                if tuslar[pygame.K_w] and not self.havada_mi:
                    self.hiz_y = self.ziplama_gucu
                    self.havada_mi = True

                self.hiz_y += self.yer_cekimi
                self.rect.y += self.hiz_y

            self.havada_mi = True

            for engel in engeller:
                if self.rect.colliderect(engel):
                    if self.hiz_y >0:
                        self.rect.bottom = engel.top
                        self.hiz_y = 0
                        self.havada_mi = False
                    elif self.hiz_y < 0:
                        self.rect.top = engel.bottom 
                        self.hiz_y = 0
            

            for lav in lav_havuzlari:
                if self.rect.colliderect(lav):
                    self.rect.topleft = (self.baslangic_x, self.baslangic_y)

            for zehir in zehir_havuzlari:
                if self.rect.colliderect(zehir):
                    self.rect.topleft = (self.baslangic_x, self.baslangic_y)



"""class CSVHarita:
    def __init__(self):
        self.tile_size = 18

        self.engeller = []
        self.merdivenler = []
        self.su_havuzlari = []
        self.lav_havuzlari = []
        self.zehir_havuzlari = []

        self.katmani_yukle("map/harita_1/harita_1_blok.csv", self.engeller)
        self.katmani_yukle("map/harita_1/harita_1_merdiven.csv", self.merdivenler)
        self.katmani_yukle("map/harita_1/harita_1_su_suyu.csv", self.su_havuzlari)
        self.katmani_yukle("map/harita_1/harita_1_ates_suyu.csv", self.lav_havuzlari)
        self.katmani_yukle("map/harita_1/harita_1_zehirli_su.csv", self.zehir_havuzlari)


    def katmani_yukle(self, dosya_yolu, hedef_liste):
        try:
            with open(dosya_yolu, mode ='r', encoding='utf-8') as dosya:
                okuyucu = csv.reader(dosya)
                for y_indeks, satir in enumerate(okuyucu):
                    for x_indeks, tile_id in enumerate(satir):
                        if tile_id.strip() != "" and int(tile_id) > -1:
                            x_poz = x_indeks * self.tile_size
                            y_poz = y_indeks * self.tile_size
                            rect = pygame.Rect(x_poz, y_poz, self.tile_size, self.tile_size)
                            hedef_liste.append(rect)
        except FileNotFoundError:
            print(f"Uyarı: {dosya_yolu} bulunamadı. bu katman boş bırakılacak")
    
    def ciz_prototip(self,ekran):

        for engel in self.engeller:
             pygame.draw.rect(ekran, (100, 100, 100), engel)

        for merdiven in self.merdivenler:
            pygame.draw.rect(ekran, (200, 150, 50), merdiven)
        
        for su in self.su_havuzlari:
            pygame.draw.rect(ekran, (30, 144, 255), su)
        
        for lav in self.lav_havuzlari:
            pygame.draw.rect(ekran, (255, 69, 0), lav)
        
        for zehir in self.zehir_havuzlari:
            pygame.draw.rect(ekran, (50, 255, 50), zehir)"""

class CSVHarita:
    def __init__(self):
        self.tile_size = 18
        
        # --- TILESET GÖRSELİNİ YÜKLE ---
        # Resmin tam yolunu belirtiyoruz. Arkası saydam (PNG) olduğu için convert_alpha() şart.
        try:
            self.tileset = pygame.image.load("Tilemap/tilemap_packed.png").convert_alpha()
        except FileNotFoundError:
            print("HATA: tilemap_packed.png dosyası Tilemap klasöründe bulunamadı!")
        
        # Çarpışma (Fizik) Listeleri
        self.engeller = []
        self.merdivenler = []
        self.su_havuzlari = []
        self.lav_havuzlari = []
        self.zehir_havuzlari = []
        
        # Çizim Listesi (İçinde hem resim parçacığını hem de koordinatını tutacak)
        self.cizim_verileri = []
        
        # 1. ÖNCE ARKA PLAN (SÜSLEMELER) YÜKLENSİN
        # Bunlara fizik (çarpışma) listesi göndermiyoruz, sadece çizilecekler.
        self.katmani_yukle("map/harita_1/harita_1_agac.csv")
        self.katmani_yukle("map/harita_1/harita_1_sarmasik.csv")
        self.katmani_yukle("map/harita_1/harita_1_ev.csv")
        self.katmani_yukle("map/harita_1/harita_1_sus.csv")
        self.katmani_yukle("map/harita_1/harita_1_tabela.csv")
        
        
        # 2. ETKİLEŞİMLİ KATMANLAR YÜKLENSİN
        # Bunlar hem çizilecek hem de ilgili fizik listesine (self.engeller vb.) eklenecek.
        self.katmani_yukle("map/harita_1/harita_1_blok.csv", self.engeller)
        self.katmani_yukle("map/harita_1/harita_1_merdiven.csv", self.merdivenler)
        self.katmani_yukle("map/harita_1/harita_1_su_suyu.csv", self.su_havuzlari)
        self.katmani_yukle("map/harita_1/harita_1_ates_suyu.csv", self.lav_havuzlari)
        self.katmani_yukle("map/harita_1/harita_1_zehirli_su.csv", self.zehir_havuzlari)
        self.katmani_yukle("map/harita_1/harita_1_zemin.csv", self.engeller)


    def katmani_yukle(self, dosya_yolu, fizik_listesi=None):
        try:
            with open(dosya_yolu, mode='r', encoding='utf-8') as dosya:
                okuyucu = csv.reader(dosya)
                for y_indeks, satir in enumerate(okuyucu):
                    for x_indeks, tile_id in enumerate(satir):
                        if tile_id.strip() != "" and int(tile_id) > -1: 
                            _id = int(tile_id)
                            x_poz = x_indeks * self.tile_size
                            y_poz = y_indeks * self.tile_size
                            rect = pygame.Rect(x_poz, y_poz, self.tile_size, self.tile_size)
                            
                            # Eğer bir fizik listesi verildiyse (zemin, merdiven vb.) çarpışmaya ekle
                            if fizik_listesi is not None:
                                fizik_listesi.append(rect)
                                
                            # ID'ye göre resmi kes ve çizim listesine ekle
                            tile_resmi = self.tile_kes(_id)
                            self.cizim_verileri.append((tile_resmi, rect))
        except FileNotFoundError:
            print(f"Uyarı: {dosya_yolu} bulunamadı, atlandı.")

    def tile_kes(self, tile_id):
        # 360px genişliğindeki resimde, 18px'lik 20 sütun vardır (360/18=20)
        sutun_sayisi = 20
        x = (tile_id % sutun_sayisi) * self.tile_size
        y = (tile_id // sutun_sayisi) * self.tile_size
        
        # Boş, saydam bir yüzey oluştur ve ana resimden ilgili parçayı buraya kopyala
        parca = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        parca.blit(self.tileset, (0, 0), (x, y, self.tile_size, self.tile_size))
        return parca

    def ciz(self, ekran):
        # Kaydedilen tüm resim parçalarını ekrana basar
        for resim, rect in self.cizim_verileri:
            ekran.blit(resim, rect)