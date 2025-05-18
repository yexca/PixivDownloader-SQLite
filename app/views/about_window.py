from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.description = QLabel()
        self.description.setText(
            """<p>作者: <a href="https://github.com/yexca">yexca</a> <br/>
            就做了一个错误处理，能不能运行看运气吧~<br/>
            具体请访问 <a href="https://blog.yexca.net/archives/248" rel="noopener">https://blog.yexca.net/archives/248</a>
             查看吧</p>"""
        )
        self.description.setOpenExternalLinks(True)  # Enable hyperlink functionality
        self.description.setWordWrap(True)  # Enable word wrapping
        self.description.setMaximumHeight(100)
        layout.addWidget(self.description)
        self.setLayout(layout)
