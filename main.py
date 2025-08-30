import os, sys, win32com.client
from PyQt5.QtCore import Qt, QRectF, QPoint, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QRegion, QPainterPath, QPixmap, QPainter, QFont, QFontMetrics
from music import Music
from musiccontroller import MusicControl

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._width = 350
        self._height = 250

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:black;")
        self.setGeometry(0,0, self._width, self._height)
        self.setFixedWidth(5)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.music = Music(self)


        self.track = QLabel(self)
        self.track.setMinimumWidth(self._width)
        self.track.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.track.setText(self.music.current_song)
        self.track.setWordWrap(True)
        self.track.setFont(QFont("Arial", 10))
        self.track.setStyleSheet("color:white; font-weight:bold;")
        self.track.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.track, 1, alignment=Qt.AlignmentFlag.AlignHCenter)


        pixmap = self.music.get_thumbnail().scaled(int(self._width / 1.7), int(self._height / 1.7), transformMode=Qt.SmoothTransformation)
        
        if not pixmap.isNull():
            self.thumbnail = QLabel(self)
            self.thumbnail.setPixmap(pixmap)
            self.thumbnail.setStyleSheet("border-radius:20px;")
            layout.addWidget(self.thumbnail, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        music_controller = MusicControl(self.music, self)
        layout.addWidget(music_controller, 1, Qt.AlignmentFlag.AlignHCenter)
        
        
        self.show()
    def enterEvent(self, event):
        self.setFixedWidth(self._width)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setFixedWidth(5)
        super().leaveEvent(event)
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
    def resizeEvent(self, a0):
        self.roundCorner(20)
        super().resizeEvent(a0)
    def reload(self):
        self.track.setText(self.music.current_song)
        pixmap = self.music.get_thumbnail().scaled(int(self._width / 1.7), int(self._height / 1.7), transformMode=Qt.SmoothTransformation)
        self.thumbnail.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())
