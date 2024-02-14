# TODO: 림 이미지 수정(배경 색 투명으로 수정), 코드 개선
# --------------------------------------------------------------------------
# PyQt 메인 스크립트입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QMovie


class rickTcal(QWidget):
    def __init__(self, sado_info):
        super().__init__()

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__)) + "/images/static/"

        # 캐릭터(사도) 설정
        sado_name = sado_info[0]
        self.sado_bolddagu_width = sado_info[1]
        self.sado_bolddagu_height = sado_info[2]

        self.clicked_on_bolddaggu = False
        self.original_gif_path = os.path.join(application_path, f'{sado_name}/default/{sado_name}.gif')
        self.clicked_gif_path = os.path.join(application_path, f'{sado_name}/moving/{sado_name}bolddagu.gif')
        self.bolddagu_after_gif_path = os.path.join(application_path, f'{sado_name}/moving/{sado_name}bolddaguafter.gif')

        self.initUI()

        # 캐릭터(사도)의 볼을 잡아당기면 2초 동안 캐릭터의 반응 애니메이션이 나타나고 다시 원래의 애니메이션으로 돌아옴.
        self.timer = QTimer(self)
        self.timer.setInterval(2000)  # 2초 후에 시그널 발생
        self.timer.timeout.connect(self.returnToOriginalGif)

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.label = QLabel(self)
        self.movie = QMovie(self.original_gif_path)
        self.label.setMovie(self.movie)

        self.movie.setScaledSize(QSize(200, 200))
        self.movie.start()

        self.adjustWindowSize()

    def returnToOriginalGif(self):
            self.movie.stop()
            self.movie.setFileName(self.original_gif_path)
            self.movie.start()
            self.timer.stop()  # 타이머 정지

    def mousePressEvent(self, event):
        BOLDDAGU_WIDTH = self.sado_bolddagu_width
        BOLDDAGU_HEIGHT = self.sado_bolddagu_height

        half_width = self.width() / 2
        half_height = self.height() / 2

        click_x = event.position().x()
        click_y = event.position().y()

        # 볼이 당겨지는 애니메이션은 캐릭터(사도)의 볼따구 부분 근처에서 발생하도록 함.
        if (half_width - BOLDDAGU_WIDTH) < click_x < (half_width + BOLDDAGU_WIDTH) \
                and (half_height - BOLDDAGU_HEIGHT) < click_y < half_height:
            if event.button() == Qt.MouseButton.LeftButton:
                self.clicked_on_bolddaggu = True
                self.movie.stop()
                self.movie.setFileName(self.clicked_gif_path)
                self.movie.start()

        # 사도를 우클릭하면 삭제
        if event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseReleaseEvent(self, event):
        if self.clicked_on_bolddaggu:
            self.clicked_on_bolddaggu = False
            # 마우스 클릭을 해제하면 놀란 표정의 GIF가 2초동안 재생
            self.movie.stop()
            self.movie.setFileName(self.bolddagu_after_gif_path)
            self.movie.start()

            # 5초 뒤에 원래의 GIF로 되돌아가기 위해 타이머를 시작합니다.
            self.timer.start()

    def adjustWindowSize(self):
        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.setFixedSize(200, 200)
        x = rect.width() - self.width()
        y = rect.height() - self.height() - 30
        self.move(x, y)


if __name__ == '__main__':
    """캐릭터(사도) 정보는 sado_name 리스트에 다음과 같은 형식으로 저장됩니다:
    
    ("캐릭터(사도)이름", "볼따구 x 범위(픽셀)", "볼따구 y 범위(픽셀)")
    """
    import random

    sado_name = [('rim', 33, 13), ('bibi', 50, 40)]

    app = QApplication(sys.argv)
    player = rickTcal(sado_info=random.choice(sado_name))
    player.show()
    sys.exit(app.exec())
