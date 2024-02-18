# TODO: 사도 이미지 추가, 폰트 추가, 레이아웃 예쁘게 수정
# --------------------------------------------------------------------------
# 사도(캐릭터)에 대한 설명 위젯을 다루는 스크립트입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QHBoxLayout,
)


class SadoDescriptionDialog(QDialog):
    addCurrentSado = pyqtSignal(str)  # 현재 설명을 보고 있는 사도 이름을 전달하는 신호

    def __init__(self, sado_data, current_index, parent=None):
        super().__init__(parent)
        self.sado_data = sado_data
        self.current_index = current_index
        self.initUI()

    def initUI(self):
        self.setWindowTitle("사도 설명")
        layout = QVBoxLayout()

        # 사도 설명 라벨
        self.descriptionLabel = QLabel(self)
        layout.addWidget(self.descriptionLabel)

        # '현재 사도를 화면에 추가' 버튼
        self.addButton = QPushButton("현재 사도를 화면에 추가")
        self.addButton.clicked.connect(self.addSadoToScreen)
        layout.addWidget(self.addButton)

        # 이전/다음 버튼
        navLayout = QHBoxLayout()
        self.prevButton = QPushButton("< 이전")
        self.prevButton.clicked.connect(self.showPrevDescription)
        navLayout.addWidget(self.prevButton)

        self.nextButton = QPushButton("다음 >")
        self.nextButton.clicked.connect(self.showNextDescription)
        navLayout.addWidget(self.nextButton)

        layout.addLayout(navLayout)
        self.setLayout(layout)

        self.updateDescription()

    def updateDescription(self):
        sado_name = list(self.sado_data.keys())[self.current_index]
        self.descriptionLabel.setText(
            f"{sado_name}: {self.sado_data[sado_name]['description']}"
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
