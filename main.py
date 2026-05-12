import pygame
import sys
from states.menu import Menu
from states.game import Oyun
from states.seviye_secim import seviye_secim
from models.muzik import ses_motoru


class Kontrol:
    def __init__(self):
        pygame.init()

        ses_motoru.baslat()
        ses_motoru.menu_muzigini_cal()

        self.tam_ekran_mi = False
        self.ekran = pygame.display.set_mode((810, 630))
        pygame.display.set_caption("Ateş ve Su")
        self.clock = pygame.time.Clock()
        
        self.states = {
            "MENU": Menu(),
            "LEVEL_SELECT": seviye_secim(),
            "GAME": Oyun(seviye=1),

        }
        self.state = self.states["MENU"]

    def change_state(self):
        next_state_name = self.state.next_state
        self.state.done = False 
        
        if next_state_name == "GAME":
            
            if hasattr(self.state, 'secilen_seviye'):
                hedef_seviye = self.state.secilen_seviye
            else:
                hedef_seviye = 1 
                
            self.states["GAME"] = Oyun(seviye=hedef_seviye) 
            
            ses_motoru.oyun_muzigini_cal()
        
        elif next_state_name == "MENU":
            ses_motoru.menu_muzigini_cal()
            
        self.state = self.states[next_state_name]    

    def run(self):
        while True:
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Q tuşuna basıldı! Kapatılıyor...")
                        self.quit_game()
    
                    if event.key == pygame.K_RETURN and (pygame.key.get_mods() & pygame.KMOD_ALT):
                        self.tam_ekran_mi = not self.tam_ekran_mi
                        if self.tam_ekran_mi:
                            self.ekran = pygame.display.set_mode((810, 630), pygame.FULLSCREEN | pygame.SCALED)
                        else:
                            self.ekran = pygame.display.set_mode((810, 630))

  
            if self.state.quit:
                self.quit_game()

            if self.state.done:
                self.change_state()

            self.state.handle_events(events)
            self.state.update()
            self.state.draw(self.ekran)
            
            pygame.display.flip()
            self.clock.tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Kontrol()
    app.run()