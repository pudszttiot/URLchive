import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel, QAction, QToolBar, QHBoxLayout
from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui

class WebPage(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.load(QUrl(url))

class HomePage(QWidget):
    def __init__(self, go_to_page_callback):
        super().__init__()

        self.go_to_page_callback = go_to_page_callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Aligns everything in the center vertically

        image_label = QLabel(self)
        movie = QMovie("URLchive.gif")
        image_label.setMovie(movie)
        movie.start()

        layout.addWidget(image_label)  # No need for explicit alignment here

        layout.addSpacing(50)  # Add spacing between the GIF and the button

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_centered())  # Create and add the button
        button_layout.setAlignment(Qt.AlignCenter)  # Aligns the button in the center horizontally

        layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.setLayout(layout)

    def button_centered(self):
        button = QPushButton("Click Here To Start")
        button.setFont(QtGui.QFont("Arial", 16))
        button.setFixedSize(200, 50)
        button.clicked.connect(self.go_to_page_callback)  # Connect the button's click event here
        return button

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URLchive")
        self.setGeometry(100, 100, 600, 400)

        # Set the application icon for the taskbar
        self.setWindowIcon(QIcon("URL.ico"))  # Replace with the actual path to your icon file

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.home_action = QAction(QIcon("home_icon.png"), "Home", self)  # Replace with the actual path to your image
        self.home_action.triggered.connect(self.show_home_page)
        self.toolbar.addAction(self.home_action)

        self.home_page = HomePage(self.load_web_page)
        self.stacked_widget.addWidget(self.home_page)

    def load_web_page(self):
        url = "https://urlchive.w3spaces.com/"  # Replace with your desired URL
        web_page = WebPage(url)
        self.stacked_widget.addWidget(web_page)
        self.stacked_widget.setCurrentWidget(web_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
