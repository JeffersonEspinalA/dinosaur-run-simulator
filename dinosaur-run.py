import sys, pygame
import random

ANCHO = 700
ALTO = 400

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

FPS = 30

class Dinosaurio(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites_corriendo = [pygame.transform.scale(pygame.image.load("img/dino_corriendo1.png").convert(), (70, 70)),
                                  pygame.transform.scale(pygame.image.load("img/dino_corriendo2.png").convert(), (70, 70))]
        self.sprites_agachado = [pygame.transform.scale(pygame.image.load("img/dino_agachado1.png").convert(), (70, 40)),
                                 pygame.transform.scale(pygame.image.load("img/dino_agachado2.png").convert(), (70, 40))]
        self.sprites_salto = pygame.transform.scale(pygame.image.load("img/dino_saltando.png").convert(), (70, 70))
        self.img_actual = 0
        self.image = self.sprites_corriendo[self.img_actual]
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = 15
        self.rect.y = 255
        self.correr = False
        self.agachado = False
        self.salto = False
        #self.velocidad_salto = 8.5
        self.velocidad_salto = 8.5

    def update(self):
        teclas = pygame.key.get_pressed()

        if self.agachado:
            self.animar_agachar()
        if self.correr:
            self.animar_correr()
        if self.salto:
            self.animar_salto()

        if (teclas[pygame.K_UP] or teclas[pygame.K_SPACE]) and not self.salto:
            self.agachado = False
            self.correr = False
            self.salto = True
        elif teclas[pygame.K_DOWN] and not self.salto:
            self.agachado = True
            self.correr = False
            self.salto = False
        elif not (self.salto or teclas[pygame.K_DOWN]):
            self.agachado = False
            self.correr = True
            self.salto = False

    def animar_salto(self):
        self.image = self.sprites_salto
        self.image.set_colorkey(BLANCO)
        if self.salto:
            self.rect.y -= self.velocidad_salto * 3
            self.velocidad_salto -= 0.8
        if self.velocidad_salto < -8.5:
            self.salto = False
            self.velocidad_salto = 8.5

    def animar_correr(self):
        self.rect.y = 255
        self.img_actual += 0.2
        if self.img_actual >= 2:
            self.img_actual = 0
        self.image = self.sprites_corriendo[int(self.img_actual)]
        self.image.set_colorkey(BLANCO)

    def animar_agachar(self):
        self.rect.y = 285
        self.img_actual += 0.2
        if self.img_actual >= 2:
            self.img_actual = 0
        self.image = self.sprites_agachado[int(self.img_actual)]
        self.image.set_colorkey(BLANCO)

class Pterosaurio(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [pygame.transform.scale(pygame.image.load("img/pterosaurio1.png").convert(), (60, 40)),
                       pygame.transform.scale(pygame.image.load("img/pterosaurio2.png").convert(), (60, 40))]
        self.img_actual = 0
        self.image = self.sprites[self.img_actual]
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.y = random.randrange(180, 265)
        self.rect.x = ANCHO
        self.velocidad_x = 9

    def update(self, puntaje):
        if puntaje % 100 == 0:
            self.velocidad_x += 1
        self.animar()
        self.rect.x -= self.velocidad_x
        if self.rect.right < 0:
            self.kill()

    def animar(self):
        self.img_actual += 0.2
        if self.img_actual >= 2:
            self.img_actual = 0
        self.image = self.sprites[int(self.img_actual)]
        self.image.set_colorkey(BLANCO)

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagenes = [pygame.transform.scale(pygame.image.load("img/cactus1.png").convert(), (30, 40)),
                       pygame.transform.scale(pygame.image.load("img/cactus2.png").convert(), (40, 40)),
                       pygame.transform.scale(pygame.image.load("img/cactus3.png").convert(), (50, 40)),
                       pygame.transform.scale(pygame.image.load("img/cactus4.png").convert(), (30, 50)),
                       pygame.transform.scale(pygame.image.load("img/cactus5.png").convert(), (40, 50)),
                       pygame.transform.scale(pygame.image.load("img/cactus6.png").convert(), (50, 50))]
        self.tipo = random.randrange(0, 6)
        self.image = self.imagenes[self.tipo]
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        if self.tipo < 3:
            self.rect.y = 280
            self.radius = 20
        else:
            self.rect.y = 270
            self.radius = 25
        self.rect.x = ANCHO
        self.velocidad_x = 10

    def update(self, puntaje):
        if puntaje % 100 == 0:
            self.velocidad_x += 1
        self.rect.x -= self.velocidad_x
        if self.rect.right < 0:
            self.kill()

    def actualizar_velocidad(self):
        self.velocidad_x += 1
        print(self.velocidad_x)

class Nube(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/nube.png")
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(100, 150)
        self.rect.x = ANCHO
        self.velocidad_x = 6

    def update(self, puntaje):
        if puntaje % 100 == 0:
            self.velocidad_x += 1
        self.rect.x -= self.velocidad_x
        if self.rect.right < 0:
            self.kill()

pygame.init()

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dinosaur Run Simulator")

icono = pygame.image.load("img/icono.png")
pygame.display.set_icon(icono)
clock = pygame.time.Clock()

PANTALLA.fill(BLANCO)

def mostrar_piso(pantalla):
    pygame.draw.line(pantalla, NEGRO, (0, 310), (700, 310), 1)
    

def mostrar_texto(pantalla, texto, x, y):
    tipo_letra = pygame.font.Font('font/PressStart2P-Regular.ttf', 20)
    superficie = tipo_letra.render(texto, True, NEGRO)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    pantalla.blit(superficie, rectangulo)

def fin_del_juego(pantalla, puntacion):
    tipo_letra1 = pygame.font.Font('font/PressStart2P-Regular.ttf', 30)
    game_over_text = tipo_letra1.render("G A M E   O V E R", True, NEGRO)
    game_over_rect = game_over_text.get_rect(center=(ANCHO / 2, 180))
    tipo_letra2 = pygame.font.Font('font/PressStart2P-Regular.ttf', 20)
    score_text = tipo_letra2.render(f"S C O R E :  {int(puntacion)}", True, NEGRO)
    score_rect = score_text.get_rect(center=(ANCHO / 2, 220))
    pantalla.blit(game_over_text, game_over_rect)
    pantalla.blit(score_text, score_rect)

sprites = pygame.sprite.Group()
cactus = pygame.sprite.Group()
nubes = pygame.sprite.Group()
pterosaurios = pygame.sprite.Group()

jugador = Dinosaurio()
sprites.add(jugador)

game_over = False
puntaje = 0
ejecutando = True
obstaculo_temporizador = 0
obstaculo_aparicion = False
obstaculo_enfriamiento = 1000

while ejecutando:
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    colision_jugador_cactus = pygame.sprite.spritecollide(jugador, cactus, False, pygame.sprite.collide_circle)

    if colision_jugador_cactus:
        game_over = True

    colision_jugador_pterosaurio = pygame.sprite.spritecollide(jugador, pterosaurios, False, pygame.sprite.collide_circle)
    if colision_jugador_pterosaurio:
        game_over = True

    if puntaje > 99999:
        game_over = True

    if game_over:
        PANTALLA.fill(BLANCO)
        fin_del_juego(PANTALLA, puntaje)

    if not game_over:
        puntaje += 0.5

        if pygame.time.get_ticks() - obstaculo_temporizador >= obstaculo_enfriamiento:
            obstaculo_aparicion = True

        if obstaculo_aparicion:
            random_obstacuclo = random.randrange(1, 50)

            if random_obstacuclo in range(1, 7):
                cactus.add(Cactus())
                obstaculo_temporizador = pygame.time.get_ticks()
                obstaculo_aparicion = False

            elif random_obstacuclo in range(7, 13) and puntaje > 200:
                pterosaurios.add(Pterosaurio())
                obstaculo_temporizador = pygame.time.get_ticks()
                obstaculo_aparicion = False

        if random.randrange(1, 200) < 7:
            nubes.add(Nube())

        sprites.update()
        cactus.update(puntaje)
        nubes.update(puntaje)
        pterosaurios.update(puntaje)

        PANTALLA.fill(BLANCO)
    
        mostrar_piso(PANTALLA)
        sprites.draw(PANTALLA)
        cactus.draw(PANTALLA)
        nubes.draw(PANTALLA)
        pterosaurios.draw(PANTALLA)

        mostrar_texto(PANTALLA, "SCORE", 520, 20)
        mostrar_texto(PANTALLA, str(int(puntaje)).zfill(5), 630, 20)
    
    pygame.display.flip()    

pygame.quit()