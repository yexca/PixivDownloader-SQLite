import logging

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.threads.download_threads import DownloadThread

logger = logging.getLogger(__name__)


class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None

    def init_ui(self):
        layout = QVBoxLayout()

        # 画师 ID
        self.user_id_label = QLabel("User ID:")
        self.user_id_input = QLineEdit()

        # 作品 ID
        self.illust_id_label = QLabel("Artwork ID:")
        self.illust_id_input = QLineEdit()

        # Button
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_download)

        user_id_layout = QHBoxLayout()
        user_id_layout.addWidget(self.user_id_label)
        user_id_layout.addWidget(self.user_id_input)
        layout.addLayout(user_id_layout)

        illust_id_layout = QHBoxLayout()
        illust_id_layout.addWidget(self.illust_id_label)
        illust_id_layout.addWidget(self.illust_id_input)
        layout.addLayout(illust_id_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start_download(self):
        try:
            self.button.setEnabled(False)
            self.button.setText("verify typing")
            # 判断输入
            if self.user_id_input.text() or self.illust_id_input.text():
                self.thread = DownloadThread(self.user_id_input.text(), self.illust_id_input.text())
                self.thread.progress.connect(self.update_button)
                self.thread.finished.connect(self.task_finished)
                self.thread.start()
            else:
                self.show_warn()
        except Exception as e:
            logger.exception("Error in start_download: %s", e)
            self.button.setEnabled(True)
            self.button.setText("Start")
            QMessageBox.warning(
                self,
                "Info",
                "Error at search user, Please Check User ID",
                QMessageBox.StandardButton.Ok,
            )

    def startDownload(self):
        self.start_download()

    def update_button(self, info):
        self.button.setText(info)

    def task_finished(self):
        QMessageBox.information(self, "Info", "Download Completed", QMessageBox.StandardButton.Ok)
        self.button.setEnabled(True)
        self.button.setText("Start")

    def show_warn(self):
        QMessageBox.warning(
            self, "Info", "Please input User ID or Artwork ID", QMessageBox.StandardButton.Ok
        )
