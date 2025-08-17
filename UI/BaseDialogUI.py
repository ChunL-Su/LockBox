from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QWidget, QVBoxLayout, QLabel)


class BaseDialogUI(QWidget):
    def __init__(self, title='', position=(100, 100, 300, 200)):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(*position)

    def move_to_center(self):
        """将窗口移动到屏幕中央"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # 计算中心位置
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        # 移动窗口到计算出的位置
        self.move(window_geometry.topLeft())

