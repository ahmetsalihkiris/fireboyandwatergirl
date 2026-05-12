import pygame

class SesYoneticisi:
    def __init__(self):
        # Ses dosyalarını tutacak değişkenleri başlangıçta boş (None) olarak tanımlıyoruz
        self.elmas_sesi = None
        self.ziplama_sesi = None
        self.olum_sesi = None
        self.muzik_acik = True # Müziğin başlangıçta açık olduğunu belirtiyoruz

    def baslat(self):
        # Pygame'in ses motorunu (mixer) çalıştırıyoruz
        pygame.mixer.init()

        # Zıplama sesini yüklemeyi deniyoruz
        try:
            self.ziplama_sesi = pygame.mixer.Sound("models/ziplama_sesi.wav")
            self.ziplama_sesi.set_volume(1.0) # Ses yüksekliği %100
        except FileNotFoundError:
            pass # Dosya yoksa hata verme, devam et
        
        # Elmas toplama sesini yüklemeyi deniyoruz
        try:
            self.elmas_sesi = pygame.mixer.Sound("models/elmas.wav")
            self.elmas_sesi.set_volume(1.0)
        except FileNotFoundError:
            pass
        
        # Ölme (suya/lava düşme) sesini yüklemeyi deniyoruz
        try:
            self.olum_sesi = pygame.mixer.Sound("models/ciss.wav")
            self.olum_sesi.set_volume(0.3) # Ölüm sesi biraz daha kısık (%30)
        except FileNotFoundError:
            pass
    
    def muzik_durumunu_degistir(self):
        # Müziğin durumunu tersine çeviriyoruz (Açıksa kapat, kapalıysa aç)
        self.muzik_acik = not self.muzik_acik

        if self.muzik_acik:
            pygame.mixer.music.set_volume(1.0) # Sesleri aç
        else:
            pygame.mixer.music.set_volume(0.0) # Sesleri tamamen kıs
        
        return self.muzik_acik
        
    def menu_muzigini_cal(self):
        # Ana menüde çalacak olan müziği yükleyip sonsuz döngüde (-1) başlatıyoruz
        try:
            pygame.mixer.music.load("models/ana_menu.ogg")
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1) # -1 parametresi müziğin bitince tekrar başlamasını sağlar
        except Exception as e:
            print(f"SES HATASI (Oyun): {e}")
        
    def oyun_muzigini_cal(self):
        # Oyun başladığında çalacak olan arka plan müziğini yüklüyoruz
        try:
            pygame.mixer.music.load("models/oyun_ici.ogg")
            pygame.mixer.music.set_volume(0.5) # Oyun içi müziği %50 seviyesinde çal
            pygame.mixer.music.play(-1)
        except Exception as e:
            pass
        
    # Karakter zıpladığında çağrılan fonksiyon
    def ziplama_cal(self):
        if self.ziplama_sesi:
            self.ziplama_sesi.play()
    
    # Elmas toplandığında çağrılan fonksiyon
    def elmas_cal(self):
        if self.elmas_sesi:
            self.elmas_sesi.play()
    
    # Karakter tehlikeli bir yere bastığında çağrılan fonksiyon
    def ciss_cal(self):
        if self.olum_sesi:
            self.olum_sesi.play()
    
# Diğer dosyalardan "ses_motoru" adıyla bu yöneticiye kolayca ulaşabilmek için bir örnek oluşturuyoruz
ses_motoru = SesYoneticisi()