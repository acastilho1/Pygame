import pygame

# Inicialização do Pygame
pygame.init()

# Definição de constantes
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 150
PADDLE_SPEED = 8
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 12, 12
FPS = 60
WHITE = (255, 255, 255)

# Criação da janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - 2 Players")
clock = pygame.time.Clock()

# Classe da bola
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Colisão com as bordas verticais
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def bounce(self):
        self.speed_x *= -1

# Classe do jogador/paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = 0

    def update(self):
        self.rect.y += self.speed_y

        # Limita o paddle à tela
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

# Criação dos grupos de sprites
all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()

# Criação da bola e paddles para cada jogador
ball = Ball()
all_sprites.add(ball)

player1_paddle = Paddle(30, HEIGHT // 2)
all_sprites.add(player1_paddle)
paddles.add(player1_paddle)

player2_paddle = Paddle(WIDTH - 30, HEIGHT // 2)
all_sprites.add(player2_paddle)
paddles.add(player2_paddle)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1_paddle.speed_y = -PADDLE_SPEED
            elif event.key == pygame.K_s:
                player1_paddle.speed_y = PADDLE_SPEED
            elif event.key == pygame.K_UP:
                player2_paddle.speed_y = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                player2_paddle.speed_y = PADDLE_SPEED

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_paddle.speed_y = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_paddle.speed_y = 0

    # Atualizaçõesws
    all_sprites.update()

    # Colisão com paddles
    hits = pygame.sprite.spritecollide(ball, paddles, False)
    if hits:
        ball.bounce()

    # Verifica colisão com as bordas horizontais
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.speed_x *= -1

    # Verifica se a bola saiu da tela
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x *= BALL_SPEED_X
        ball.speed_y *= BALL_SPEED_Y

    # Renderização
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, player1_paddle)
    pygame.draw.rect(screen, WHITE, player2_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    pygame.display.flip()
    clock.tick(FPS)

# Encerra o Pygame
pygame.quit()
