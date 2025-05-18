MAIN_STYLE = """

/* 全局禁用 focus 框 */
*:focus {
    outline: none;
}

/* 全局背景 */
QMainWindow {
    background-image: url();
    background-repeat: no-repeat;
    background-position: center;
} 

/* 半透明毛玻璃效果 */
QWidget {
    background: rgba(0, 0, 0, 0.2); /* 半透明黑色背景 */
    border-radius: 15px;           /* 圆角 */
    padding: 10px;                /* 内边距 */
    color: #ffffff;               /* 字体颜色 */
    font-family: "Comic Sans MS", "Arial", sans-serif; /* 可爱字体 */
    font-size: 16px;              /* 默认字体大小 */
}

/* 列表样式 */
QListWidget {
    background: rgba(0, 0, 0, 0.5); /* 毛玻璃效果 */
    border: 1px solid rgba(255, 255, 255, 0.2); /* 微光边框 */
    font-size: 16px;
    padding: 5px;
}

QListWidget::item {
    padding: 10px;
    border: none;
}

QListWidget::item:selected {
    border: none;
    background: rgba(255, 255, 255, 0.2); /* 选中效果 */
    color: #ffb6c1;                      /* 选中文本颜色 */
}

/* 标签样式 */
QLabel {
    font-size: 16px;
    color: #ffffff;
    margin: 5px;
    text-align: center;
}

/* 弹窗全局背景 */
QDialog {
    background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
    border-radius: 15px;           /* 圆角 */
    padding: 20px;                /* 内边距 */
    border: 1px solid rgba(255, 255, 255, 0.2); /* 微光边框 */
}

/* QMessageBox 全局样式 */
QMessageBox {
    background: rgba(0, 0, 0, 0.5);  /* 半透明背景 */
    border-radius: 10px;            /* 圆角 */
    border: 1px solid rgba(255, 255, 255, 0.3); /* 边框 */
    color: #ffffff;                /* 字体颜色 */
    font-size: 16px;               /* 字体大小 */
}

/* 弹窗内的按钮样式 */
QPushButton {
    background: rgba(255, 255, 255, 0.1); /* 半透明按钮背景 */
    border: 1px solid rgba(255, 255, 255, 0.3); /* 按钮边框 */
    color: #ffffff;
    padding: 8px 15px;
    border-radius: 10px;
    font-size: 14px;
}

QPushButton:hover {
    background: rgba(255, 255, 255, 0.2); /* 鼠标悬停效果 */
}

QPushButton:pressed {
    background: rgba(255, 255, 255, 0.3); /* 按钮按下效果 */
}

"""