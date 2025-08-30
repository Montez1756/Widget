import os, win32com.client, pythoncom
from win32com.client import WithEvents
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPainterPath, QPixmap, QPainter

class Music(QObject):
    def __init__(self, window):
        super().__init__(None)

        self.window = window

        self.itunes = win32com.client.Dispatch("iTunes.Application")
        self.track = None
        self.current_artist = ""
        self.current_song = ""
        self.thumbnail_path = "current_artwork.jpg"
        self.player_state = self.get_player_state()
        self.initTrack()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkNewTrack)
        self.timer.start(500)

    #"""
    # 
    # Music Class GUI Events
    # 
    # 
    # """

    def rounded_image(self, image_path : str, radius : int) -> QPixmap:
        img = QImage(image_path)
        size = img.size()
        
        # Create a transparent pixmap
        rounded = QPixmap(size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded rect path
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), radius, radius)

        painter.setClipPath(path)
        painter.drawImage(0, 0, img)
        painter.end()

        return rounded
    
    #"""
    #
    # Music Class Itunes Events
    #
    # """
    def initTrack(self):
        self.track = self.get_current_track()
        self.current_artist = self.get_current_artist() or ""
        self.current_song = self.get_current_song_name() or ""
        artwork = self.get_current_thumbnail()

        if artwork:
            artwork.SaveArtworkToFile(os.path.abspath(self.thumbnail_path))
    def get_current_track(self):
        return self.itunes.CurrentTrack
    def get_current_artist(self):
        return self.track.Artist
    def get_current_song_name(self):
        return self.track.Name
    def get_player_state(self):
        return self.itunes.PlayerState
    def get_current_thumbnail(self):
        return self.track.Artwork.Item(1) if self.track.Artwork.Count > 0 else None
    def toggle(self):
        state = self.get_player_state()
        if state == 1:
            self.itunes.Pause()
        else:
            self.itunes.Play()
    def nextTrack(self):
        self.itunes.NextTrack()
        self.reload()
    def prevTrack(self):
        self.itunes.PreviousTrack()
        self.reload()
    def get_thumbnail(self) -> QPixmap:
        return self.rounded_image(self.thumbnail_path, 20)
    
    def checkNewTrack(self):
        self.track = self.itunes.CurrentTrack
        new_song = self.get_current_song_name()
        if new_song != self.current_song:
            self.reload()
    def reload(self):
        self.initTrack()
        self.window.reload()