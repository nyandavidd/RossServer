import os.path
from typing import Any, Callable, Optional

from MessagersInterfaces import Listener, Notifier
from RossServer import RossEvent, RossState
import pygame


class SoundEncoder(Listener[RossEvent]):
    def __init__(self, directory="./sounds/", file_name_fun: Optional[Callable[[RossEvent], str]] = None):
        self._directory = directory
        self._get_file_name = file_name_fun
        self._mx = pygame.mixer
        self._mx.init()
        self._lives: dict[int, bool] = dict()

    def get_file_name(self, event: RossEvent) -> str:
        if self._get_file_name:
            return self._get_file_name(event)
        else:
            return f"{event.camera_id}.mp3"

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        if (message.state == RossState.PGM or message.state == RossState.BOTH) and \
                self._lives.get(message.camera_id) is not True:
            filename = self._directory + self.get_file_name(message)
            if os.path.isfile(filename):
                self._mx.music.stop()
                self._mx.music.load(self._directory + self.get_file_name(message))
                self._mx.music.play()

        if message.state == RossState.PGM or message.state == RossState.BOTH:
            self._lives[message.camera_id] = True
        else:
            self._lives[message.camera_id] = False