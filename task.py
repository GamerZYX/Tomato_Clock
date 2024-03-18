# tasks.py
from celery import shared_task
import pygame  # Import pygame for music playback
import time
import sys

# def play_music(file_path, play_time=1500):  # play_time in seconds, 1500s = 25min
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    
#     # Wait for the specified play time (25 minutes here)
#     time.sleep(play_time)
    
#     # Stop the music after 25 minutes
#     pygame.mixer.music.stop()

# def play_break(file_path, play_time=300):  # play_time in seconds, 1500s = 25min
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    
#     # Wait for the specified play time (25 minutes here)
#     time.sleep(play_time)
    
#     # Stop the music after 25 minutes
#     pygame.mixer.music.stop()

# 全局变量，控制音乐是否播放
music_playing = True

def play_music(file_path, play_time):
    global music_playing
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    
    start_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    
    music_playing = True  # 开始播放音乐
    while pygame.time.get_ticks() - start_time < play_time * 1000 and music_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
        clock.tick(30)
    
    pygame.mixer.music.stop()

def play_break(file_path):  
    play_music(file_path, 300)



def stop_music():
    global music_playing
    music_playing = False  # 收到请求时停止音乐
    return "Music will be stopped."


@shared_task
def play_music_async(file_path, play_time=1500):
    play_music(file_path, play_time=1500)
    play_break(file_path)
    stop_music()
