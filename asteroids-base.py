# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time
from os import path

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

#Carregar todos os assets.
def load_assets(img_dir, snd_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir,"playerShip1_orange.png")).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir,"meteorBrown_med1.png")).convert()
    assets["tiro_img"] = pygame.image.load(path.join(img_dir,"laserRed16.png")).convert()
    assets["background"] = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir,"expl3.wav"))
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    assets["dest_sound"] = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    explosion_anim = []
    for i in range(9):
        filename = "regularExplosion0{}.png".format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (32,32))
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    return assets

#Classe do jogador que representa nave.
class Player(pygame.sprite.Sprite):
    
    #Construtor da classe.
    def __init__(self, player_img):
        #Construtor da classe pai.
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem do fundo
        self.image = player_img
        
        #Diminui o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        #Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #Detalhe sobre posicionamento.
        self.rect = self.image.get_rect()
        
        #Centraliza no baixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        #Velocidade da nave
        self.speedx = 0
        
        #Melhora colisao.
        self.radius = 25
        
    def update(self):
        self.rect.x += self.speedx
        
        #Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
            
class Tiro(pygame.sprite.Sprite):
    #Construtor da classe.
    def __init__(self, tiro_img, x, y):
        #Construtor classe pai.
        pygame.sprite.Sprite.__init__(self)
        #Carregando imagem.
        
        self.image = tiro_img
        
        #Tamanho da imagem
        self.image = pygame.transform.scale(tiro_img, (10, 40))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK)
        
        #Detalhe sobre o posicionamento
        self.rect = self.image.get_rect()
        
        self.rect.centerx = x
        self.rect.bottom = y
       
        #Velocidade tiro
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
    
        if self.rect.bottom < 0:
            self.kill()
        
class Mob(pygame.sprite.Sprite):
    #Construtor da classe.
    def __init__ (self, mob_img):
    #Construtor da clase pai
        pygame.sprite.Sprite.__init__(self)
    
        #Carregando imagem
        mob_img = assets["mob_img"]
        self.image = mob_img
        
        #Diminui o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK) #PAREI AQUIII
        
        #Detalhe sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        #Posicionamento do meteoro.
        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.centery = random.randrange(-100, -40)
        
        #Velocidade asteroid
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)
        
        #Melhora colisao.
        self.radius = int(self.rect.width * .85 / 2)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.centerx = random.randrange(0, WIDTH)
            self.rect.centery = random.randrange(-100, -40)
        if self.rect.bottom > HEIGHT:
            self.rect.centerx = random.randrange(0, WIDTH)
            self.rect.centery = random.randrange(-100, -40)
            
class Explosion(pygame.sprite.Sprite):
    #Construtor de classe.
    def __init__ (self, center, explosion_anim):
        #Construtor de classe pai.
        pygame.sprite.Sprite.__init__(self)
        
        #Carregar animacao de explosao.
        self.explosion_anim = explosion_anim
        
        #Inicia processo de animacao.
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        #Guarda tick da primeira imagem
        self.last_update = pygame.time.get_ticks()
        
        #Controlle de ticks da animacao 1 tick = 1 milisegundo
        self.frame_ticks = 50
    
    def update(self):
        #Verifica tick atual.
        now = pygame.time.get_ticks()
        
        #Verifica quantos ticks passaram des da ultima mudanca de frame
        elapsed_tick = now - self.last_update
        
        #Se ja esta na hora de mudar de imagem.
        if (elapsed_tick > self.frame_ticks):
            
            #Marca o tick da nova imagem.
            self.last_update = now
            
            #Avanca um quadro.
            self.frame += 1
            
            #Verifica se acabou a animacao.
            if self.frame == len(self.explosion_anim):
                #Se sim mate explosao.
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 
        

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

#Carrega todos os assets de uma vez e guarda em um dicionario
assets = load_assets(img_dir, snd_dir)

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets["background"]
background_rect = background.get_rect()

#Carregar som
pygame.mixer.music.load(path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)
boom_sound = assets['boom_sound']
pew_sound = assets['pew_sound']
dest_sound = assets['dest_sound']

#Cria uma nave chamando a classe 
player = Player(assets["player_img"])


#Cria um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range (0,8):
    n = Mob(assets['mob_img'])
    all_sprites.add(n)
    mobs.add(n)



# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops =- 1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                if event.key == pygame.K_SPACE:
                    pew_sound.play()
                    bullet = Tiro(assets["tiro_img"], player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    
                  
                    

                
                    
            #Verifica se alguma tecla soltou.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
            
        #Depois de cada evento
        #Atualizar as sprites
     
        all_sprites.update()
        
        
        bullet_hit = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in bullet_hit:
            dest_sound.play()
            m = Mob(assets["mob_img"])
            all_sprites.add(m)
            mobs.add(m)
            
            #No lugar do meteoro add explisao anim.
            explosao = Explosion(hit.rect.center, assets["explosion_anim"])
            all_sprites.add(explosao)
            
        #Checa colisao.
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        #Toca som se bater
        if hits:
            boom_sound.play()
            time.sleep(1)
            
            running = False
        
            
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
