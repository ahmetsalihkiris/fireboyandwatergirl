import pygame
from states.base import State
from models.arayuz import Buton

class seviye_secim(State):
    def __init__(self):
        super().__init__()
        # Yazı tipi sistemini başlatıyoruz ve butonlar/başlık için fontları tanımlıyoruz
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)
        self.buyuk_font = pygame.font.SysFont("Arial", 60, bold = True)

        # Bölüm seçme butonlarını ve geri butonunu ekrandaki yerlerine göre oluşturuyoruz
        self.btn_bolum1 = Buton("Bölüm 1", 305, 180, 200, 60, self.font)
        self.btn_bolum2 = Buton("Bölüm 2", 305, 250, 200, 60, self.font)
        self.btn_bolum3 = Buton("Bölüm 3", 305, 320, 200, 60, self.font)
        self.btn_geri = Buton("Geri", 305, 460, 200, 60, self.font)

        # Varsayılan olarak seçilen seviyeyi 1 yapıyoruz
        self.secilen_seviye = 1

        # ARKA PLAN YÜKLEME:
        # Eğer "ahmetbg.png" dosyası klasörde yoksa, except bloğuna atlar ve ekran siyah kalır.
        try:
            self.arkaplan = pygame.image.load("ahmetbg.png") # Resim dosyasını yükle
            self.arkaplan = pygame.transform.scale(self.arkaplan, (810, 630)) # Ekran boyutuna ölçekle
        
        except:
            # Resim bulunamazsa hata vermemesi için koyu gri bir zemin oluşturuyoruz
            self.arkaplan = pygame.Surface((810, 630))
            self.arkaplan.fill((20, 20, 20))

    def handle_events(self, events):
        for event in events:
            # Pencereyi kapatma (X) butonuna basılırsa çıkış sinyali gönder
            if event.type == pygame.QUIT:
                self.quit = True
            
            # Fare tıklama olaylarını kontrol ediyoruz
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Bölüm 1 butonu tıklandıysa: Seviyeyi 1 yap ve GAME sahnesine geç
                if self.btn_bolum1.tiklandi_mi(event):
                    self.secilen_seviye = 1
                    self.next_state = "GAME"
                    self.done = True
                
                # Bölüm 2 butonu tıklandıysa: Seviyeyi 2 yap ve GAME sahnesine geç
                elif self.btn_bolum2.tiklandi_mi(event):
                    self.secilen_seviye = 2
                    self.next_state = "GAME"
                    self.done = True
                
                # Bölüm 3 butonu tıklandıysa: Seviyeyi 3 yap ve GAME sahnesine geç
                elif self.btn_bolum3.tiklandi_mi(event):
                    self.secilen_seviye = 3
                    self.next_state = "GAME"
                    self.done = True
                
                # Geri butonu tıklandıysa: Sahneyi MENU olarak değiştir ve geri dön
                elif self.btn_geri.tiklandi_mi(event):
                    self.next_state = "MENU"
                    self.done = True

    def draw(self, screen):
        # 1. Önce arka plan resmini (veya rengini) en alta çiziyoruz
        screen.blit(self.arkaplan, (0, 0))
        
        # 2. Üst kısma altın sarısı renginde "BÖLÜM SEÇ" başlığını yazdırıyoruz
        baslik = self.buyuk_font.render("BÖLÜM SEÇ", True, (255, 215, 0))
        baslik_rect = baslik.get_rect(center=(400, 80))
        screen.blit(baslik, baslik_rect)
        
        # 3. Tüm butonların güncel hallerini ekranın üzerine çiziyoruz
        self.btn_bolum1.ciz(screen)
        self.btn_bolum2.ciz(screen)
        self.btn_bolum3.ciz(screen)
        self.btn_geri.ciz(screen)