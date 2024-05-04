import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QLabel,
    QAction,
    QToolBar,
    QHBoxLayout,
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui

from menu_bar import HelpDialog, MenuBar


class WebPage(QWebEngineView):
    def __init__(self, url, main_window):
        super().__init__()
        self.load(QUrl(url))
        self.main_window = main_window

    def showEvent(self, event):
        super().showEvent(event)
        self.main_window.setFixedSize(1150, 685)
        self.main_window.setGeometry(100, 38, 1150, 685)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.main_window.setFixedSize(600, 400)


class HomePage(QWidget):
    def __init__(self, go_to_page_callback):
        super().__init__()

        self.go_to_page_callback = go_to_page_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel(self)
        pixmap = QPixmap("../Images/URLchive_2.png")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  # Ensure the image fits the label
        layout.addWidget(image_label)

        layout.addSpacing(50)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button())
        button_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(button_layout)

    def create_button(self):
        button = QPushButton("Click Here To Start")
        button.setFont(QtGui.QFont("Arial", 12))
        button.setFixedSize(200, 50)
        button.clicked.connect(self.go_to_page_callback)

        # Apply style sheet to customize the button
        button.setStyleSheet("""
        QPushButton {
            background-color: #D3D3D3; /* Light Gray */
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            border-radius: 12px;
        }
        
        QPushButton:hover {
            background-color: #B0B0B0; /* Slightly Darker Gray */
            color: white;
        }
        
        QPushButton:pressed {
            background-color: #808080; /* Dark Gray */
            box-shadow: 0 5px #666;
            transform: translateY(4px);
        }
    """)

        return button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URLchive")
        self.setFixedSize(600, 600)
        menubar = MenuBar(self)
        self.setMenuBar(menubar)

        self.setWindowIcon(QIcon("../Images/URLchive_3.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Apply background color to the toolbar
        self.toolbar.setStyleSheet("background-color: #ffffff;")

        self.home_action = QAction(QIcon("../Images/home_icon.png"), "Home", self)
        self.home_action.triggered.connect(self.show_home_page)
        self.toolbar.addAction(self.home_action)

        self.home_page = HomePage(self.load_web_page)
        self.stacked_widget.addWidget(self.home_page)

        # Apply background color to the main window
        self.setStyleSheet("background-color: #e34105;")

    def load_web_page(self):
        url = "https://urlchive.w3spaces.com"
        web_page = WebPage(url, self)
        self.stacked_widget.addWidget(web_page)
        self.stacked_widget.setCurrentWidget(web_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_help_dialog(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
