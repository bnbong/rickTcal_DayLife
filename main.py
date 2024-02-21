# TODO: 사도 설명 위젯 수정, 사도 idle 애니메이션 개선
# --------------------------------------------------------------------------
# 릭트컬 - 데이라이프 데스크톱 앱의 메인 스크립트입니다.
#
# GLOBAL VARs
# - occupied_positions : 사도의 위치를 계산하는 데 사용되는 글로벌 리스트입니다.
# - players : 사도 위젯 플레이어를 관리하는 데 사용되는 글로벌 리스트입니다.
# - global_bolddagu_sound : 볼따구 당길 때 재생되는 QSoundEffect 글로벌 객체입니다.
# - global_bolddagu_ouch_sound : 볼따구 놓을 때 재생되는 QSoundEffect 글로벌 객체입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os
import random
import sys
import json
import glob

from PyQt6.QtGui import QIcon, QMovie, QFontDatabase, QFont
from PyQt6.QtCore import Qt, QSize, QTimer, QUrl, QPoint, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

from sado_info import SadoDescriptionDialog

# GLOBAL VARs
occupied_positions = []
players = []
global_bolddagu_sound = QSoundEffect()
global_bolddagu_ouch_sound = QSoundEffect()


def initialize_global_resources(application_path):
    sound_path = application_path + "/sounds/"
    global_bolddagu_sound.setSource(QUrl.fromLocalFile(sound_path + "bolddagu.wav"))
    global_bolddagu_ouch_sound.setSource(QUrl.fromLocalFile(sound_path + "ouch.wav"))


class rickTcal(QWidget):
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
        self.timer = QTimer(self)
        self.timer.setInterval(2000)  # 2초 후에 시그널 발생
        self.timer.timeout.connect(self.returnToOriginalGif)

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
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
        if (BOLDDAGU_WIDTH) < click_x < (half_width) and (
            half_height - BOLDDAGU_HEIGHT
        ) < click_y < half_height:
            if event.button() == Qt.MouseButton.LeftButton:
                self.clicked_on_bolddaggu = True
                self.movie.stop()
                self.movie.setFileName(self.clicked_gif_path)
                self.movie.start()

                global_bolddagu_sound.play()

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

            global_bolddagu_ouch_sound.play()

            # 5초 뒤에 원래의 GIF로 되돌아가기 위해 타이머를 시작합니다.
            self.timer.start()

    def changeStandingMotion(self):
        # TODO: 로직 추가
        pass

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
        self.closed.emit()  # 위젯이 닫힐 때 closed 신호 발생
        super().closeEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sado_data = sado_data

        self.layout = QVBoxLayout(self)
        self.initUI()

    def initUI(self):
        # 사도들의 설명 위젯 추가
        sado_info_icon = application_path + "/images/static/sado_icon.png"

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.sadoIconButton = QPushButton(QIcon(sado_info_icon), "")
        self.sadoIconButton.clicked.connect(self.showSadoDescription)

        # 사도들의 설명 위젯은 투명한 버튼으로 화면에 표시.
        self.sadoIconButton.setStyleSheet(
            "background-color: transparent; border: none;"
        )

        self.adjustWindowSize()

        self.layout.addWidget(self.sadoIconButton)

    def showSadoDescription(self):
        # 사도 설명 대화 상자 표시
        current_index = 0
        dialog = SadoDescriptionDialog(self.sado_data, current_index, self, title_font, description_font)
        dialog.addCurrentSado.connect(self.addSado)
        dialog.exec()

    def addSado(self, sado_name):
        # 사도를 화면에 추가하는 로직
        sado_info = self.sado_data.get(sado_name)
        if not sado_info:
            print(f"{sado_name} 정보를 찾을 수 없습니다.")
            return

        player = rickTcal(
            application_path=application_path,
            sado_name=sado_name,
            bolddagu_x=sado_info["bolddagu_x"],
            bolddagu_y=sado_info["bolddagu_y"],
        )
        player.closed.connect(lambda: self.removePlayer(player))
        player.show()
        players.append(player)

    def removePlayer(self, player):
        player.deleteLater()  # QWidget의 deleteLater 메서드를 사용하여 리소스 해제
        players.remove(player)  # players 리스트에서 해당 인스턴스 제거

    def adjustWindowSize(self):
        iconSize = QSize(50, 50)  # 아이콘 크기 설정
        self.sadoIconButton.setIconSize(iconSize)

        screen = QApplication.primaryScreen().geometry()
        rightMargin = 30  # 우측 마진
        bottomMargin = 70  # 하단 마진

        buttonWidth = iconSize.width()
        buttonHeight = iconSize.height()

        # 버튼 위치 계산: 화면의 우측 하단
        x = screen.width() - buttonWidth - rightMargin
        y = screen.height() - buttonHeight - bottomMargin

        self.setGeometry(x, y, 10, 10)


if __name__ == "__main__":
    """캐릭터(사도) 정보는 sado.json 파일에 다음과 같은 형식으로 저장됩니다:

    "<사도 이름>" : {
        "bolddagu_x": int  # 볼따구의 x 범위 입니다.
        "bolddagu_y": int  # 볼따구의 y 범위 입니다.
        "description": str # 사도에 대한 설명 입니다.
    }
    """
    app = QApplication(sys.argv)

    if getattr(sys, "frozen", False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # 커스텀 폰트 적용
    titleFontPath = application_path + "/fonts/Katuri.ttf"
    descriptionFontPath = application_path + "/fonts/ONE MOBILE POP.ttf"

    title_font = QFont('Arial', 12)
    description_font = QFont('Arial', 10)
    description_font.setBold(False)

    if not os.path.exists(titleFontPath) or not os.path.exists(descriptionFontPath):
        print("Font file not found.")
    else:
        titleFontId = QFontDatabase.addApplicationFont(titleFontPath)
        descriptionFontId = QFontDatabase.addApplicationFont(descriptionFontPath)
        if titleFontId == -1 or descriptionFontId == -1:
            print("Failed to load font.")
        else:
            titleFontFamily = QFontDatabase.applicationFontFamilies(titleFontId)[0]
            descriptionFontFamily = QFontDatabase.applicationFontFamilies(descriptionFontId)[0]
            title_font = QFont(titleFontFamily, 12)
            description_font = QFont(descriptionFontFamily, 10)

    # 사도 데이터 로드
    json_path = os.path.join(application_path, "sado_test.json")
    with open(json_path, "r", encoding="utf-8") as file:
        sado_data = json.load(file)

    # 글로벌 참조 로드
    initialize_global_resources(application_path)

    # 캐릭터(사도) 설명 위젯 추가
    mainWindow = MainWindow()
    mainWindow.show()

    # 캐릭터(사도) 로드
    # ~ Version 1.0 초기 캐릭터(사도) 5종 : 버터, 에르핀, 비비, 림, 실피르
    for sado_name, sado_info in sado_data.items():
        player = rickTcal(
            application_path=application_path,
            sado_name=sado_name,
            bolddagu_x=sado_info["bolddagu_x"],
            bolddagu_y=sado_info["bolddagu_y"],
        )
        player.show()
        players.append(player)

    sys.exit(app.exec())
