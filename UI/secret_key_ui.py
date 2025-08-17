from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QLabel
from UI.BaseDialogUI import BaseDialogUI


class SecretKeyDialog(BaseDialogUI):
    def __init__(self, key):
        super().__init__("注意", (100, 100, 300, 200))
        self.key = key
        self.init_ui()
        self.move_to_center()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        msg_label = QLabel("请务必保管好这个密钥，此密钥是获取密码的唯一凭证，且此密钥只生成一次")
        msg_label.setStyleSheet("color: rgb(255, 0, 0);font-weight: bold;font-size: 14px;")
        main_layout.addWidget(msg_label)

        plain_text_edit = QPlainTextEdit()
        plain_text_edit.setStyleSheet("font-size: 14px;")
        plain_text_edit.setPlainText(self.key)
        plain_text_edit.setReadOnly(True)
        main_layout.addWidget(plain_text_edit)


        self.setLayout(main_layout)
