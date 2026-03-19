import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from app.controllers.settings_controller import SettingsController

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.settings = {}
        self.init_ui()
        self.controller = SettingsController()
        self.load_settings()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Download Path
        self.download_label = QLabel("Download Path:")
        self.download_path_display = QLabel("")
        self.download_path_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.download_path_button = QPushButton("Select Path")
        self.download_path_button.clicked.connect(self.select_download_path)

        # Token
        self.refresh_token_label = QLabel("refresh token:")
        self.refresh_token_input = QLineEdit()

        # description
        self.description = QLabel()
        self.description.setText(
            """<p>Please visit <a href="https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362" rel="noopener">@ZipFile Pixiv OAuth Flow</a>
            to get <code>refresh token</code> for using this application</p>"""
        )
        self.description.setOpenExternalLinks(True)  # Enable hyperlink functionality
        self.description.setWordWrap(True)  # Enable word wrapping
        self.description.setMaximumHeight(100)

        # # Database Address
        # self.db_host_label = QLabel("数据库地址:")
        # self.db_host_input = QLineEdit()

        # # Database Address
        # self.db_port_label = QLabel("数据库端口:")
        # self.db_port_input = QLineEdit()

        # # Database Address
        # self.db_user_label = QLabel("数据库用户:")
        # self.db_user_input = QLineEdit()

        # # Database Address
        # self.db_password_label = QLabel("数据库密码:")
        # self.db_password_input = QLineEdit()

        # # Database name
        # self.db_database_label = QLabel("数据库名称:")
        # self.db_database_input = QLineEdit()

        # Buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.load_settings)

        # Adding widgets to layout
        # layout.addWidget(self.download_label)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.download_label)
        path_layout.addWidget(self.download_path_display)
        path_layout.addWidget(self.download_path_button)
        layout.addLayout(path_layout)

        refresh_token_layout = QHBoxLayout()
        refresh_token_layout.addWidget(self.refresh_token_label)
        refresh_token_layout.addWidget(self.refresh_token_input)
        layout.addLayout(refresh_token_layout)

        description_layout = QHBoxLayout()
        description_layout.addWidget(self.description)
        layout.addLayout(description_layout)

        # db_address_layout = QHBoxLayout()
        # db_address_layout.addWidget(self.db_host_label)
        # db_address_layout.addWidget(self.db_host_input)
        # layout.addLayout(db_address_layout)

        # db_address_layout = QHBoxLayout()
        # db_address_layout.addWidget(self.db_port_label)
        # db_address_layout.addWidget(self.db_port_input)
        # layout.addLayout(db_address_layout)

        # db_address_layout = QHBoxLayout()
        # db_address_layout.addWidget(self.db_user_label)
        # db_address_layout.addWidget(self.db_user_input)
        # layout.addLayout(db_address_layout)

        # db_address_layout = QHBoxLayout()
        # db_address_layout.addWidget(self.db_password_label)
        # db_address_layout.addWidget(self.db_password_input)
        # layout.addLayout(db_address_layout)

        # db_address_layout = QHBoxLayout()
        # db_address_layout.addWidget(self.db_database_label)
        # db_address_layout.addWidget(self.db_database_input)
        # layout.addLayout(db_address_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        # Load settings from the JSON file.
        self.settings = self.controller.get_settings()

        # Populate fields
        self.download_path_display.setText(self.settings.get("download_path", ""))
        self.refresh_token_input.setText(self.settings.get("refresh_token", ""))
        # self.db_host_input.setText(self.settings.get("db_host", ""))
        # self.db_port_input.setText(self.settings.get("db_port", ""))
        # self.db_user_input.setText(self.settings.get("db_user", ""))
        # self.db_password_input.setText(self.settings.get("db_password", ""))
        # self.db_database_input.setText(self.settings.get("db_database", ""))

    def save_settings(self):
        # Save current settings to the JSON file.
        self.settings["download_path"] = self.download_path_display.text()
        self.settings["refresh_token"] = self.refresh_token_input.text()
        # self.settings["db_host"] = self.db_host_input.text()
        # self.settings["db_port"] = self.db_port_input.text()
        # self.settings["db_user"] = self.db_user_input.text()
        # self.settings["db_password"] = self.db_password_input.text()
        # self.settings["db_database"] = self.db_database_input.text()

        self.controller.save_settings(self.settings)
        self.show_info()

    def select_download_path(self):
        """Open a file dialog to select the download path."""
        path = QFileDialog.getExistingDirectory(self, "Select Download Path")
        logging.debug("SettingsWindow.select_download_path: Download Path is: %s", path)
        if path:
            self.download_path_display.setText(path.replace("/", "\\"))

    def show_info(self):
        QMessageBox.information(self, "Info", "Successful", QMessageBox.StandardButton.Ok)
