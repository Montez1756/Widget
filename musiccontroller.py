from PyQt5.QtCore import Qt, QRectF, QPoint, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStyle
from PyQt5.QtGui import QImage, QRegion, QPainterPath, QPixmap, QPainter, QIcon
from music import Music
class MusicControl(QWidget):
    def __init__(self, music : Music = None, parent : QWidget = None):
        super().__init__(parent)
        self._parent = parent
        self.music = music
        self.setStyleSheet("background-color:#444; border-radius:20px;")

        layout = QHBoxLayout(self)
        self.setLayout(layout)
        
        style = QApplication.style()

        play_icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        pause_icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        forward_icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward)
        prev_icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        
        self.prev = QPushButton(prev_icon, "", self)
        self.forward = QPushButton(forward_icon, "", self)
        self.play = QPushButton(play_icon, "", self)
        self.pause = QPushButton(pause_icon, "", self)

        self.pause.clicked.connect(self.toggle)
        self.play.clicked.connect(self.toggle)
        self.prev.clicked.connect(self.music.prevTrack)
        self.forward.clicked.connect(self.music.nextTrack)
        
        layout.addWidget(self.prev)
        layout.addWidget(self.play)
        layout.addWidget(self.pause)
        layout.addWidget(self.forward)

        if self.music.get_player_state() == 1:
            self.play.setVisible(False)
        else:
            self.pause.setVisible(False)
        
    def toggle(self):
        self.music.toggle()
        if self.music.get_player_state() == 1:
            self.play.setVisible(False)
            self.pause.setVisible(True)
        else:
            self.play.setVisible(True)
            self.pause.setVisible(False)
        





