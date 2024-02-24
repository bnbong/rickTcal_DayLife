# --------------------------------------------------------------------------
# 사도들의 애니메이션 정상 재생 여부 확인, 볼따구 픽셀 범위 위치를 찾는 테스트 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os
import random
import sys
import json
import glob

from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QSize, QTimer, QPoint, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel


# GLOBAL VARs
occupied_positions = []
players = []


class rickTcal_test(QWidget):
    """
    캐릭터(사도) 위젯 클래스입니다.
    볼따구를 잡아당기면 잡고 있는 동안 볼따구 애니메이션이 재생되고 볼따구를 놓으면 놀란 표정의 애니메이션이 재생됩니다.

    ---

    self.original_gif_path : 캐릭터(사도)의 기본 GIF 파일 경로입니다.
    self.standing_gifs : 캐릭터(사도)의 idle 애니메이션 GIF 파일들의 경로입니다.
    self.clicked_gif_path : 캐릭터(사도)의 볼따구 애니메이션 GIF 파일 경로입니다.
    self.bolddagu_after_gif_path : 캐릭터(사도)의 볼따구 놓았을 때 애니메이션 GIF 파일 경로입니다.

    self.bolddagu_timer : 캐릭터(사도)의 볼따구 애니메이션을 제어하는 QTimer 객체입니다.
    self.standing_timer : 캐릭터(사도)의 idle 애니메이션을 제어하는 QTimer 객체입니다.

    self.clicked_on_bolddaggu : 캐릭터(사도)의 볼따구 애니메이션을 제어하는 Boolean 변수입니다.
    self.sado_bolddagu_width : 캐릭터(사도)의 볼따구 x 좌표입니다. (사도 JSON 데이터 파일에서 가져옴)
    self.sado_bolddagu_height : 캐릭터(사도)의 볼따구 y 좌표입니다. (사도 JSON 데이터 파일에서 가져옴)
    """

    closed = pyqtSignal()  # 위젯이 닫힐 때 발생할 신호

    def __init__(self, application_path, sado_name, bolddagu_x, bolddagu_y):
        super().__init__()

        image_path = application_path + "/images/static/"

        sado_name = sado_name
        self.sado_bolddagu_width = bolddagu_x
        self.sado_bolddagu_height = bolddagu_y

        self.clicked_on_bolddaggu = False

        default_gif_path = os.path.join(image_path, f"{sado_name}/default/")
        self.original_gif_path = os.path.join(
            image_path, f"{sado_name}/default/{sado_name}.gif"
        )
        self.standing_gifs = glob.glob(f"{default_gif_path}*.gif")
        self.clicked_gif_path = os.path.join(
            image_path, f"{sado_name}/moving/{sado_name}bolddagu.gif"
        )
        self.bolddagu_after_gif_path = os.path.join(
            image_path, f"{sado_name}/moving/{sado_name}bolddaguafter.gif"
        )

        self.initUI()

        # 캐릭터(사도)의 볼을 잡아당기면 2초 동안 캐릭터의 반응 애니메이션이 나타나고 다시 원래의 애니메이션으로 돌아옴.
        self.bolddagu_timer = QTimer(self)
        self.bolddagu_timer.setInterval(2000)  # 2초 후에 시그널 발생
        self.bolddagu_timer.timeout.connect(self.returnToOriginalGif)

        # 캐릭터(사도)의 idle 애니메이션은 5초마다 변경
        self.standing_timer = QTimer(self)
        self.standing_timer.setInterval(5000)  # 5초마다
        self.standing_timer.timeout.connect(self.changeStandingMotion)
        self.standing_timer.start()

    def initUI(self):
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )

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
        self.bolddagu_timer.stop()

    def mousePressEvent(self, event):
        print(
            "current bolddagu position data: ",
            self.sado_bolddagu_width,
            self.sado_bolddagu_height,
        )  # for debugging
        BOLDDAGU_WIDTH = self.sado_bolddagu_width
        BOLDDAGU_HEIGHT = self.sado_bolddagu_height

        click_x = event.position().x()
        click_y = event.position().y()

        # 볼이 당겨지는 애니메이션은 캐릭터(사도)의 볼따구 부분 근처에서 발생하도록 함.
        if (BOLDDAGU_WIDTH - 10) < click_x < (BOLDDAGU_WIDTH + 10) and (
            BOLDDAGU_HEIGHT - 10
        ) < click_y < (BOLDDAGU_HEIGHT + 10):
            if event.button() == Qt.MouseButton.LeftButton:
                print("clicked position:", click_x, click_y)  # for debugging
                self.clicked_on_bolddaggu = True
                self.movie.stop()
                self.movie.setFileName(self.clicked_gif_path)
                self.movie.start()

                self.standing_timer.stop()

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

            # 2초 뒤에 원래의 GIF로 되돌아가기 위해 타이머를 시작.
            self.bolddagu_timer.start()
            self.standing_timer.start()

    def changeStandingMotion(self):
        # 현재 재생 중인 GIF가 standing_gifs 리스트에 있다면, 다음 GIF로 변경
        if self.movie.fileName() in self.standing_gifs:
            current_index = self.standing_gifs.index(self.movie.fileName())
            next_index = (current_index + 1) % len(
                self.standing_gifs
            )  # idle 애니메이션 리스트를 순환
            next_gif_path = self.standing_gifs[next_index]
        else:
            next_gif_path = self.standing_gifs[0]
        print(next_gif_path)  # for debugging

        self.movie.stop()
        self.movie.setFileName(next_gif_path)
        self.movie.start()

    def adjustWindowSize(self):
        screen = QApplication.primaryScreen().geometry()
        width = 200  # 사도 위젯의 너비
        height = 200  # 사도 위젯의 높이

        # 바탕화면 바닥에 사도를 배치하기 위한 y 좌표 계산
        y = screen.height() - height - 50  # 작업 표시줄 등을 고려하여 여유 공간을 둠

        while True:
            x = random.randint(0, screen.width() - width)
            new_pos = QPoint(x, y)
            if not any(
                pos.x() == new_pos.x() and pos.y() == new_pos.y()
                for pos in occupied_positions
            ):
                break

        # 새로운 위치를 차지한 것으로 표시
        occupied_positions.append(new_pos)

        self.setFixedSize(width, height)
        self.move(x, y)

    def closeEvent(self, event):
        print("close event!")  # for debugging
        if self.bolddagu_timer.isActive():
            self.bolddagu_timer.stop()
        if self.standing_timer.isActive():
            self.standing_timer.stop()

        self.closed.emit()  # 위젯이 닫힐 때 closed 신호 발생
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    application_path = os.path.dirname(os.path.abspath(__file__))

    # 사도 데이터 로드
    json_path = os.path.join(
        application_path, "sado_test.json"
    )  # 사도 데이터 파일 경로 (테스트)
    with open(json_path, "r", encoding="utf-8") as file:
        sado_data = json.load(file)

    # 캐릭터(사도) 로드
    for sado_name, sado_info in sado_data.items():
        player = rickTcal_test(
            application_path=application_path,
            sado_name=sado_name,
            bolddagu_x=sado_info["bolddagu_x"],
            bolddagu_y=sado_info["bolddagu_y"],
        )
        player.show()
        players.append(player)

    sys.exit(app.exec())
