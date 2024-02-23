# TODO: 레이아웃 배경 추가
# ignore: N801, N802, N806
# --------------------------------------------------------------------------
# 사도(캐릭터)에 대한 설명 위젯을 다루는 스크립트입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QApplication
)


class SadoDescriptionDialog(QDialog):
    addCurrentSado = pyqtSignal(str)  # 현재 설명을 보고 있는 사도 이름을 전달하는 신호

    def __init__(
        self,
        sado_data,
        current_index,
        parent=None,
        titleFont=None,
        descriptionFont=None,
    ):
        super().__init__(parent)
        self.sado_data = sado_data
        self.current_index = current_index
        self.titleFont = titleFont
        self.descriptionFont = descriptionFont
        self.quitIcon = QIcon("images/static/quit_icon.png")

        self.tmiLabel = QLabel("TMI")
        self.nameLabel = QLabel("사도 이름")
        self.imageLabel = QLabel(self)
        self.descriptionLabel = QLabel(self)
        self.addButton = QPushButton("현재 사도를 화면에 추가")
        self.prevButton = QPushButton("< 이전")
        self.nextButton = QPushButton("다음 >")
        self.quitButton = QPushButton(icon=self.quitIcon, text="종료")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("사도 설명")

        # 메인 레이아웃
        layout = QHBoxLayout()

        # TMI 제목 라벨
        self.tmiLabel.setFont(self.titleFont)

        # 사도 이름 라벨
        self.nameLabel.setFont(self.titleFont)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 사도 이미지 & 사도 이름 라벨이 들어갈 세로 레이아웃
        nameLabelLayout = QVBoxLayout()
        nameLabelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 사도 설명 & 네비게이션 버튼이 들어갈 세로 레이아웃
        descriptionLayout = QVBoxLayout()
        descriptionLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        navLayout = QHBoxLayout()
        navLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # 사도 이미지 라벨
        nameLabelLayout.addWidget(self.imageLabel)
        nameLabelLayout.addWidget(self.nameLabel)

        # 사도 설명 라벨
        # TODO: 설명 레이아웃 배경 추가
        descriptionLayout.addWidget(self.tmiLabel)

        self.descriptionLabel.setFont(self.descriptionFont)
        descriptionLayout.addWidget(self.descriptionLabel)

        # '현재 사도를 화면에 추가' 버튼
        self.addButton.setFont(self.titleFont)
        self.addButton.clicked.connect(self.addSadoToScreen)
        navLayout.addWidget(self.addButton)

        # 이전/다음 버튼
        self.prevButton.setFont(self.titleFont)
        self.prevButton.clicked.connect(self.showPrevDescription)
        navLayout.addWidget(self.prevButton)

        self.nextButton.setFont(self.titleFont)
        self.nextButton.clicked.connect(self.showNextDescription)
        navLayout.addWidget(self.nextButton)

        # 데스크톱 앱(rickTcal) 종료 버튼
        self.quitButton.setFont(self.titleFont)
        self.quitButton.clicked.connect(QApplication.instance().quit)
        navLayout.addWidget(self.quitButton)

        descriptionLayout.addLayout(navLayout)

        layout.addLayout(nameLabelLayout)
        layout.addLayout(descriptionLayout)

        # TODO: 사도 종족 별 배경 화면 변경
        self.setStyleSheet("background: #000000;")

        self.setLayout(layout)
        self.updateDescription()

    def updateDescription(self):
        sado_name = list(self.sado_data.keys())[self.current_index]
        pixmap = QPixmap(f"images/static/{sado_name}/{sado_name}_icon.png").scaled(100, 100)

        # TMI 라벨에 oneline_description을 설정합니다.
        self.tmiLabel.setText(f"TMI\n\n{self.sado_data[sado_name]['oneline_description']}")

        # 이미지 라벨의 크기를 고정합니다.
        self.imageLabel.setFixedSize(100, 100)

        self.imageLabel.setPixmap(pixmap)
        self.nameLabel.setText(sado_name)
        self.descriptionLabel.setText(
            f"{self.sado_data[sado_name]['description']}"
        )

    def showPrevDescription(self):
        self.current_index = (self.current_index - 1) % len(self.sado_data)
        self.updateDescription()

    def showNextDescription(self):
        self.current_index = (self.current_index + 1) % len(self.sado_data)
        self.updateDescription()

    def addSadoToScreen(self):
        sado_name = list(self.sado_data.keys())[self.current_index]
        self.addCurrentSado.emit(sado_name)
