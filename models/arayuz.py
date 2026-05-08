import pygame

class Buton:
    def __init__(self, metin, x, y, genislik, yukseklik, font):
        self.resim = pygame.image.load("btn.jpg").convert()
        self.resim = pygame.transform.scale(self.resim, (genislik, yukseklik))
        self.rect = self.resim.get_rect(topleft=(x, y))
        
        self.metin = metin
        self.font = font
        self.yazi_yuzeyi = self.font.render(self.metin, True, (255, 255, 255))
        self.yazi_rect = self.yazi_yuzeyi.get_rect(center=self.rect.center)
        
        self.maske = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)
        self.maske.fill((50, 50, 50, 100))

    def ciz(self, ekran):
        fare_konumu = pygame.mouse.get_pos()
        ekran.blit(self.resim, self.rect)
        
        if self.rect.collidepoint(fare_konumu):
            ekran.blit(self.maske, self.rect)
            
        ekran.blit(self.yazi_yuzeyi, self.yazi_rect)

    def tiklandi_mi(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False