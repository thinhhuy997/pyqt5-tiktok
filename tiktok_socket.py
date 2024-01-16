from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSlot, pyqtSignal, QThreadPool
import requests
from PyQt5.QtCore import QObject, pyqtSignal
import time
from proxy_chrome_driver import get_chromedriver
from auto_action import auto_like, auto_haha, auto_play_video, auto_comment_on_livetream, auto_follow_on_livestream
import traceback
import shutil
from http.cookies import SimpleCookie
from selenium.common.exceptions import NoSuchElementException

from traodoisub import Traodoisub



class WorkerSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)

    # new
    profile_status = pyqtSignal(int)
    # cookie
    cookie = pyqtSignal(str)

class TiktokSocketWorker(QRunnable):
    def __init__(self, live_id: str) -> None:
        self.live_id = live_id
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):

        # Instantiate the client with the user's username
        client: TikTokLiveClient = TikTokLiveClient(unique_id=self.live_id)


        # Define how you want to handle specific events via decorator
        @client.on("connect")
        async def on_connect(_: ConnectEvent):
            self.signals.result.connect.emit(f"Connected to Room ID: {client.room_id}")


        client.run()




        