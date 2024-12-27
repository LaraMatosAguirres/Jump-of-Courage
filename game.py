import pgzrun
from pgzero import actor
import random

# Tocar música de fundo
music.play("background")  
music.set_volume(0.5)

# Configurações do jogo
WIDTH = 586
HEIGHT = 360
TITLE = "Platformer Adventure"

# Criando o sprite 'platform' com a imagem 'platform.png' localizada na pasta 'images'
platform = actor.Actor('platform')
hero1 = actor.Actor("hero1")
enemy1 = actor.Actor("enemy1")
enemy2 = actor.Actor("enemy2")
enemy3 = actor.Actor("enemy3")
enemy4 = actor.Actor("enemy4")

# Variáveis de controle do herói
hero1.x = 290
hero1.y = 260  # Posição inicial do herói
jumping = False  # Verifica se o herói está pulando
velocity_y = 0  # Velocidade vertical do herói
gravity = 0.5  # Gravidade que atrai o herói para baixo
jump_strength = -10  # Força do pulo
jump_height = 200  # Altura máxima do pulo
move_speed = 5

# Velocidade de movimento dos inimigos
enemy_speed = 2

# Inicializando os inimigos em posições diferentes
enemy1.x = 200
enemy1.y = 260

enemy2.x = 350
enemy2.y = 260

enemy3.x = 450
enemy3.y = 260

enemy4.x = 100
enemy4.y = 260

# Criar um dicionário para armazenar o estado de direção dos inimigos
enemy_directions = {
    enemy1: random.choice([True, False]),  # Aleatório, True = esquerda, False = direita
    enemy2: random.choice([True, False]),
    enemy3: random.choice([True, False]),
    enemy4: random.choice([True, False])
}

# Variáveis de estado do jogo
game_over = False
enemies_active = False  # Indica se os inimigos já começaram a se mover

# Variáveis para instrução inicial piscando
show_instruction = True  # Controla se a instrução está visível

# Função que ativa os inimigos após 5 segundos
def activate_enemies():
    global enemies_active
    enemies_active = True

# Programar a ativação dos inimigos após 5 segundos
clock.schedule_unique(activate_enemies, 5)

# Função que alterna a visibilidade da instrução inicial
def toggle_instruction():
    global show_instruction
    show_instruction = not show_instruction

# Programar a alternância da instrução a cada 0,5 segundos durante os 5 primeiros segundos
for i in range(10):
    clock.schedule(toggle_instruction, i * 0.5)

# Função que verifica se o herói está tocando o chão
def is_on_ground():
    return hero1.y >= 260  # Supondo que a plataforma está na altura 260

def update(dt):
    global velocity_y
    global jumping
    global game_over

    if game_over:
        return  # Se o jogo acabou, não faz mais nada

    # Aplicar a gravidade
    velocity_y += gravity

    # Atualizar a posição do herói
    hero1.y += velocity_y

    # Impedir que o herói ultrapasse a plataforma
    if hero1.y >= 260:
        hero1.y = 260
        velocity_y = 0
        jumping = False

    # Lógica de pulo
    if keyboard.space and not jumping:
        velocity_y = jump_strength  # Aplica a força do pulo
        jumping = True

    if jumping and hero1.y <= 260 - jump_height:
        velocity_y = 0  # Interrompe o pulo quando atingir a altura máxima
        jumping = False

    # Movimento do personagem para frente e para trás com limites de tela
    if keyboard.left:
        if hero1.x > 0:  # Impede que o personagem ultrapasse o lado esquerdo da tela
            hero1.x -= move_speed  # Move para a esquerda
    if keyboard.right:
        if hero1.x < WIDTH - hero1.width:  # Impede que o personagem ultrapasse o lado direito da tela
            hero1.x += move_speed  # Move para a direita

    # Movimento dos inimigos apenas se estiverem ativos
    if enemies_active:
        move_enemy(enemy1)
        move_enemy(enemy2)
        move_enemy(enemy3)
        move_enemy(enemy4)

        # Verificar colisão entre o herói e os inimigos
        if check_collision(hero1, enemy1) or check_collision(hero1, enemy2) or check_collision(hero1, enemy3) or check_collision(hero1, enemy4):
            game_over = True
            music.stop()  # Para a música ao detectar "game over"


# Função para verificar colisão entre dois atores
def check_collision(actor1, actor2):
    # Verifica se há sobreposição nas coordenadas (considerando o tamanho dos atores)
    return actor1.colliderect(actor2)

# Função para mover os inimigos
def move_enemy(enemy):
    # Acessar a direção do inimigo usando o dicionário
    moving_left = enemy_directions[enemy]
    
    # Mover para a direita
    if not moving_left:
        enemy.x += enemy_speed
    else:
        enemy.x -= enemy_speed
    
    # Quando o inimigo atinge a borda da tela, mudar a direção
    if enemy.x <= 0:
        enemy_directions[enemy] = False  # Mudar direção para direita
    elif enemy.x >= WIDTH - enemy.width:
        enemy_directions[enemy] = True  # Mudar direção para esquerda

def draw():
    # Se o jogo acabou, desenha a tela preta com a mensagem de "Você morreu"
    if game_over:
        screen.fill((0, 0, 0))  # Tela preta
        screen.draw.text("Você morreu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color=(255, 0, 0))
        return  # Não desenha mais nada depois disso

    # Desenha o fundo e os sprites
    screen.fill((135, 206, 235))  # Cor de fundo (céu)
    platform.draw()  # Desenha a plataforma
    hero1.draw()  # Desenha o herói
    enemy1.draw()  # Desenha os inimigos
    enemy2.draw()
    enemy3.draw()
    enemy4.draw()

    # Mostrar instrução inicial piscando nos primeiros 5 segundos
    if not enemies_active and show_instruction:
        screen.draw.text("Aperte espaço para pular e as setas para andar", 
                         center=(WIDTH // 2, HEIGHT // 4 - 20), 
                         fontsize=30, 
                         color=(0, 0, 0))
        screen.draw.text(" para desviar dos fantasmas", 
                         center=(WIDTH // 2, HEIGHT // 4 + 20), 
                         fontsize=30, 
                         color=(0, 0, 0))

# Inicia o jogo
pgzrun.go()
