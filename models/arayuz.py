import pygame

class Buton:
    def __init__(self, metin, x, y, genislik, yukseklik, font):
        # Butonun arka plan görselini yüklüyoruz (btn.jpg dosyası klasörde olmalı)
        self.resim = pygame.image.load("btn.jpg").convert()
        # Görseli, buton için belirlediğimiz genişlik ve yüksekliğe göre yeniden boyutlandırıyoruz
        self.resim = pygame.transform.scale(self.resim, (genislik, yukseklik))
        # Butonun ekrandaki konumunu ve çarpışma kutusunu (rect) oluşturuyoruz
        self.rect = self.resim.get_rect(topleft=(x, y))
        
        # Butonun üzerinde yazacak metni ve yazı tipini ayarlıyoruz
        self.metin = metin
        self.font = font
        # Metni beyaz renkte (255, 255, 255) bir yüzeye çiziyoruz
        self.yazi_yuzeyi = self.font.render(self.metin, True, (255, 255, 255))
        # Yazıyı, butonun tam ortasına gelecek şekilde hizalıyoruz
        self.yazi_rect = self.yazi_yuzeyi.get_rect(center=self.rect.center)
        
        # MASKE SİSTEMİ: Fare üzerine geldiğinde butonun kararması için yarı saydam bir yüzey
        self.maske = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)
        # Siyah rengin üzerine 100 değeriyle saydamlık veriyoruz (0-255 arası)
        self.maske.fill((50, 50, 50, 100))

    def ciz(self, ekran):
        # Fare koordinatlarını anlık olarak alıyoruz
        fare_konumu = pygame.mouse.get_pos()
        # Önce butonun ana görselini ekrana çiziyoruz
        ekran.blit(self.resim, self.rect)
        
        # ÇARPIŞMA KONTROLÜ: Eğer fare butonun üzerindeyse maskeyi çiz (buton kararır)
        if self.rect.collidepoint(fare_konumu):
            ekran.blit(self.maske, self.rect)
            
        # Son olarak en üste butonun metnini çiziyoruz
        ekran.blit(self.yazi_yuzeyi, self.yazi_rect)

    def tiklandi_mi(self, event):
        # Eğer bir fare tıklaması olduysa ve bu "Sol Tık" (button == 1) ise
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Tıklanan nokta butonun sınırları içindeyse 'True' döndür
            if self.rect.collidepoint(event.pos):
                return True
        # Tıklanmadıysa veya buton dışında tıklandıysa 'False' döndür
        return False