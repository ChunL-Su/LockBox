from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
                             QFileDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from configparser import ConfigParser
from UI.BaseDialogUI import BaseDialogUI
import os


class SettingsDialog(BaseDialogUI):
    def __init__(self):
        super().__init__("🗂️ 设置存储路径", (100, 100, 400, 200))
        self.init_ui()
        self.move_to_center()

    def init_ui(self):
        self.setWindowIcon(QIcon("folder_icon.png"))
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 路径输入框
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请输入或选择路径...")
        self.path_input.textChanged.connect(self.validate_path)
        layout.addWidget(QLabel("路径:"))
        layout.addWidget(self.path_input)

        # 浏览按钮
        browse_btn = QPushButton("🖿 浏览文件夹")
        browse_btn.clicked.connect(self.browse_folder)
        layout.addWidget(browse_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # 确定/取消按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.ok_btn.setEnabled(False)  # 初始禁用
        self.ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def accept(self):
        print("accepted")


    def reject(self):
        print("rejected")

    def browse_folder(self):
        """打开文件夹选择对话框"""
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if path:
            secret_key_file = 'k.skf'
            self.path_input.setText(path)
            file_path = os.path.join(path, secret_key_file)
            try:
                with open(file_path, 'x') as f:  # 'x' 表示独占创建模式
                    pass
            except FileExistsError:
                print("文件已存在，创建失败")


    def validate_path(self):
        """检查路径是否有效"""
        path = self.path_input.text()
        is_valid = len(path) > 0  # 这里替换为实际路径检查逻辑
        self.ok_btn.setEnabled(is_valid)
        # 可选：动态样式（红色边框提示错误）
        self.path_input.setStyleSheet(
            "border: 1px solid red;" if not is_valid else ""
        )


if __name__ == '__main__':
    config = ConfigParser()
    config.read("../config.ini")

    # 获取路径
    path1 = config.get("db_path", "sqlite_db_path")
    print(path1)  # 输出: ./output/images