import pygame
import random
import buttons

import time

t = time.localtime()
current_time = time.strftime("%H", t)
current_time = int(current_time)

pygame.init()

score = 0
score_font = pygame.font.Font('assets/ImminentLine.ttf', 50)
white = (255, 255, 255)

game = True
menu = True
main_page = True
replay_menu = True

screen_x = 1280
screen_y = 720

window = pygame.display.set_mode((screen_x, screen_y))

bgOne = pygame.image.load('assets/sprites/720_base.png')
bgTwo = pygame.image.load('assets/sprites/720_base.png')

bgOne_x = 0
bgTwo_x = bgOne.get_width()

bird_mid = pygame.image.load('assets/sprites/bluebird-midflap.png')
bird_up = pygame.image.load('assets/sprites/bluebird-upflap.png')
bird_down = pygame.image.load('assets/sprites/bluebird-downflap.png')

btn_play_yellow = pygame.image.load('assets/sprites/play_btn_yellow.png')
btn_quit_yellow = pygame.image.load('assets/sprites/quit_btn_yellow.png')
btn_menu_yellow = pygame.image.load('assets/sprites/menu_btn_yellow.png')
btn_play_blue = pygame.image.load('assets/sprites/play_btn_blue.png')
btn_quit_blue = pygame.image.load('assets/sprites/quit_btn_blue.png')
btn_menu_blue = pygame.image.load('assets/sprites/menu_btn_blue.png')

play_btn = buttons.button(screen_x/2 - btn_play_yellow.get_width() - 180, screen_y/2 + 100, 212, 64, white, '', btn_play_yellow)
quit_btn = buttons.button(screen_x/2 - btn_play_yellow.get_width(), screen_y/2 + 100, 212, 64, white, '', btn_quit_yellow)
menu_btn = buttons.button(screen_x/2 - btn_play_yellow.get_width() + 180, screen_y/2 + 100, 212, 64, white, '', btn_menu_yellow)

if 7 < current_time < 18:
    background = pygame.image.load('assets/sprites/background_light.png')
else:
    background = pygame.image.load('assets/sprites/background_dark.png')
flappy_bird = pygame.image.load('assets/sprites/flappy_bird.png')
pipe = pygame.image.load('assets/sprites/green_bar.png')

timer_id1 = pygame.USEREVENT
pipe_timer = pygame.time.set_timer(timer_id1, 2000)

fly_sound = pygame.mixer.Sound('assets/audio/wing.wav')
die_sound = pygame.mixer.Sound('assets/audio/hit.wav')
point_sound = pygame.mixer.Sound('assets/audio/point.wav')

high_score = 0

def rot_center(image, angle):
    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


class player:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.width = width + 3
        self.height = height + 10
        self.hit_box = (self.x, self.y, self.width, self.height)

    def draw(self, bird, up):
        self.hit_box = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(window, white, self.hit_box, 1)
        if up:
            window.blit(rot_center(bird, 20), (self.x, self.y))
        else:
            window.blit(rot_center(bird, -20), (self.x, self.y))


class player_pipe:
    def __init__(self):
        self.x_top = 1400
        self.y_top = int(random.uniform(-400, 0))
        self.x_bottom = 1400
        self.y_bottom = self.y_top + 650
        self.top_pipe = rot_center(pipe, 180)
        self.bottom_pipe = pipe


    def draw_pipe(self):
        window.blit(self.top_pipe, (self.x_top, self.y_top))
        window.blit(self.bottom_pipe, (self.x_bottom, self.y_bottom))
        # pygame.draw.rect(window, white, (self.x_top, self.y_top, 80, 500), 1)
        # pygame.draw.rect(window, white, (self.x_bottom, self.y_bottom, 80, 500), 1)

    def check_collision(self, x, y, character):
        if character.x + character.width > self.x_top:
            if character.y < (self.y_top+500) or character.y + character.height > self.y_bottom:
                global game
                global menu
                global main_page
                global replay_menu
                game = False
                menu = True
                main_page = True
                replay_menu = True
                die_sound.play()

pipe_list = []
p1 = player(200, 350, 24, 34)
play_3 = True
play_2 = True
play_1 = True
while menu:
    score = 0
    pipe_list = []
    p1 = player(200, 350, 24, 34)
    while main_page:
        window.blit(background, (0, 0))
        window.blit(bgOne, (bgOne_x, 0))
        window.blit(bgTwo, (bgTwo_x, 0))
        window.blit(flappy_bird, (screen_x/2 - flappy_bird.get_width()/2, 100))
        bgOne_x -= 4
        bgTwo_x -= 4
        if bgOne_x - 1 < -(bgOne.get_width()):
            bgOne_x = bgTwo_x + bgTwo.get_width()
        if bgTwo_x - 1 < -(bgTwo.get_width()):
            bgTwo_x = bgOne_x + bgOne.get_width()
        play_btn.draw(window, False)
        quit_btn.draw(window, False)
        menu_btn.draw(window, False)

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                menu = False
                main_page = False
                replay_menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.is_over(pos):
                    main_page = False
                    game = True
                elif menu_btn.is_over(pos):
                    None
                elif quit_btn.is_over(pos):
                    game = False
                    menu = False
                    main_page = False

            if event.type == pygame.MOUSEMOTION:
                if play_btn.is_over(pos):
                    if play_1:
                        fly_sound.play()
                        play_1 = False
                    play_btn.image = btn_play_blue
                else:
                    play_1 = True
                    play_btn.image = btn_play_yellow
                if menu_btn.is_over(pos):
                    if play_2:
                        fly_sound.play()
                        play_2 = False
                    menu_btn.image = btn_menu_blue
                else:
                    play_2 = True
                    menu_btn.image = btn_menu_yellow
                if quit_btn.is_over(pos):
                    if play_3:
                        fly_sound.play()
                        play_3 = False
                    quit_btn.image = btn_quit_blue
                else:
                    play_3 = True
                    quit_btn.image = btn_quit_yellow

        pygame.display.update()
    while game:
        play_1 = True
        play_2 = True
        play_3 = True
        window.blit(background, (0, 0))
        window.blit(bgOne, (bgOne_x, 0))
        window.blit(bgTwo, (bgTwo_x, 0))

        for ls in pipe_list:
            ls.x_top -= 3
            ls.x_bottom -= 3
            ls.draw_pipe()
            if ls.x_top > p1.x and ls.x_bottom > p1.x:
                ls.check_collision(p1.x, p1.y, p1)
        for ls in pipe_list:
            if ls.x_top < 0 and ls.x_bottom < 0:
                point_sound.play()
                pipe_list.remove(ls)
                score += 1

        keys = pygame.key.get_pressed()
        key_up = keys[pygame.K_SPACE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                menu = False
                replay_menu = False
            if event.type == timer_id1:
                pipe_list.append(player_pipe())
        if key_up and p1.y > 0:
            p1.y -= 12
            p1.draw(bird_up, True)
        else:
            p1.y += 5
            p1.draw(bird_down, False)
        bgOne_x -= 4
        bgTwo_x -= 4

        if bgOne_x - 1 < -(bgOne.get_width()):
            bgOne_x = bgTwo_x + bgTwo.get_width()
        if bgTwo_x - 1 < -(bgTwo.get_width()):
            bgTwo_x = bgOne_x + bgOne.get_width()

        score_text = score_font.render(str(score), True, white)
        window.blit(score_text, (screen_x/2 - score_text.get_width() / 2, 0))

        pygame.display.update()
    while replay_menu:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                menu = False
                main_page = False
                replay_menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.is_over(pos):
                    main_page = False
                    game = True
                    replay_menu = False
                elif menu_btn.is_over(pos):
                    replay_menu = False
                    game = True
                    main_page = True
                elif quit_btn.is_over(pos):
                    game = False
                    menu = False
                    main_page = False
                    replay_menu = False

            if event.type == pygame.MOUSEMOTION:
                if play_btn.is_over(pos):
                    if play_1:
                        fly_sound.play()
                        play_1 = False
                    play_btn.image = btn_play_blue
                else:
                    play_1 = True
                    play_btn.image = btn_play_yellow
                if menu_btn.is_over(pos):
                    if play_2:
                        fly_sound.play()
                        play_2 = False
                    menu_btn.image = btn_menu_blue
                else:
                    play_2 = True
                    menu_btn.image = btn_menu_yellow
                if quit_btn.is_over(pos):
                    if play_3:
                        fly_sound.play()
                        play_3 = False
                    quit_btn.image = btn_quit_blue
                else:
                    play_3 = True
                    quit_btn.image = btn_quit_yellow

        window.blit(background, (0, 0))
        window.blit(bgOne, (bgOne_x, 0))
        window.blit(bgTwo, (bgTwo_x, 0))
        for ls in pipe_list:
            ls.draw_pipe()
        if score > high_score:
            high_score = score
        high_score_text = score_font.render(("High Score: "+str(high_score)), True, white)
        window.blit(high_score_text, (screen_x/2 - high_score_text.get_width() / 2, screen_y/2 - high_score_text.get_height() / 2))
        p1.draw(bird_up, True)
        play_btn.draw(window, False)
        quit_btn.draw(window, False)
        menu_btn.draw(window, False)
        pygame.display.update()

pygame.quit()
