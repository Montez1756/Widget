import os, win32com.client, pythoncom
from win32com.client import WithEvents
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPainterPath, QPixmap, QPainter

class Events():
    def OnPlayerPlayingTrackChanged(self, newTrack):
        print("self ello")
class Music(QObject):
    def __init__(self, window):
        super().__init__(None)

        pythoncom.CoInitialize()

        self.events = win32com.client.DispatchWithEvents("iTunes.Application", Events)
        self.events.track_signal.connect(lambda: print("hello"))
        self.player_state = self.get_player_state()
        self.current_artist = ""
        self.current_song = ""
        self.thumbnail_path = "current_artwork.jpg"
        self.get_track_info()

        timer = QTimer(self)
        timer.timeout.connect(lambda: pythoncom.PumpWaitingMessages())
        timer.start(50)

    def get_track_info(self):
        try:
            track = self.events.CurrentTrack
            print(track.Duration)
            # print(dir(track))
            if track is not None :
                self.current_artist = track.Artist
                self.current_song = track.Name
                if track.Artwork.Count > 0:
                    artwork = track.Artwork.Item(1)
                    artwork.SaveArtworkToFile(os.path.abspath(self.thumbnail_path))
        except Exception as e:
            print("Error accessingn iTunes Com: ", e)
    def get_player_state(self):
        return self.events.PlayerState
    def toggle(self):
        state = self.get_player_state()
        print(state)
        if state == 1:
            self.events.pause()
        else:
            self.events.play()
    def nextTrack(self):
        self.events.NextTrack()
    def prevTrack(self):
        self.events.PreviousTrack()
    def get_thumbnail(self) -> QPixmap:
        return self.rounded_image(self.thumbnail_path, 20)
    def OnPlayerPlay(self, track):
        print("Playing:", track.Name, "-", track.Artist)

    def OnPlayerStop(self, track):
        print("Stopped:", track.Name)
    def OnPlayerPlayingTrackChanged(self, newTrack):
        print("Now playing:", newTrack.Name, "-", newTrack.Artist)
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