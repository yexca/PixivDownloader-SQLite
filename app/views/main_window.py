from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QListWidget, QMainWindow, QSplitter, QStackedWidget

# from app.views.pixiv_auth_window import PixivAuthWindow
from app.controllers.main_controller import MainController
from app.views.about_window import AboutWindow
from app.views.home_window import HomeWindow
from app.views.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = MainController()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(self.controller.get_icon()))
        self.setWindowTitle("PixivDownloader By yexca v1.1")
        # self.setFixedSize(1280, 720)  # 设置窗口大小
        # self.resize(1280, 720)
        screen = QApplication.primaryScreen()
        dpi_scaling = screen.devicePixelRatio()

        scaled_width = int(1280 / dpi_scaling)
        scaled_height = int(720 / dpi_scaling)
        self.resize(scaled_width, scaled_height)

        # 创建 Splitter
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(0)  # 把分隔线宽度设为 0

        # 左侧菜单栏
        self.menu_list = QListWidget()
        self.menu_list.addItem("Home")
        # self.menu_list.addItem("Pixiv 验证")
        self.menu_list.addItem("Sttings")
        self.menu_list.addItem("About")
        self.menu_list.currentRowChanged.connect(self.change_page)

        # 右侧内容区
        self.stacked_widget = QStackedWidget()

        # 添加页面
        self.stacked_widget.addWidget(HomeWindow())
        # self.stacked_widget.addWidget(PixivAuthWindow())
        self.stacked_widget.addWidget(SettingsWindow())
        self.stacked_widget.addWidget(AboutWindow())

        # 布局
        splitter.addWidget(self.menu_list)
        splitter.addWidget(self.stacked_widget)
        splitter.setStretchFactor(1, 4)

        self.setCentralWidget(splitter)
        self.menu_list.setCurrentRow(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        # pixmap = QPixmap(os.getcwd() + "\\app\\resources\\images\\background.png")
        pixmap = QPixmap(self.controller.get_background_image())
        painter.drawPixmap(self.rect(), pixmap)

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
