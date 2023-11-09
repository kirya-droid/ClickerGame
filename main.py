import pygame
import sys
import math
import random
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent

# Instantiate the client with the user's username

client: TikTokLiveClient = TikTokLiveClient(unique_id="@akuna_atata")
# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

from moviepy.editor import VideoFileClip

# Инициализация pygame
pygame.init()

# Создание списка для падающих печенек
falling_cookies = []
clicked_cookies = []

# Установка размера окна
screen = pygame.display.set_mode((400, 800))
background = pygame.Surface((400, 800))

# Установка заголовка окна
pygame.display.set_caption("Clicker")

# Загрузка изображения печенья
cookie = pygame.image.load('venv/image/cook.png')

# Загрузка изображения солнечных лучей
sun_rays = pygame.image.load('venv/image/sun.png')

# Изменение размера изображений
cookie = pygame.transform.scale(cookie, (100, 100))
sun_rays = pygame.transform.scale(sun_rays, (300, 300))

# Создание уменьшенной версии печенья
small_cookie = pygame.transform.scale(cookie, (96, 96))

# Установка шрифта и размера
font = pygame.font.Font('venv/fonts/Lolitta.ttf', 25)
# Начальное количество кликов
clicks = 0
streak = 0
last_click = 0
current_streak = 1
target_streak = 1
blink_state = True
fade_state = 0
fade_speed = 1
idle_time = 0

# Начальное положение печенья
cookie_rect = cookie.get_rect(center = screen.get_rect().center)

# Угол вращения лучей
angle = 0

# Скорость вращения
rotation_speed = 0.05

# Создание тени
shadow = pygame.Surface((119, 119), pygame.SRCALPHA)  # Увеличиваем размер тени
pygame.draw.circle(shadow, (0, 0, 0, 50), (60, 60), 52)  # Рисуем круг по центру нового изображения
# Создание затемненной шапки
header = pygame.Surface((400, 150))  # Установка размера шапки
header.set_alpha(100)  # Установка прозрачности (0 - полностью прозрачный, 255 - полностью непрозрачный)
header.fill((0, 0, 0))  # Заполнение шапки черным цветом
def handle_events():
    global clicks, cookie, cookie_rect, streak, last_click, current_streak, target_streak, idle_time, clicked_cookies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cookie_rect.collidepoint(event.pos):
                current_time = pygame.time.get_ticks()
                if current_time - last_click < 500:
                    streak += 1
                    if streak > 5:  # Check if streak is greater than 5
                        streak = 5  # Set streak to 5
                else:
                    streak = 1
                last_click = current_time  # Update last_click when a click event occurs
                clicks += streak
                current_streak = streak
                target_streak = streak
                create_cookie()
                # Уменьшение печенья
                cookie = small_cookie
                cookie_rect = cookie.get_rect(center = screen.get_rect().center)
                idle_time = 0  # Reset idle_time when the cookie is clicked
                # Create a new cookie with the number of clicks and add it to the list
                clicked_cookie = font.render(str(streak), True, (0, 0, 0))

                # Generate a random position within the cookie's area
                random_x = random.randint(cookie_rect.left, cookie_rect.right - clicked_cookie.get_width())
                random_y = random.randint(cookie_rect.top, cookie_rect.bottom - clicked_cookie.get_height())
                clicked_cookie_rect = clicked_cookie.get_rect(topleft = (random_x, random_y))
                clicked_cookies.append((clicked_cookie, clicked_cookie_rect))
        # Возвращение печенья к исходному размеру после нажатия
        if event.type == pygame.MOUSEBUTTONUP:
            cookie = pygame.transform.scale(cookie, (100, 100))
            cookie_rect = cookie.get_rect(center = screen.get_rect().center)
    idle_time += 1  # Increase idle_time by 1 every frame


def create_cookie():
    new_cookie = pygame.transform.scale(cookie, (50, 50))  # Создаем меньшую версию печенья
    rotated_cookie = pygame.transform.rotate(new_cookie, random.randint(0, 360))  # Rotate the cookie by a random angle
    rect = rotated_cookie.get_rect(center = (random.randint(0, 400), 0))  # Помещаем печенье в случайное место сверху экрана
    falling_cookies.append((rotated_cookie, rect))  # Добавляем печенье и его Rect в список падающих печенек


    async def on_like(event: LikeEvent):
        print(f"@{event.user.unique_id} liked the stream!")


async def simulate_click(event: LikeEvent):
   global clicks, cookie, cookie_rect, streak, last_click, current_streak, target_streak, idle_time, clicked_cookies
   current_time = pygame.time.get_ticks()
   if current_time - last_click < 500:
       streak += 1
       if streak > 5: # Check if streak is greater than 5
           streak = 5 # Set streak to 5
   else:
       streak = 1
   last_click = current_time # Update last_click when a click event occurs
   clicks += streak
   current_streak = streak
   target_streak = streak
   create_cookie()
   # Уменьшение печенья
   cookie = small_cookie
   cookie_rect = cookie.get_rect(center = screen.get_rect().center)
   idle_time = 0 # Reset idle_time when the cookie is clicked
   # Create a new cookie with the number of clicks and add it to the list
   clicked_cookie = font.render(str(streak), True, (0, 0, 0))

   # Generate a random position within the cookie's area
   random_x = random.randint(cookie_rect.left, cookie_rect.right - clicked_cookie.get_width())
   random_y = random.randint(cookie_rect.top, cookie_rect.bottom - clicked_cookie.get_height())
   clicked_cookie_rect = clicked_cookie.get_rect(topleft = (random_x, random_y))
   clicked_cookies.append((clicked_cookie, clicked_cookie_rect))

def update_cookies():
    for i, (cookie, rect) in enumerate(falling_cookies):
        rect.move_ip(0, 1)
        if not background.get_rect().colliderect(rect):
            del falling_cookies[i]
        else:
            falling_cookies[i] = (cookie, rect)
def draw_cookies():
    for cookie, rect in falling_cookies:
        background.blit(cookie, rect)

def draw_button():
    global fade_state
    button_color = (255, 255, 255)
    button_text = font.render("Tap!", True, button_color)  # Create the button text with the new color
    button_rect = button_text.get_rect(center = (200, 700))  # Position the button at the bottom of the screen
    button_text.set_alpha(fade_state)  # Set the alpha value of the button text
    screen.blit(button_text, button_rect)  # Draw the button on the screen
def draw_screen():
   global angle, current_streak, last_click, fade_state, fade_speed, idle_time, clicked_cookies
   # Draw the background onto the background surface
   background.fill((102, 138, 255))

   # Draw the sun rays
   rotated_sun_rays = pygame.transform.rotate(sun_rays, angle)
   sun_rays_rect = rotated_sun_rays.get_rect(center = cookie_rect.center)
   background.blit(rotated_sun_rays, sun_rays_rect)

   # Draw the cookies onto the background surface
   update_cookies()
   draw_cookies()

   # Draw the rest of the elements onto the main screen surface
   screen.blit(background, (0, 0))
   screen.blit(header, (0, 0))
   text = font.render(str(clicks) + ": Cookies!", True, (255, 255, 255))
   screen.blit(text, (100, 50))
   streak_text = font.render("x" + str(current_streak), True, (255, 255, 255))
   screen.blit(streak_text, (100, 80))
   if cookie.get_size() == (100, 100):
    shadow_rect = shadow.get_rect(center=cookie_rect.center)
    screen.blit(shadow, shadow_rect)
   screen.blit(cookie, cookie_rect)
   if pygame.time.get_ticks() - last_click > 5000:
    draw_button()
   for i, (clicked_cookie, clicked_cookie_rect) in enumerate(clicked_cookies):
    clicked_cookie_rect.move_ip(0, -1)
    screen.blit(clicked_cookie, clicked_cookie_rect)
    if clicked_cookie_rect.top < 0:
        del clicked_cookies[i]
   fade_state = (fade_state + fade_speed) % 256
   angle = (angle + rotation_speed) % 360
   pygame.display.flip()
while True:
    handle_events()
    draw_screen()