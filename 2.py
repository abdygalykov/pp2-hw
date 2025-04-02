import pygame
import os
from pygame.locals import *

pygame.init()
pygame.mixer.init()

MUSIC_FOLDER = "music"
tracks = [os.path.join(MUSIC_FOLDER, file) for file in os.listdir(MUSIC_FOLDER) if file.endswith(".mp3")]
current_track = 0

def play_music():
    pygame.mixer.music.load(tracks[current_track])
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global current_track
    current_track = (current_track + 1) % len(tracks)
    play_music()

def previous_track():
    global current_track
    current_track = (current_track - 1) % len(tracks)
    play_music()

if tracks:
    play_music()

def event_loop():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print(f"Key pressed: {event.key}")
                if event.key == K_SPACE:
                    if pygame.mixer.music.get_busy():
                        stop_music()
                    else:
                        play_music()
                elif event.key == 1073741903:
                    next_track()
                elif event.key == 1073741904:
                    previous_track()
                elif event.key == K_q and (pygame.key.get_mods() & KMOD_META):  # CMD + Q для выхода
                    return

event_loop()
pygame.quit()