from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
)
from app.controllers.pixiv_auth_controller import PixivAuthController

class PixivAuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.controller = PixivAuthController()
        self.authToken = {}
        self.init_ui()
        self.load_settings()
        pass

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        self.refresh_token_label = QLabel("refresh token:")
        self.refresh_token_input = QLineEdit()

        # description
        self.description = QLabel()
        self.description.setText(
            """<p>现在 Pixiv 不支持账号密码使用，获取 <code>refresh token</code> 请访问 
            <a href="https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362" rel="noopener">@ZipFile Pixiv OAuth Flow</a>
             按照步骤操作即可</p>"""
        )
        self.description.setOpenExternalLinks(True)  # Enable hyperlink functionality
        self.description.setWordWrap(True)  # Enable word wrapping
        self.description.setMaximumHeight(100)

        # Buttons
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)

        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.load_settings)

        refresh_token_layout = QHBoxLayout()
        refresh_token_layout.addWidget(self.refresh_token_label)
        refresh_token_layout.addWidget(self.refresh_token_input)
        layout.addLayout(refresh_token_layout)

        description_layout = QHBoxLayout()
        description_layout.addWidget(self.description)
        layout.addLayout(description_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        # Load settings from the JSON file.
        self.authToken = self.controller.get_pixiv_auth_token()

        # Populate fields
        self.refresh_token_input.setText(self.authToken)
    
    def save_settings(self):
        # Save current settings to the JSON file.
        self.authToken = self.refresh_token_input.text()

        self.controller.save_pixiv_auth_token(self.authToken)
        self.show_info()
    
    def show_info(self):
        QMessageBox.information(self, "信息提示", "操作成功！", QMessageBox.StandardButton.Ok)