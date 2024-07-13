import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.1)
music = pygame.mixer.music.load('Box.mp3')
pygame.mixer.music.play(-1)

colision = pygame.mixer.Sound('smw_coin.wav')
colision.set_volume(1.0)

apple_image = pygame.image.load('apple_alt_32.png')
apple_image = pygame.transform.scale(apple_image, (20, 20))

obstacle_image = pygame.image.load('bomb_32.png')
obstacle_image = pygame.transform.scale(obstacle_image, (20, 20))

head_image = pygame.image.load('snake_green_head_32.png')
head_image = pygame.transform.scale(head_image, (20, 20))

body_image = pygame.image.load('snake_green_blob_32.png')
body_image = pygame.transform.scale(body_image, (20, 20))

flower_image = pygame.image.load('Bush.png')
flower_positions = [(randint(40, 600), randint(50, 430)) for _ in range(5)]

width = 640
height = 480

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Estudando python fluente')
clock = pygame.time.Clock()

x_snake = int(width / 2)
y_snake = int(height / 2)

run = 10
x_control = 20
y_control = 0

x_apple = randint(40, 600)
y_apple = randint(50, 430)


obstacles = []
for _ in range(7):
    obstacles.append((randint(40, 600), randint(50, 430)))

font = pygame.font.SysFont('arial', 40, True, False)
point = 0

list_snake = []
width_initial = 5

dead = False

def snake_movement(list_snake):
    for i, XeY in enumerate(list_snake):
        if i == len(list_snake) - 1:
            screen.blit(head_image, XeY)
        else:
            screen.blit(body_image, XeY)

def reinitialize():
    global point, width_initial, x_snake, y_snake, list_snake, list_head, x_apple, y_apple, dead, obstacles
    point = 0
    width_initial = 5
    x_snake = int(width / 2)
    y_snake = int(height / 2)
    list_snake = []
    list_head = []
    x_apple = randint(40, 600)
    y_apple = randint(50, 430)
    dead = False
    obstacles = []
    for _ in range(7):
        obstacles.append((randint(40, 600), randint(50, 430)))

while True:
    clock.tick(30)
    screen.fill((0, 128, 0))
    message = f"Ponto: {point}"
    text_format = font.render(message, False, (0, 0, 0))

    # Desenha as flores
    for pos in flower_positions:
        screen.blit(flower_image, pos)


    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if x_control == run:
                    pass
                else:
                    x_control = -run
                    y_control = 0
            if event.key == K_RIGHT:
                if x_control == -run:
                    pass
                else:
                    x_control = run
                    y_control = 0
            if event.key == K_UP:
                if y_control == run:
                    pass
                else:
                    y_control = -run
                    x_control = 0
            if event.key == K_DOWN:
                if y_control == -run:
                    pass
                else:
                    y_control = run
                    x_control = 0

    x_snake += x_control
    y_snake += y_control
    snake = pygame.draw.rect(screen, (0, 255, 0), (x_snake, y_snake, 20, 20))
    apple = screen.blit(apple_image, (x_apple, y_apple))


    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle)
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 20, 20)
        if snake.colliderect(obstacle_rect):
            dead = True

    if snake.colliderect(apple):
        point += 1
        x_apple = randint(40, 600)
        y_apple = randint(50, 430)
        colision.play()
        width_initial += 1

    list_head = []
    list_head.append(x_snake)
    list_head.append(y_snake)
    list_snake.append(list_head)

    if list_snake.count(list_head) > 1 or dead:
        font2 = pygame.font.SysFont('arial', 20, True, False)
        message2 = "Game Over PRESSIONE ENTER PARA JOGAR NOVAMENTE"
        text_format2 = font2.render(message2, True, (0, 0, 0))
        ret_text = text_format2.get_rect()

        dead = True
        while dead:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        reinitialize()
            ret_text.center = (width // 2, height // 2)
            screen.blit(text_format2, ret_text)
            pygame.display.update()

    if x_snake > width:
        x_snake = 0
    if x_snake < 0:
        x_snake = width
    if y_snake > height:
        y_snake = 0
    if y_snake < 0:
        y_snake = height

    if len(list_snake) > width_initial:
        del list_snake[0]

    snake_movement(list_snake)
    screen.blit(text_format, (10, 10))
    pygame.display.update()