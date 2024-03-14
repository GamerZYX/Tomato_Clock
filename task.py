# tasks.py
from celery import shared_task
import pygame  # Import pygame for music playback
import time

def play_music(file_path, play_time=1500):  # play_time in seconds, 1500s = 25min
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    
    # Wait for the specified play time (25 minutes here)
    time.sleep(play_time)
    
    # Stop the music after 25 minutes
    pygame.mixer.music.stop()

@shared_task
def play_music_async(file_path, play_time=1500):
    play_music(file_path, play_time)
