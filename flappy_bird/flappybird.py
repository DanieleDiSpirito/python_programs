#librerie:
import pygame
import random

pygame.init()
pygame.mixer.init()

#immagini:
sfondo = pygame.image.load('C:/Users/danie/python_programs/pygame_games/Flappy Bird/sfondo.png')
bird = pygame.image.load('C:/Users/danie/python_programs/pygame_games/Flappy Bird/uccello.png')
base = pygame.image.load('C:/Users/danie/python_programs/pygame_games/Flappy Bird/base.png')
tubo_giu = pygame.image.load('C:/Users/danie/python_programs/pygame_games/Flappy Bird/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)
gameover = pygame.image.load('C:/Users/danie/python_programs/pygame_games/Flappy Bird/gameover.png')

#musica:
#musica = pygame.mixer.music.load('C:/Users/Asus/Downloads/Flappy Bird Theme Song.mp3')

#costanti globali:
SCHERMO = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird DDS&MC")
FPS = 50
VEL_AVANZ = 3
FONT = pygame.font.SysFont('Times New Roman', 72, bold=False) #scritta (bold = grassetto)
SCRITTA_INIZIALE = pygame.font.SysFont('Times New Roman', 20)

#classi:
class tubi_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint (-75, 150)
    def avanza_e_disegna(self):
        self.x -= VEL_AVANZ
        SCHERMO.blit(tubo_giu, (self.x, self.y + 210))
        SCHERMO.blit(tubo_su, (self.x, self.y - 210))
    def collisione(self, bird, birdx, birdy):
        tolleranza = 5
        bird_lato_dx = birdx + bird.get_width() - tolleranza
        bird_lato_sx = birdx + tolleranza
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        bird_lato_su = birdy + tolleranza
        bird_lato_giu = birdy + bird.get_height() - tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        if (bird_lato_dx > tubi_lato_sx and bird_lato_sx < tubi_lato_dx):
            if (bird_lato_su < tubi_lato_su or bird_lato_giu > tubi_lato_giu):
                hai_perso() #sconfitta
    def fra_i_tubi(self, bird, birdx):
        tolleranza = 5
        bird_lato_dx = birdx + bird.get_width() - tolleranza
        bird_lato_sx = birdx + tolleranza
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        if (bird_lato_dx > tubi_lato_sx and bird_lato_sx < tubi_lato_dx):
            return True
#funzioni:
def disegna_oggetti():
    SCHERMO.blit(sfondo, (0,0))
    for t in tubi:
        t.avanza_e_disegna()
    SCHERMO.blit(bird, (birdx, birdy))
    SCHERMO.blit(base, (basex, 400))
    punti_render = FONT.render(str(punti), 1, (0,0,0)) #colore in rgb
    SCHERMO.blit(punti_render, (136,0))

def scrittura_iniziale():
    global scritta
    scritta = 'Clicca \'SPAZIO\' per iniziare'
    scrittura_iniziale = SCRITTA_INIZIALE.render(str(scritta), 1, (0,0,0))
    SCHERMO.blit(scrittura_iniziale, (40, 200))

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    
def inizializza():
    global birdx, birdy, bird_vely
    global basex
    global tubi
    global punti
    global fra_i_tubi
    global inizio
    global Record
    punti = 0
    birdx, birdy = 60, 130
    bird_vely = 0 #velocità in y
    basex = 0
    tubi = []
    tubi.append(tubi_classe())
    fra_i_tubi = False
    inizio = False

def hai_perso():
    SCHERMO.blit(gameover, (50, 180))
    aggiorna()
    ricominciamo = False
    while not ricominciamo:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                inizializza()
                ricominciamo = True
            if event.type == pygame.QUIT:
                pygame.quit()

def record_punteggio():
    global Record
    scritta_record = 'RECORD: ' + str(Record)
    if (Record<punti):
        Record = punti
        scritta_record = 'new RECORD: ' + str(Record)
        with open('C:/Users/danie/python_programs/pygame_games/Flappy Bird/record.txt', 'w') as file_:
            print(Record, file=file_)
            file_.close()
    scrittura_record = SCRITTA_INIZIALE.render(str(scritta_record), 1, (0,0,0))
    SCHERMO.blit(scrittura_record, (160, 480))

#codice principale:
inizializza()

SCHERMO.blit(sfondo, (0,0))
SCHERMO.blit(bird, (birdx, birdy))
SCHERMO.blit(base, (basex, 400))
with open('C:/Users/danie/python_programs/pygame_games/Flappy Bird/record.txt', 'r') as file_:
    Record = int(file_.read())
    file_.close()

while True:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            inizio = True
    if event.type == pygame.QUIT:
        pygame.quit()
    record_punteggio()
    aggiorna()
    scrittura_iniziale()
    #riproduzione musica:
    #musica = pygame.mixer.music.play(-1)
    while inizio:
        basex -= VEL_AVANZ
        if basex < -45: basex = 0
        bird_vely += 1
        birdy += bird_vely
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                bird_vely = -8;
            if event.type == pygame.QUIT:
                pygame.quit()
        if tubi[-1].x < 150: tubi.append(tubi_classe())
        for t in tubi:
            t.collisione(bird, birdx, birdy)
        if not fra_i_tubi:
            for t in tubi:
                if t.fra_i_tubi(bird, birdx):
                    fra_i_tubi = True
                    break
        if fra_i_tubi:
            fra_i_tubi = False
            for t in tubi:
                if t.fra_i_tubi(bird, birdx):
                    fra_i_tubi = True
                    break
            if not fra_i_tubi:
                punti += 1
        if (birdy > 380 or birdy < 0): 
            hai_perso() #sconfitta
        record_punteggio() 
        disegna_oggetti()
        aggiorna()
















