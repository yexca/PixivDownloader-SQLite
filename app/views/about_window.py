from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.description = QLabel()
        self.description.setText(
            """<p>Authoy: <a href="https://github.com/yexca">yexca</a> <br/>
            I just handled one error, it is lucky for normally running XD~<br/>
            For detals, please visit <a href="https://blog.yexca.net/en/archives/248/" rel="noopener">My Blog Page</a></p>"""
        )
        self.description.setOpenExternalLinks(True)  # Enable hyperlink functionality
        self.description.setWordWrap(True)  # Enable word wrapping
        self.description.setMaximumHeight(100)
        layout.addWidget(self.description)
        self.setLayout(layout)
