import os

from pygame import mixer

class MusicHandler:
    GAME_MUSIC =  os.path.join("assets", 'Music/2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3')
    GAME_OVER_SOUND = os.path.join("assets",'Music/game-over-38511.mp3')
    GAME_WIN_SOUND= os.path.join("assets", 'Music/8-bit-video-game-win-level-sound-version-1-145827.mp3')
    def __init__(self):
        mixer.init()
        mixer.music.load(self.GAME_MUSIC)
        mixer.music.play(-1)
        self.__game_over_sound_played = False
        self.__game_win_sound_played=False

    def play_game_over_sound(self):
        if not self.__game_over_sound_played:
            mixer.music.stop()
            mixer.music.load(self.GAME_OVER_SOUND)
            mixer.music.play()
            self.__game_over_sound_played = True

    def play_win_music(self):
        if not self.__game_win_sound_played:
            mixer.music.stop()
            mixer.music.load(self.GAME_WIN_SOUND)
            mixer.music.play()
            self.__game_win_sound_played = True

