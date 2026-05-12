import pygame
from states.base import State
from models.classes import Ates1, Su1, CSVHarita
from models.muzik import ses_motoru

# Oyun ekranını yöneten ana sınıf
class Oyun(State): 
    def __init__(self, seviye=1):
        super().__init__()

        # Başlangıç seviyesi
        self.seviye = seviye

        # Font sistemini başlat
        pygame.font.init()

        # Küçük yazılar için font
        self.kucuk_font = pygame.font.SysFont("Arial", 30)

        # Büyük başlıklar için font
        self.buyuk_font = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Oyun bitti mi kontrolü
        self.is_game_over = False

        # Geçen süre
        self.gecen_zam = 0

        # İlk seviyeyi yükle
        self.load_level()

        # Bölüm bitti ekranı açık mı
        self.bolum_bitti_ekrani = False

        # Oyun tamamen bitti ekranı açık mı
        self.oyun_bitti_ekrani = False

        # Toplam bölüm sayısı
        self.toplam_bolum_sayisi = 3

        # Şu an oynanan bölüm
        self.suanki_bolum = 1

        # Bölüm bitiş ekranı başlık fontu
        self.font_baslik = pygame.font.SysFont("Arial", 50, bold = True)

        # Alt açıklama fontu
        self.font_alt = pygame.font.SysFont("Arial", 30 )

    # Seviye yükleme fonksiyonu
    def load_level(self):

        print(f"Bölüm {self.seviye} Yükleniyor...")

        # Haritayı CSV dosyasından oluştur
        self.harita = CSVHarita(self.seviye)

        # Seviye 1 başlangıç koordinatları
        if self.seviye == 1:
            self.ates = Ates1(790, 605)
            self.su = Su1(750, 605)

        # Seviye 2 başlangıç koordinatları
        elif self.seviye == 2:
            self.ates = Ates1(50, 605)
            self.su = Su1(50, 555) 

        # Seviye 3 ve sonrası başlangıç koordinatları
        elif self.seviye >= 3:
            self.ates = Ates1(390, 605)
            self.su = Su1(495, 605)
        
        # Oyuncuları sprite grubuna ekle
        self.oyuncular = pygame.sprite.Group(self.ates, self.su)

        # Süreyi başlat
        self.bas_zam = pygame.time.get_ticks()

        # Oyun durumunu sıfırla
        self.is_game_over = False

    # Klavye ve diğer olayları kontrol eden fonksiyon
    def handle_events(self, events):

        for event in events:
            
            # Oyun bittiyse ve R tuşuna basıldıysa seviyeyi yeniden yükle
            if self.is_game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.load_level()
            
            # Bölüm bittiyse ENTER ile sonraki bölüme geç
            if self.bolum_bitti_ekrani and event.key == pygame.K_RETURN:
                self.bolum_bitti_ekrani = False
                self.seviye += 1
                self.suanki_bolum +=1
                self.load_level()
            
            # Oyun tamamen bittiyse ESC ile menüye dön
            elif self.oyun_bitti_ekrani and event.key == pygame.K_ESCAPE:
                self.oyun_bitti_ekrani = False
                self.sevite = 1
                self.suanki_bolum = 1
                self.next_state = "MENU"
                self.done = True

    # Oyun mantığını güncelleyen fonksiyon
    def update(self):

        # Oyun bittiyse hiçbir şeyi güncelleme
        if self.is_game_over:
            return

        # Bölüm veya oyun bitiş ekranı açıksa güncelleme yapma
        if self.bolum_bitti_ekrani or self.oyun_bitti_ekrani:
            return
        
        # Oyuncuları güncelle
        self.oyuncular.update(
            self.harita.engeller,          # Katı bloklar
            self.harita.merdivenler,       # Merdivenler
            self.harita.su_havuzlari,      # Su havuzları
            self.harita.lav_havuzlari,     # Lav havuzları
            self.harita.zehir_havuzlari,   # Zehir havuzları
            self.harita.kirmizi_elmaslar,  # Kırmızı elmaslar
            self.harita.mavi_elmaslar      # Mavi elmaslar
        )

        # Karakterlerden biri öldüyse
        if self.ates.oldu_mu or self.su.oldu_mu:

            # Oyun bitti durumuna geç
            self.is_game_over = True

            # Ölüm sesi çal
            ses_motoru.ciss_cal()

            print("Game Over")
         
        # Karakterler ev alanına ulaştı mı kontrol değişkenleri
        ates_evde = False
        su_evde = False

        # Ev alanlarını kontrol et
        for ev_kare in self.harita.ev_alanlari:

            # Ateş karakteri evde mi
            if self.ates.hitbox.colliderect(ev_kare):
                ates_evde = True

            # Su karakteri evde mi
            if self.su.hitbox.colliderect(ev_kare):
                su_evde = True
        
        # Kalan kırmızı elmas sayısı
        kalan_kirmizi = len(self.harita.kirmizi_elmaslar)

        # Kalan mavi elmas sayısı
        kalan_mavi = len(self.harita.mavi_elmaslar)
        

        # İki oyuncu da evdeyse ve tüm elmaslar toplandıysa
        if ates_evde and su_evde and kalan_kirmizi == 0 and kalan_mavi == 0:
 
            # Son bölüm değilse bölüm bitiş ekranı aç
            if self.seviye < self.toplam_bolum_sayisi:
                self.bolum_bitti_ekrani = True

            # Son bölümse oyun bitiş ekranı aç
            else:
                self.oyun_bitti_ekrani = True

    
    # Ekrana çizim yapan fonksiyon
    def draw(self, ekran):

        # Arka plan rengini doldur
        ekran.fill((30, 30, 30))

        # Haritayı çiz
        self.harita.ciz(ekran)

        # Oyuncuları çiz
        self.oyuncular.draw(ekran)

        # Oyun devam ediyorsa süreyi güncelle
        if not self.is_game_over:
            self.gecen_zam = (pygame.time.get_ticks() - self.bas_zam) // 1000

        # Süre yazısını oluştur
        zaman_yazi = self.kucuk_font.render(f"{self.gecen_zam}", True, (255, 255, 255))

        # Süre yazısının konumu
        zaman_rect = zaman_yazi.get_rect(center=(405, 30))

        # Süreyi ekrana çiz
        ekran.blit(zaman_yazi, zaman_rect)
    
  
        # Game Over ekranı
        if self.is_game_over:

            # Yarı saydam siyah perde oluştur
            karartma = pygame.Surface((810, 630), pygame.SRCALPHA)
            karartma.fill((0, 0, 0, 150))

            # Perdeyi ekrana çiz
            ekran.blit(karartma, (0, 0))

            # GAME OVER yazısı
            game_over_yazi = self.buyuk_font.render("GAME OVER", True, (255, 0, 0))

            # Yazının ortalanması
            yazi_rect = game_over_yazi.get_rect(center=(400, 300))

            # Yazıyı ekrana çiz
            ekran.blit(game_over_yazi, yazi_rect)
        
            # Yeniden başlatma bilgisi
            bilgi_yazi = self.kucuk_font.render(
                "Yeniden başlamak için 'R' tuşuna basınız",
                True,
                (255, 255, 255)
            )

            # Bilgi yazısının konumu
            bilgi_rect = bilgi_yazi.get_rect(center=(400, 360))

            # Bilgi yazısını çiz
            ekran.blit(bilgi_yazi, bilgi_rect)

        # Bölüm bitirme ekranı
        if self.bolum_bitti_ekrani:

            # Karartma perdesi
            perde = pygame.Surface((810, 630))
            perde.set_alpha(180)
            perde.fill((0,0,0))

            ekran.blit(perde, (0,0))

            # Bölüm tamamlandı yazısı
            yazi1 = self.font_baslik.render(
                "Bölümü Bitirdiniz!",
                True,
                (0,255,0)
            )

            # Sonraki bölüme geçiş bilgisi
            yazi2 = self.font_alt.render(
                "Bir sonraki bölüme geçmek için ENTER'a basınız",
                True,
                (200,200,200)
            )

            # Yazıları ekrana ortalı şekilde çiz
            ekran.blit(yazi1, (810//2 - yazi1.get_width()//2,200))
            ekran.blit(yazi2, (810//2 - yazi2.get_width()//2,320))

        # Oyun tamamen bittiyse
        elif self.oyun_bitti_ekrani:

            # Karartma perdesi
            perde = pygame.Surface((810, 630))
            perde.set_alpha(180)
            perde.fill((0, 0, 0))

            ekran.blit(perde, (0, 0))

            # Tebrik mesajı
            yazi1 = self.font_baslik.render(
                "Tebrikler, Oyunu Bitirdiniz!",
                True,
                (0, 255, 0)
            ) 

            # Menüye dönüş bilgisi
            yazi2 = self.font_alt.render(
                "Menüye dönmek için ESC'ye basınız",
                True,
                (200, 200, 200)
            )
            
            # Yazıları ekrana çiz
            ekran.blit(yazi1, (810//2 - yazi1.get_width()//2, 200))
            ekran.blit(yazi2, (810//2 - yazi2.get_width()//2, 320))