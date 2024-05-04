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
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl

from menu_bar import HelpDialog, MenuBar

# Constants
HOME_ICON_PATH = "../Images/home_icon.png"
URLCHIVE_ICON_PATH = "../Images/URLchive_3.png"
URLCHIVE_IMAGE_PATH = "../Images/URLchive_2.png"
URLCHIVE_URL = "https://urlchive.w3spaces.com"
EXIT_ICON_PATH = "../Images/exit_2.png"
HOW_TO_USE_ICON_PATH = "../Images/how_to_use.png"


class WebPage(QWebEngineView):
    def __init__(self, url, main_window):
        super().__init__()
        self.load(QUrl(url))
        self.main_window = main_window

    def showEvent(self, event):
        super().showEvent(event)
        self.main_window.setFixedSize(1150, 685)
        self.main_window.setGeometry(450, 300, 1150, 685)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.main_window.setFixedSize(600, 600)
        self.main_window.setGeometry(450, 300, 600, 600)


class HomePage(QWidget):
    def __init__(self, go_to_page_callback):
        super().__init__()

        self.go_to_page_callback = go_to_page_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel(self)
        pixmap = QPixmap(URLCHIVE_IMAGE_PATH)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)  # Ensure the image fits the label
        layout.addWidget(image_label)

        layout.addSpacing(50)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button())
        button_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(button_layout)

        # Load the font file and set the font for the button
        font_path = "../Fonts/Montserrat-Medium.ttf"  # Path to the font file
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 20)
        self.setFont(font)

    def create_button(self):
        button = QPushButton("Click Here To Start")
        # No need to set font here as it's already set in __init__
        button.setFixedSize(220, 50)
        button.clicked.connect(self.go_to_page_callback)

        # Apply style sheet to customize the button
        button.setStyleSheet("""
        QPushButton {
            background-color: #2c2c2c;
            border: none;
            color: white;
            padding: 2px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 20px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            border-radius: 12px;
        }
        
        QPushButton:hover {
            background-color: #161616;
            color: white;
        }
        
        QPushButton:pressed {
            background-color: #000000;
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
        self.setGeometry(650, 300, 600, 600)
        menubar = MenuBar(self)
        self.setMenuBar(menubar)

        self.setWindowIcon(QIcon(URLCHIVE_ICON_PATH))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Apply background color to the toolbar
        self.toolbar.setStyleSheet("background-color: #ffffff;")

        self.home_action = QAction(QIcon(HOME_ICON_PATH), "Home", self)
        self.home_action.setToolTip("Go to Home Page")
        self.home_action.triggered.connect(self.show_home_page)
        self.toolbar.addAction(self.home_action)

        self.toolbar.addSeparator()  # Separator after Home button

        self.how_to_use_action = QAction(
            QIcon(HOW_TO_USE_ICON_PATH), "How To Use", self
        )
        self.how_to_use_action.setToolTip("How To Use")
        self.how_to_use_action.triggered.connect(self.show_help_dialog)
        self.toolbar.addAction(self.how_to_use_action)

        self.toolbar.addSeparator()  # Separator after "How To Use" button

        self.exit_action = QAction(QIcon(EXIT_ICON_PATH), "Exit", self)
        self.exit_action.setToolTip("Exit Application")
        self.exit_action.triggered.connect(self.exit_application)
        self.toolbar.addAction(self.exit_action)

        self.home_page = HomePage(self.load_web_page)
        self.stacked_widget.addWidget(self.home_page)

        # Apply background color to the main window
        self.setStyleSheet("background-color: #e34105;")

    def load_web_page(self):
        web_page = WebPage(URLCHIVE_URL, self)
        self.stacked_widget.addWidget(web_page)
        self.stacked_widget.setCurrentWidget(web_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_help_dialog(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def exit_application(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
