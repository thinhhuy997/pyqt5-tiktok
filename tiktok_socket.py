from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, DisconnectEvent
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
import random



class WorkerSignals(QObject):
    con_status = pyqtSignal(int)
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)
    finished = pyqtSignal()

class TiktokSocketWorker(QRunnable):
    def __init__(self, live_id: str) -> None:
        super(TiktokSocketWorker, self).__init__()
        self.is_running = True
        self.live_id = live_id
        self.signals = WorkerSignals()

        self.client: TikTokLiveClient = TikTokLiveClient(unique_id=self.live_id)
    @pyqtSlot()
    def run(self):
        try:
            # Instantiate the client with the user's username
            # client: TikTokLiveClient = TikTokLiveClient(unique_id=self.live_id)

            self.signals.result.emit(f"Đang kết nối tới Livestream của '{self.live_id}'")

            # Define how you want to handle specific events via decorator
            @self.client.on("connect")
            async def on_connect(_: ConnectEvent):
                self.signals.con_status.emit(1)
                self.signals.result.emit(f"Đã kết nối tới Livestream với ID: {self.client.room_id}")

            @self.client.on("disconnect")
            async def on_disconnect(event: DisconnectEvent):
                self.signals.con_status.emit(0)
                self.signals.result.emit(f"Livestream của '{self.live_id}' đã bị ngắt kết nối")

            self.client.run()
        except Exception as err:
            self.signals.con_status.emit(0)
            self.signals.result.emit(f'Lỗi: Kết nối tới Livestream của "{self.live_id}" không thành công!')
            tb_info = traceback.format_exc()
            self.signals.error.emit((type(err), err.args, tb_info))
        finally:
            self.signals.result.emit(f'Đã chạy vào finally - {random.random()}')
            self.signals.finished.emit()
    
    def stop(self):
        self.client.stop()
        self.signals.result.emit(f'Đã ngắt kết nối')


        