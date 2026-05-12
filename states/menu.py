import pygame
from states.base import State
from models.arayuz import Buton
from models.muzik import ses_motoru

class Menu(State):
    def __init__(self):
        super().__init__()
        # Yazı tiplerini tanımlıyoruz (Butonlar ve Başlık için)
        self.font = pygame.font.SysFont(None, 48)
        self.buyuk_font = pygame.font.SysFont("Arial", 60, bold=True)

        # Menüdeki butonları koordinat ve boyutlarıyla oluşturuyoruz
        self.basla_butonu = Buton("Başla", 305, 250, 200, 80, self.font)
        self.bolumler_butonu = Buton("Bölümler", 305, 350, 200, 70, self.font)
        self.cikis_butonu = Buton("Çıkış", 305, 450, 200, 80, self.font)

        # ARKA PLAN YÜKLEME: Burası kritik. 
        # Eğer "b.png" bulunamazsa 'except' bloğu çalışır ve düz siyah ekran verir.
        try:
            self.arkaplan = pygame.image.load("b.png") # Resmi dosyadan çekiyoruz
            self.arkaplan = pygame.transform.scale(self.arkaplan, (810, 630)) # Ekran boyutuna sığdırıyoruz
        
        except:
            # Resim yüklenirken hata oluşursa oyun çökmesin diye koyu gri bir renk atıyoruz
            self.arkaplan = pygame.Surface((810,630))
            self.arkaplan.fill((20, 20, 20))
    
    def handle_events(self, events):
        for event in events:
            # Pencere kapatma düğmesine (X) basılırsa oyundan çık
            if event.type == pygame.QUIT:
                self.quit = True
            
            # Fare tıklamalarını yakalıyoruz
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Tıklanan noktayı alıyoruz (Aslında mouse_pos burada tanımlanmış ama aşağıda event kullanılmış)
                mouse_pos = event.pos
       
            # Butonlara tıklanıp tıklanmadığını kontrol ediyoruz
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Başla Butonu: Sahneyi GAME yap ve geçişi onayla (done = True)
                if self.basla_butonu.tiklandi_mi(event):
                    print("SİSTEM: 'Başla' butonuna tıklandı! Oyun sahnesine geçiliyor...")
                    self.next_state = "GAME"
                    self.done = True
                
                # Bölümler Butonu: Sahneyi LEVEL_SELECT yap ve geçişi onayla
                if self.bolumler_butonu.tiklandi_mi(event):
                    print("SİSTEM: 'Bölümler' butonuna tıklandı! Bölüm seçimi açılıyor...")
                    self.next_state = "LEVEL_SELECT"
                    self.done = True
                    
                # Çıkış Butonu: Oyunu tamamen kapat
                if self.cikis_butonu.tiklandi_mi(event):
                    print("SİSTEM: 'Çıkış' butonuna tıklandı! Kapatılıyor...")
                    self.quit = True
              
    def draw(self, ekran):
        # 1. Önce en alta arka planı seriyoruz (Üzerine gelecek her şey bunun üstünde kalır)
        ekran.blit(self.arkaplan, (0, 0))

        # 2. Ana başlığı (ATEŞ VE SU) altın sarısı renginde yazdırıyoruz
        oyun_basliği = self.buyuk_font.render("ATEŞ VE SU", True, (255, 215, 0))
        baslik_rect = oyun_basliği.get_rect(center = (400, 100))
        ekran.blit(oyun_basliği, baslik_rect)

        # 3. Butonların görsellerini ekranın üstüne çiziyoruz
        self.basla_butonu.ciz(ekran)
        self.bolumler_butonu.ciz(ekran)
        self.cikis_butonu.ciz(ekran)