import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QScrollArea,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt

from encrypted_file import EncryptedMessage
from UI.add_password_ui import AddPasswordDialog
from UI.setting_ui import SettingsDialog
from UI.secret_key_ui import SecretKeyDialog
from UI.BaseAppMessage import BaseAppMessage
from db.db_tools import SQLiteDB
from qr_code import generate_qrcode
from exc_chrome import launch_chrome


def get_configs_path():
    exe_dir = Path(sys.executable).parent/"_internal" if getattr(sys, 'frozen', False) else Path(__file__).parent
    config_dir = exe_dir / "config"
    secret_key_path = config_dir / "secret_key.skf"
    sqlite_db_path = config_dir / "sqlite_db.db"
    return secret_key_path, sqlite_db_path

# 获取路径
SECRET_KEY_PATH, SQLITE_DB_PATH = get_configs_path()


class PasswordManager(QMainWindow):
    def __init__(self, position = (100, 100, 800, 500)):
        super().__init__()
        SQLiteDB.create_db(SQLITE_DB_PATH)
        self.setWindowTitle("密码管理器")
        self.setGeometry(*position)

        # 设置主窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #2E2E2E;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #00C8A4;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00D8B4;
            }
            QListWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
            }
            QFrame {
                background-color: #1E1E1E;
                border-radius: 4px;
            }
        """)

        self.init_ui()
        self.center_window()

    def connect_and_read_db(self, db_path):
        with SQLiteDB(db_path) as db:
            db.create_table('user',
                            {'id': 'INTEGER', 'user_name': 'TEXT', 'pwd': 'TEXT', 'site': 'TEXT'},
                            'id')
            datas = db.select(table_name='user', columns= ['id', 'user_name', 'pwd', 'site'])
        # print(f'Datas : {datas}')
        return datas

    def center_window(self):
        """将窗口移动到屏幕中央"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # 计算中心位置
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        # 移动窗口到计算出的位置
        self.move(window_geometry.topLeft())

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # 侧边导航栏
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar, stretch=1)

        # 主内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        # 顶部工具栏
        toolbar = self.create_toolbar()
        content_layout.addWidget(toolbar)

        # 密码列表区域
        self.password_list = self.create_password_list(self.connect_and_read_db(SQLITE_DB_PATH))
        content_layout.addWidget(self.password_list, stretch=1)

        # 状态栏
        self.status_bar = self.create_status_bar()
        content_layout.addWidget(self.status_bar)

        main_layout.addWidget(content_widget, stretch=4)

        self.setCentralWidget(main_widget)
        self.get_secret_key(SECRET_KEY_PATH)

    def get_secret_key(self, default_key_path):
        if os.path.exists(default_key_path):
            with open(default_key_path, "r") as f:
                lines = f.readlines()
                if lines:
                    key = lines[0].strip()
                    self.key_box.setText(key)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("""
                    QFrame {
                        background-color: #1E1E1E;
                    }
                """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        # 导航项
        nav_items = [
            ("所有密码", "icons/all_passwords.png", self.show_disabled_feature_alert),
            ("常用", "icons/frequent.png", self.show_disabled_feature_alert),
            ("社交媒体", "icons/social.png", self.show_disabled_feature_alert),
            ("金融", "icons/finance.png", self.show_disabled_feature_alert),
            ("生成密钥", "icons/work.png", self.generate_key),
            ("回收站", "icons/trash.png", self.show_disabled_feature_alert),
            ("设置", "icons/settings.png", self.settings),
        ]

        for text, icon, function in nav_items:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("""
                QPushButton {
                    text-align: center;
                    padding: 10px;
                    background-color: #0047AB;
                    color: #FFF8DC;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2E2E2E;
                }
            """)
            if function is not None:
                btn.clicked.connect(function)
            sidebar_layout.addWidget(btn)

        # 添加间距
        sidebar_layout.addStretch()

        # 用户信息
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(0, 0, 0, 0)

        avatar = QLabel()
        avatar.setPixmap(QIcon("D:/PythonProject/LockBox/UI/icons/user.png").pixmap(26, 26))
        # avatar.setPixmap(QIcon("./icons/user.png").pixmap(26, 26))
        user_layout.addWidget(avatar)

        user_info = QLabel("用户:\nuser@example.com")
        user_info.setStyleSheet("font-size: 12px;")
        user_layout.addWidget(user_info, stretch=1)

        # user_settings_btn = QToolButton()
        # user_settings_btn.setIcon(QIcon("icons/settings.png"))
        # user_settings_btn.setIconSize(QSize(20, 20))
        # user_layout.addWidget(user_settings_btn)

        sidebar_layout.addWidget(user_widget)

        return sidebar

    def generate_key(self):
        k = EncryptedMessage.generate_secret_key()
        self.secret_key_dialog = SecretKeyDialog(k)
        self.secret_key_dialog.show()


    def create_toolbar(self):
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title = QLabel("密码管理器")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        toolbar_layout.addWidget(title)

        # 搜索框
        self.key_box = QLineEdit()
        self.key_box.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.key_box.setPlaceholderText("密钥")
        self.key_box.setMinimumWidth(200)
        toolbar_layout.addWidget(self.key_box, stretch=1)

        # 添加按钮
        add_btn = QPushButton("新增密码")
        add_btn.setIcon(QIcon("icons/add.png"))
        add_btn.clicked.connect(self.add_password)
        toolbar_layout.addWidget(add_btn)

        return toolbar

    def add_password(self):
        if self.key_box.text() == "":
            BaseAppMessage().show_message('请在顶部密钥框填写您的密钥！', 2500)
            return
        self.sub_window = AddPasswordDialog()
        self.sub_window.data_submitted.connect(self.create_password_item)
        self.sub_window.show()

    def settings(self):
        self.setting_dialog = SettingsDialog()
        self.setting_dialog.show()

    def show_disabled_feature_alert(self):
        BaseAppMessage().show_message("功能暂未开放", 2500)


    def create_password_list(self, datas=None):
        self.scroll_area = QScrollArea()
        # self.scroll_area.setStyleSheet("border: 2px solid red;")
        self.scroll_area.setWidgetResizable(True)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(5, 5, 5, 5)
        self.container_layout.setSpacing(10)

        self.max_id = 0
        used_id = set()
        if datas is not None:
            for data in datas:
                used_id.add(data['id'])
                if data['id'] >= self.max_id:
                    self.max_id = data['id']
                self.create_password_item(data)
        if self.max_id == 0:
            self.id_pool = {1,2,3,4,5,6,7,8,9,10}
        else:
            self.id_pool = {i for i in range(1, self.max_id + 5)} - used_id


        self.container_layout.addStretch()
        self.scroll_area.setWidget(container)

        return self.scroll_area

    def create_password_item(self, data):
        site = data['site']
        username = data['user_name']
        pwd = data['pwd']
        record_id = data.get('id')
        if record_id is None:
            if self.id_pool:
                record_id = self.id_pool.pop()
            else:
                record_id = self.max_id + 1
            if self.max_id <= record_id:
                self.max_id = record_id

            # 入库前转为密文
            transformer = EncryptedMessage(self.key_box.text())
            # secret_user_name = transformer.encrypt(username)
            secret_user_pwd = transformer.encrypt(pwd)

            # 插入数据
            with SQLiteDB(SQLITE_DB_PATH) as db:
                db.insert('user', {'id': record_id, 'site': site, 'user_name': username, 'pwd': secret_user_pwd})


        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                border-radius: 6px;
            }
        """)
        item.setMinimumHeight(80)

        item.pwd = pwd
        item.record_id = record_id

        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 10, 15, 10)

        # 网站图标
        icon = QLabel()
        icon.setPixmap(QIcon("icons/website.png").pixmap(40, 40))
        layout.addWidget(icon)

        # 信息区域
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)

        item.site_label = QLabel(site)
        item.site_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        item.site_label.setCursor(Qt.CursorShape.PointingHandCursor)  # 设置手型光标

        # 通过事件过滤器实现点击
        item.site_label.mousePressEvent = lambda event, url=site: (
            launch_chrome(url) if event.button() == Qt.MouseButton.LeftButton else None
        )

        info_layout.addWidget(item.site_label)

        item.user_label = QLabel(username)
        item.user_label.setStyleSheet("color: #AAAAAA;")
        info_layout.addWidget(item.user_label)

        layout.addWidget(info_widget, stretch=1)

        # 操作按钮
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        item.copy_btn = QPushButton("复制密码")
        item.copy_btn.setStyleSheet("background-color: transparent;color: rgb(255, 255, 255);font-size:14px")
        item.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        item.copy_btn.clicked.connect(lambda: self.cp_btn(item))
        btn_layout.addWidget(item.copy_btn)

        item.qr_code_btn = QPushButton("二维码")
        item.qr_code_btn.setStyleSheet("background-color: transparent;color: rgb(255, 255, 255);font-size:14px")
        item.qr_code_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        item.qr_code_btn.clicked.connect(lambda: self.qr_code_btn(item))
        btn_layout.addWidget(item.qr_code_btn)

        item.del_btn = QPushButton("删除")
        item.del_btn.setStyleSheet("background-color: transparent;color: rgb(255, 255, 255);font-size:14px")
        item.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        item.del_btn.clicked.connect(lambda: self.del_btn(item))
        btn_layout.addWidget(item.del_btn)

        layout.addWidget(btn_widget)

        self.container_layout.insertWidget(0, item)

    def qr_code_btn(self, item):
        if self.key_box.text() == '':
            BaseAppMessage().show_message("请在上方密钥栏填写密钥", 2500)
            return
        key_text = self.key_box.text()
        transformer = EncryptedMessage(key_text)
        with SQLiteDB(SQLITE_DB_PATH) as db:
            res = db.select('user', ['pwd'], f'id={item.record_id}', fetch_all=False)

        qr_site_info = item.site_label.text()
        qr_user_name = item.user_label.text()
        qr_pwd_info = transformer.decrypt(res[0]['pwd'])

        generate_qrcode(f"site:{qr_site_info}\nuser:{qr_user_name}\npwd:{qr_pwd_info}")


    def cp_btn(self, item):
        if self.key_box.text() == '':
            BaseAppMessage().show_message("请在上方密钥栏填写密钥", 2500)
            return
        # copy_app = QApplication([])  # 必须创建 QApplication 实例?
        key_text = self.key_box.text()
        transformer = EncryptedMessage(key_text)
        with SQLiteDB(SQLITE_DB_PATH) as db:
            res = db.select('user', ['pwd'], f'id={item.record_id}', fetch_all=False)
            text = transformer.decrypt(res[0]['pwd'])
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        BaseAppMessage().show_message(f"{text} 已复制到剪贴板", 2500)

    def del_btn(self, item):
        item.deleteLater()
        self.container_layout.removeWidget(item)
        with SQLiteDB(SQLITE_DB_PATH) as db:
            db.delete('user', f"id={item.record_id}")

    def create_status_bar(self):
        status_bar = QWidget()
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 5, 10, 5)

        status_encrypted = QLabel("🔒 已加密")
        status_layout.addWidget(status_encrypted)

        status_sync = QLabel("🔄 最后同步: 今天 15:30")
        status_layout.addWidget(status_sync)

        status_stats = QLabel("📊 总计: 42 个项目")
        status_layout.addWidget(status_stats, stretch=1)

        status_layout.addWidget(QLabel("v1.0.0"))

        return status_bar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())