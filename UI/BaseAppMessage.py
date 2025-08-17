from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtCore import QPropertyAnimation, QTimer, Qt
import sys

default_msg_style = """
            background-color: rgba(50, 50, 50, 180);
            color: white;
            border-radius: 10px;
            padding: 15px;
            font-size: 18px;
        """

class BaseAppMessage(QLabel):
    def __init__(self, parent=None, style=""):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if not style:
            self.setStyleSheet(default_msg_style)
        else:
            self.setStyleSheet(style)
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.adjustSize()

    def show_message(self, text, duration=2000):
        """显示淡入淡出消息"""
        self.setText(text)
        self.adjustSize()

        # 确保在父窗口中心显示
        if self.parent():
            self.move(
                self.parent().width() // 2 - self.width() // 2,
                self.parent().height() // 3 - self.height() // 2
            )

        # 淡入动画
        self.fade_in()

        # 定时器用于在显示一段时间后淡出
        QTimer.singleShot(duration, self.fade_out)
        # self.deleteLater()


    def fade_in(self):
        """淡入效果"""
        self.show()
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def fade_out(self):
        """淡出效果"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.close)
        self.animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    BaseAppMessage().show_message('哈哈哈hhhHHHH', 2500)
    sys.exit(app.exec())