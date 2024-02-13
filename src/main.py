import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QMovie, QScreen, QPainter


class rickTcal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        gif_path = "static/silfirdance.gif"

        self.label = QLabel(self)
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)

        self.movie.setScaledSize(QSize(200, 200))

        self.movie.start()

        self.adjustWindowSize()

    def paintEvent(self, event):
        painter = QPainter(self)
        # 볼따구 늘리는 Event 로직 추가 예정


    def adjustWindowSize(self):
        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.setFixedSize(200, 200)
        x = rect.width() - self.width()
        y = rect.height() - self.height()
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = rickTcal()
    player.show()
    sys.exit(app.exec())
