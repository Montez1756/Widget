import os, sys, win32com.client
from PyQt5.QtCore import Qt, QRectF, QPoint, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QRegion, QPainterPath, QPixmap, QPainter, QFont
from music import Music
from musiccontroller import MusicControl

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._width = 300
        self._height = 250

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0,0, self._width, self._height)

        self.setStyleSheet("background-color:black;")

        self.roundCorner(20)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.music = Music(self)

        track_name = self.music.current_song

        self.track = QLabel(track_name, self)
        font = QFont("Ariel", 10)
        self.track.setFont(font)
        self.track.setWordWrap(True)
        self.track.setStyleSheet("color:white; font-weight:bold;")
        
        self.track.setContentsMargins(10,10,10,10)
        layout.addWidget(self.track, alignment=Qt.AlignmentFlag.AlignHCenter)


        self.pixmap = self.music.get_thumbnail().scaled(int(self._width / 1.7), int(self._height / 1.7), transformMode=Qt.SmoothTransformation)
        
        if not self.pixmap.isNull():
            self.thumbnail = QLabel(self)
            self.thumbnail.setPixmap(self.pixmap)
            self.thumbnail.setStyleSheet("border-radius:20px;")
            layout.addWidget(self.thumbnail, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        music_controller = MusicControl(self.music, self)
        layout.addWidget(music_controller, 1, Qt.AlignmentFlag.AlignHCenter)
        self.show()
    def new_track(self):
        self.music.get_track_info()
        self.pixmap = self.music.get_thumbnail().scaled(int(self._width / 1.7), int(self._height / 1.7), transformMode=Qt.SmoothTransformation)
        track_name = self.music.current_song
        self.track.setText(track_name)
    def roundCorner(self, radius):
        r = self.rect()
        path = QPainterPath()

        # Start at top-left
        path.moveTo(r.topLeft())

        # Top edge
        path.lineTo(r.topRight())

        # Right edge, stop radius above bottom
        path.lineTo(r.bottomRight().x(), r.bottomRight().y() - radius)

        # Curve around bottom-right corner
        ctrl = r.bottomRight()  # control point (corner itself)
        end = r.bottomRight() + QPoint(-radius, 0)  # end point to the left
        path.quadTo(ctrl, end)

        # Bottom edge to bottom-left
        path.lineTo(r.bottomLeft())

        # Left edge to top-left
        path.lineTo(r.topLeft())

        path.closeSubpath()

        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)


if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())
