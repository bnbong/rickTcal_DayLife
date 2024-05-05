# ignore: N801, N802, N806
# --------------------------------------------------------------------------
# 사도(캐릭터)에 대한 설명 위젯을 다루는 스크립트입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QPalette
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QApplication,
    QWidget,
)

SADO_NAME_MAP = {
    "butter": "버터",
    "silfir": "실피르",
    "vivi": "비비",
    "erpin": "에르핀",
    "rim": "림",
}


SPECIES_BACKGROUND_MAP = {
    "수인": "suin.png",
    "요정": "fairy.png",
    "용족": "dragon.png",
    "엘프": "elf.png",
    "유령": "ghost.png",
    "마녀": "witch.png",
    "정령": "spirit.png",
}


class SadoDescriptionDialog(QDialog):
    addCurrentSado = pyqtSignal(str)  # 현재 설명을 보고 있는 사도 이름을 전달하는 신호

    def __init__(
        self,
        sado_data,
        current_index,
        application_path,
        parent=None,
        titleFont=None,
        descriptionFont=None,
    ):
        super().__init__(parent)
        self.sado_data = sado_data
        self.current_index = current_index
        self.titleFont = titleFont
        self.descriptionFont = descriptionFont
        self.application_path = application_path
        self.image_path = os.path.join(self.application_path, "images", "static")
        self.quitIcon = QIcon(os.path.join(self.image_path, "quit_icon.png"))
        self.prevIcon = QIcon(os.path.join(self.image_path, "prev_button.png"))
        self.nextIcon = QIcon(os.path.join(self.image_path, "next_button.png"))

        self.tmiLabel = QLabel("TMI")  # text
        self.nameLabel = QLabel("사도 이름")  # text
        self.iconLabel = QLabel(self)  # image
        self.imageLabel = QLabel(self)  # image
        self.descriptionLabel = QLabel(self)  # text
        self.addButton = QPushButton("현재 사도를 화면에 추가")
        self.prevButton = QPushButton(self)
        self.nextButton = QPushButton(self)
        self.quitButton = QPushButton(icon=self.quitIcon, text="종료")

        self.initUI()

    def initUI(self):
        self.setFixedSize(1000, 750)
        self.setWindowTitle("사도 설명")

        # 다어얼로그 메인 레이아웃
        layout = QHBoxLayout()

        # TMI 제목 라벨
        self.tmiLabel.setFont(self.titleFont)

        # 사도 이름 라벨
        self.nameLabel.setFont(self.titleFont)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # nav 바와 사도 관련 정보 레이아웃을 포함하는 레이아웃
        mainLayout = QVBoxLayout()

        # 사도 관련 정보가 들어가는 핵심 레이아웃
        sadoLayout = QHBoxLayout()

        # 사도 이미지 & 사도 이름 라벨이 들어갈 세로 레이아웃
        nameLabelLayout = QVBoxLayout()
        nameLabelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 사도 설명 & TMI가 들어갈 세로 레이아웃
        descriptionLayout = QVBoxLayout()  # 사도 설명 전체 레이아웃
        descriptionLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tmiLayout = QHBoxLayout()  # TMI 레이아웃
        tmiLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        tmiLayout.addWidget(self.iconLabel)
        tmiLayout.addWidget(self.tmiLabel)

        # 사도 이미지 라벨
        nameLabelLayout.addWidget(self.imageLabel)
        nameLabelLayout.addWidget(self.nameLabel)

        # 사도 설명 라벨
        descriptionLayout.addLayout(tmiLayout)
        self.descriptionLabel.setFont(self.descriptionFont)
        descriptionLayout.addWidget(self.descriptionLabel)

        navLayout = QHBoxLayout()  # 네비게이션 버튼 레이아웃
        navLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # '현재 사도를 화면에 추가' 버튼
        self.addButton.setFont(self.titleFont)
        self.addButton.clicked.connect(self.addSadoToScreen)
        navLayout.addWidget(self.addButton)

        # 데스크톱 앱(rickTcal) 종료 버튼
        self.quitButton.setFont(self.titleFont)
        self.quitButton.clicked.connect(QApplication.instance().quit)
        navLayout.addWidget(self.quitButton)

        # 이전/다음 버튼
        self.prevButton.setFont(self.titleFont)
        self.prevButton.clicked.connect(self.showPrevDescription)
        self.prevButton.setIcon(self.prevIcon)
        self.prevButton.setIconSize(QSize(50, 50))

        self.nextButton.setFont(self.titleFont)
        self.nextButton.clicked.connect(self.showNextDescription)
        self.nextButton.setIcon(self.nextIcon)
        self.nextButton.setIconSize(QSize(50, 50))

        sadoLayout.addLayout(nameLabelLayout)
        sadoLayout.addLayout(descriptionLayout)

        descriptionWidget = QWidget()
        descriptionWidget.setLayout(sadoLayout)

        # 레이아웃 스타일 적용
        sadoLayout.setContentsMargins(50, 50, 50, 50)

        # TODO: 윈도우 빌드에서 background 이미지를 불러오지 못하는 문제 해결 필요
        descriptionWidget.setStyleSheet(
            """
            QWidget {
                border-width: 40px;
                border-image: url('"""
            + os.path.join(
                self.application_path,
                "images",
                "static",
                "backgrounds",
                "description.png",
            )
            + """');
            }
        """
        )
        self.nameLabel.setStyleSheet(
            "background-color: transparent; border-image: none; color : black; font-size: 20px;"
        )
        self.tmiLabel.setStyleSheet(
            "background-color: transparent; border-image: none; color : black; font-size: 18px;"
        )
        self.iconLabel.setStyleSheet(
            "background-color: transparent; border-image: none;"
        )
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setStyleSheet(
            "background-color: transparent; "
            "border-image: none; color : black; "
            "max-width: 400px; min-height: 250px; font-size: 15px;"
        )
        self.imageLabel.setStyleSheet("border-image: none;")
        self.addButton.setStyleSheet("color : black;")
        self.quitButton.setStyleSheet("color : black;")
        self.nextButton.setStyleSheet(
            "border-image: none; background-color: transparent; border: none;"
        )
        self.prevButton.setStyleSheet(
            "border-image: none; background-color: transparent; border: none;"
        )

        # 레이아웃 적용
        mainLayout.addWidget(descriptionWidget)
        mainLayout.addLayout(navLayout)

        layout.addWidget(self.prevButton)
        layout.addLayout(mainLayout)
        layout.addWidget(self.nextButton)

        self.setLayout(layout)
        self.updateDescription()

    def updateDescription(self):
        sado_name = list(self.sado_data.keys())[self.current_index]
        sado_hangeul_name = SADO_NAME_MAP.get(sado_name)
        species = self.sado_data[sado_name].get("species")

        background_image = SPECIES_BACKGROUND_MAP.get(species, "suin.png")
        self.setBackgroundImage(background_image)

        # 사도 이미지 로드
        icon_pixmap = QPixmap(
            os.path.join(self.image_path, f"{sado_name}", f"{sado_name}_icon.png")
        ).scaled(100, 100)
        profile_pixmap = QPixmap(
            os.path.join(self.image_path, f"{sado_name}", f"{sado_name}_profile.png")
        ).scaled(365, 512, Qt.AspectRatioMode.KeepAspectRatio)
        sado_icon = QIcon(icon_pixmap)
        self.setWindowIcon(sado_icon)

        # TMI 라벨에 oneline_description을 설정.
        self.tmiLabel.setText(
            f"TMI\n\n{self.sado_data[sado_name]['oneline_description']}"
        )

        self.iconLabel.setPixmap(icon_pixmap)
        self.imageLabel.setPixmap(profile_pixmap)
        self.nameLabel.setText(sado_hangeul_name)
        self.descriptionLabel.setText(f"{self.sado_data[sado_name]['description']}")

    def setBackgroundImage(self, image_file):
        backgroundpixmap = (
            QPixmap(os.path.join(self.image_path, "backgrounds", f"{image_file}"))
        ).scaled(QSize(100, 100), Qt.AspectRatioMode.KeepAspectRatio)
        brush = QBrush(backgroundpixmap)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def showPrevDescription(self):
        self.current_index = (self.current_index - 1) % len(self.sado_data)
        self.updateDescription()

    def showNextDescription(self):
        self.current_index = (self.current_index + 1) % len(self.sado_data)
        self.updateDescription()

    def addSadoToScreen(self):
        sado_name = list(self.sado_data.keys())[self.current_index]
        self.addCurrentSado.emit(sado_name)
