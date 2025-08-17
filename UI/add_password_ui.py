from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QPushButton,
                             QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QApplication)
import sys
from UI.BaseDialogUI import BaseDialogUI
from UI.BaseAppMessage import BaseAppMessage


class AddPasswordDialog(BaseDialogUI):
    data_submitted = pyqtSignal(dict)
    def __init__(self):
        super().__init__("详细信息", (100, 100, 300, 200))
        self.init_ui()
        self.move_to_center()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(7)

        # 地址栏
        address_widget = QWidget()
        address_layout = QHBoxLayout(address_widget)
        name_label = QLabel("名称:")
        name_label.setStyleSheet("font: 15px;")
        address_layout.addWidget(name_label)
        self.address_line_edit = QLineEdit()
        self.address_line_edit.setPlaceholderText("ip地址，app名称等备注信息...")
        self.address_line_edit.setStyleSheet("font: 15px;")
        address_layout.addWidget(self.address_line_edit)
        main_layout.addWidget(address_widget)

        # 用户名栏
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        username_label = QLabel("用户名:")
        username_label.setStyleSheet("font: 15px;")
        user_layout.addWidget(username_label)
        self.user_line_edit = QLineEdit()
        self.user_line_edit.setStyleSheet("font: 15px;")
        user_layout.addWidget(self.user_line_edit)
        main_layout.addWidget(user_widget)

        # 密码栏
        password_widget = QWidget()
        password_layout = QHBoxLayout(password_widget)
        password_label = QLabel("密码:")
        password_label.setStyleSheet("font: 15px;")
        password_layout.addWidget(password_label)
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setStyleSheet("font: 15px;")
        password_layout.addWidget(self.password_line_edit)
        main_layout.addWidget(password_widget)

        # 确认密码栏
        confirm_password_widget = QWidget()
        confirm_password_layout = QHBoxLayout(confirm_password_widget)
        confirm_label = QLabel("确认密码:")
        confirm_label.setStyleSheet("font: 15px;")
        confirm_password_layout.addWidget(confirm_label)
        self.confirm_password_line_edit = QLineEdit()
        self.confirm_password_line_edit.setStyleSheet("font: 15px;")
        confirm_password_layout.addWidget(self.confirm_password_line_edit)
        main_layout.addWidget(confirm_password_widget)

        # 保存和取消按钮
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        save_button = QPushButton("Save")
        save_button.setStyleSheet("font: 15px;")
        save_button.clicked.connect(self.save_password)
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("font: 15px;")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

    def save_password(self):
        address = self.address_line_edit.text()
        user = self.user_line_edit.text()
        password = self.password_line_edit.text()
        confirm_password = self.confirm_password_line_edit.text()
        if address and user and (password == confirm_password):
            data = {'site': address,
                    'user_name': user,
                    'pwd': password}
            self.data_submitted.emit(data)
        else:
            BaseAppMessage().show_message("填写信息存在空或两次输入密码不一致", 2500)

    def cancel(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddPasswordDialog()
    window.show()
    sys.exit(app.exec())