# ignore: N801, N802
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

if getattr(sys, "frozen", False):  # production, development 환경 구분
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


def initialize_global_resources(application_path: str):
    sound_path = application_path + "/sounds/"
    global_bolddagu_sound.setSource(QUrl.fromLocalFile(os.path.join(sound_path + "bolddagu.wav")))
    global_bolddagu_ouch_sound.setSource(QUrl.fromLocalFile(os.path.join(sound_path + "ouch.wav")))


class rickTcal(QWidget):
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

    def __init__(self, sado_name, bolddagu_x, bolddagu_y, idle_len):
        super().__init__()

        print("application path:", application_path)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.label = QLabel(self)
        self.movie = QMovie()

        self.sado_name = sado_name
        self.sado_bolddagu_width = bolddagu_x
        self.sado_bolddagu_height = bolddagu_y
        self.idle_len = int(idle_len)
        self.sado_position = QPoint()

        self.clicked_on_bolddaggu = False

        image_path = os.path.join(application_path, "images", "static", self.sado_name, "default")
        self.original_gif_path = os.path.join(image_path, f"{self.sado_name}0.gif")
        self.standing_gifs = glob.glob(os.path.join(image_path, "*.gif"))
        self.clicked_gif_path = os.path.join(application_path, "images", "static", self.sado_name, "moving",
                                             f"{self.sado_name}bolddagu.gif")
        self.bolddagu_after_gif_path = os.path.join(application_path, "images", "static", self.sado_name, "moving",
                                                    f"{self.sado_name}bolddaguafter.gif")

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
        BOLDDAGU_WIDTH = self.sado_bolddagu_width
        BOLDDAGU_HEIGHT = self.sado_bolddagu_height

        click_x = event.position().x()
        click_y = event.position().y()

        # 볼이 당겨지는 애니메이션은 캐릭터(사도)의 볼따구 부분 근처에서 발생하도록 함.
        if (BOLDDAGU_WIDTH - 10) < click_x < (BOLDDAGU_WIDTH + 10) and (
            BOLDDAGU_HEIGHT - 10
        ) < click_y < (BOLDDAGU_HEIGHT + 10):
            if event.button() == Qt.MouseButton.LeftButton:
                self.clicked_on_bolddaggu = True
                self.movie.stop()
                self.movie.setFileName(self.clicked_gif_path)
                self.movie.start()

                self.standing_timer.stop()

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

            # 2초 뒤에 원래의 GIF로 되돌아가기 위해 타이머를 시작.
            self.bolddagu_timer.start()
            self.standing_timer.start()

    def changeStandingMotion(self):
        next_gif_path = random.choice(self.standing_gifs)

        self.movie.stop()
        self.movie.setFileName(next_gif_path)
        self.movie.start()

    def adjustWindowSize(self):
        screen = QApplication.primaryScreen().geometry()
        width = 200  # 사도 위젯의 너비
        height = 200  # 사도 위젯의 높이

        y = screen.height() - height - 50  # 작업 표시줄 등을 고려하여 여유 공간을 둠
        max_attempts = 100  # 겹치지 않는 위치를 찾기 위한 최대 시도 횟수

        for _ in range(max_attempts):
            x = random.randint(0, screen.width() - width)
            new_pos = QPoint(x, y)

            # 겹치는지 확인
            overlapping = any(
                new_pos.x() < pos.x() + width and new_pos.x() + width > pos.x()
                for pos in occupied_positions
            )

            if not overlapping:
                print("finding position attempt:", _ + 1)  # for debugging
                self.sado_position = new_pos
                occupied_positions.append(self.sado_position)
                self.setFixedSize(width, height)
                self.move(self.sado_position)
                break
        else:
            # 최대 시도 횟수를 초과하여 겹치지 않는 위치를 찾지 못한 경우
            print("사도를 배치할 적절한 위치를 찾지 못했습니다.")
            self.sado_position = QPoint(200, y)  # default position
            occupied_positions.append(self.sado_position)
            self.setFixedSize(width, height)
            self.move(self.sado_position)

    def closeEvent(self, event):
        print("close event!")  # for debugging
        if self.bolddagu_timer.isActive():
            self.bolddagu_timer.stop()
        self.bolddagu_timer.deleteLater()
        if self.standing_timer.isActive():
            self.standing_timer.stop()
        self.standing_timer.deleteLater()

        self.closed.emit()  # 위젯이 닫힐 때 closed 신호 발생
        players.remove(self)
        occupied_positions.remove(self.sado_position)
        self.deleteLater()  # rickTcal 객체 명시적 삭제

        super().closeEvent(event)
        print("deleted!:", players)  # for debugging
        print("occupied positions:", occupied_positions)  # for debugging


class MainWindow(QWidget):
    """
    메인 창 클래스입니다.
    우측 하단의 사도 아이콘 버튼을 클릭하면 사도 설명 다이얼로그 창이 나타납니다.
    해당 창에서 사도에 대한 설명을 확인할 수 있고 화면에 해당 사도를 소환할 수 있으며 rickTcal 데스크톱 앱을 끌 수 있는 버튼이 있습니다.
    """

    def __init__(self):
        super().__init__()
        sado_info_icon = application_path + "/images/static/sado_icon.png"
        self.sado_data = sado_data

        self.layout = QVBoxLayout(self)
        self.sadoIconButton = QPushButton(QIcon(sado_info_icon), "")

        self.initUI()

    def initUI(self):
        # 사도들의 설명 위젯 추가
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

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
        dialog = SadoDescriptionDialog(
            self.sado_data, current_index, application_path, self, title_font, description_font
        )
        dialog.addCurrentSado.connect(self.addSado)
        dialog.exec()

    def addSado(self, sado_name):
        print("addSado before:", players)  # for debugging
        # 화면에 사도 위젯이 3개 이상일 때 추가하지 않음 (성능 이슈 방지 목적)
        if len(players) >= 3:
            print("화면에 띄울 수 있는 사도의 최대 수에 도달했습니다.")
            return

        # 사도를 화면에 추가하는 로직
        sado_info = self.sado_data.get(sado_name)
        if not sado_info:
            print(f"{sado_name} 정보를 찾을 수 없습니다.")
            return

        player = rickTcal(
            sado_name=sado_name,
            bolddagu_x=sado_info["bolddagu_x"],
            bolddagu_y=sado_info["bolddagu_y"],
            idle_len=sado_info["idle"]
        )
        player.show()
        players.append(player)
        print("addSado after:", players)  # for debugging
        print("occupied positions:", occupied_positions)  # for debugging

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
    """
    rickTcal 데스크톱 앱의 메인 로직들을 실행합니다.

    캐릭터(사도) 정보가 저장되는 sado.json 파일의 구조는 CONTRIBUTION.md 파일을 참조해주세요.
    """
    app = QApplication(sys.argv)

    # 커스텀 폰트 적용
    titleFontPath = application_path + "/fonts/Katuri.ttf"
    descriptionFontPath = application_path + "/fonts/ONE MOBILE POP.ttf"

    title_font = QFont("Arial", 16)  # 커스텀 폰트 로드 실패 시, 기본 폰트 Arial로 설정
    description_font = QFont(
        "Arial", 14
    )  # 커스텀 폰트 로드 실패 시, 기본 폰트 Arial로 설정
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
            descriptionFontFamily = QFontDatabase.applicationFontFamilies(
                descriptionFontId
            )[0]
            title_font = QFont(titleFontFamily, 12)
            description_font = QFont(descriptionFontFamily, 10)

    # 사도 데이터 로드
    json_path = os.path.join(
        application_path, "sado.json"
    )  # 사도 데이터 파일 경로 (배포)
    with open(json_path, "r", encoding="utf-8") as file:
        sado_data = json.load(file)

    # 글로벌 참조 로드
    initialize_global_resources(application_path)

    # 캐릭터(사도) 설명 위젯 추가
    mainWindow = MainWindow()
    mainWindow.show()

    # 캐릭터(사도) 로드
    # ~ Version 1.0 초기 캐릭터(사도) 5종 : 버터, 에르핀, 비비, 림, 실피르
    selected_sados = random.sample(list(sado_data.items()), 3)
    for sado_name, sado_info in selected_sados:
        player = rickTcal(
            sado_name=sado_name,
            bolddagu_x=sado_info["bolddagu_x"],
            bolddagu_y=sado_info["bolddagu_y"],
            idle_len=sado_info["idle"]
        )
        player.show()
        players.append(player)
        print(sado_name, ":", player)  # for debugging
    print("rickTcal players:", players)  # for debugging
    print("occupied positions:", occupied_positions)  # for debugging
    sys.exit(app.exec())
