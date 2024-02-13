import os
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QMovie


class rickTcal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__)) + "/images/static/"

        self.original_gif_path = os.path.join(application_path, 'rim.gif')
        self.clicked_gif_path = os.path.join(application_path, 'rimbolddagu.gif')

        self.label = QLabel(self)
        self.movie = QMovie(self.original_gif_path)
        self.label.setMovie(self.movie)

        self.movie.setScaledSize(QSize(200, 200))
        self.movie.start()

        self.adjustWindowSize()

    def mousePressEvent(self, event):
        half_width = self.width() / 2
        half_height = self.height() / 2

        click_x = event.position().x()
        click_y = event.position().y()

        # 볼이 당겨지는 애니메이션은 캐릭터의 볼 부분이 위치하는 2사분면에서 발생하도록 함.
        if click_x < half_width and click_y < half_height:
            if event.button() == Qt.MouseButton.LeftButton:
                self.movie.stop()
                self.movie.setFileName(self.clicked_gif_path)
                self.movie.start()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.movie.stop()
            self.movie.setFileName(self.original_gif_path)
            self.movie.start()

    def adjustWindowSize(self):
        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.setFixedSize(200, 200)
        x = rect.width() - self.width()
        y = rect.height() - self.height() - 30
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = rickTcal()
    player.show()
    sys.exit(app.exec())
