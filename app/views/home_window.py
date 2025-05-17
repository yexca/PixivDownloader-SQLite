from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
)
from app.threads.download_threads import DownloadThread

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 画师 ID
        self.userID_label = QLabel("画师 ID:")
        self.userID_input = QLineEdit()

        # 作品 ID
        self.illustID_label = QLabel("作品 ID:")
        self.illustID_input = QLineEdit()

        # Button
        self.button = QPushButton("开始")
        self.button.clicked.connect(self.startDownload)

        userID_layout = QHBoxLayout()
        userID_layout.addWidget(self.userID_label)
        userID_layout.addWidget(self.userID_input)
        layout.addLayout(userID_layout)

        illustID_layout = QHBoxLayout()
        illustID_layout.addWidget(self.illustID_label)
        illustID_layout.addWidget(self.illustID_input)
        layout.addLayout(illustID_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def startDownload(self):
        try:
            self.button.setEnabled(False)
            self.button.setText("验证输入中")
            # 判断输入
            if self.userID_input.text() or self.illustID_input.text():
                self.thread = DownloadThread(self.userID_input.text(), self.illustID_input.text())
                self.thread.progress.connect(self.update_button)
                self.thread.finished.connect(self.task_finished)
                self.thread.start()
            else:
                self.show_warn()
        except Exception as e:
            print(f"Error in startDownload: {e}")
            self.button.setEnabled(True)
            self.button.setText("开始")
            QMessageBox.warning(self, "信息提示", "查询画师出错，请检查输入是否正确", QMessageBox.StandardButton.Ok)

    def update_button(self, info):
        self.button.setText(info)

    def task_finished(self):
        QMessageBox.information(self, "信息提示", "下载完成！", QMessageBox.StandardButton.Ok)
        self.button.setEnabled(True)
        self.button.setText("开始")
    def show_warn(self):
        QMessageBox.warning(self, "信息提示", "未输入", QMessageBox.StandardButton.Ok)
