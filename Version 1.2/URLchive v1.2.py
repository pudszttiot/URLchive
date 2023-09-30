import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel, QAction, QToolBar, QHBoxLayout, QMenu, QMenuBar, QDialog
from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui

class WebPage(QWebEngineView):
    def __init__(self, url, main_window):
        super().__init__()
        self.load(QUrl(url))
        self.main_window = main_window

    def showEvent(self, event):
        super().showEvent(event)
        # When the web page is shown, update the window size
        self.main_window.setFixedSize(1150, 685)  # Adjust the size as needed
        self.main_window.setGeometry(100, 38, 1150, 685)

    def hideEvent(self, event):
        super().hideEvent(event)
        # When hiding the web page, restore the previous window size
        self.main_window.setFixedSize(600, 400)

class HomePage(QWidget):
    def __init__(self, go_to_page_callback):
        super().__init__()

        self.go_to_page_callback = go_to_page_callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Aligns everything in the center vertically

        image_label = QLabel(self)
        movie = QMovie(r"..\Images\URLchive.gif")
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

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("How to Use")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon(r"..\Images\URL.ico"))

        help_text = """
         <h2>Welcome to URLchive</h2>

        <p><strong>URLchive</strong> is a web page archiving tool that allows you to save and organize web pages for later reference.</p>

        <h3>Getting Started</h3>

        <ol>
            <li>Click the "Click Here To Start" button on the home page to go to the URLchive web app.</li>
            <li>In the URLchive web app, you can enter the URL of the web page you want to archive in the address bar and click the "Archive" button to save the page.</li>
            <li>You can view your archived pages by clicking the "View Archive" button in the app.</li>
        </ol>

        <h3>Archiving a Web Page</h3>

        <p>Follow these steps to archive a web page:</p>

        <ol>
            <li>Go to the URLchive web app by clicking the "Click Here To Start" button.</li>
            <li>In the app, you will see an address bar. Enter the URL of the web page you want to archive (e.g., https://example.com).</li>
            <li>Click the "Archive" button to save the page. The archived page will be stored for later reference.</li>
        </ol>

        <h3>Viewing Archived Pages</h3>

        <p>To view your archived pages:</p>

        <ol>
            <li>Click the "View Archive" button in the app. You will see a list of all the web pages you have archived.</li>
            <li>Click on a page in the list to view it. You can navigate through the archived pages using the navigation controls.</li>
        </ol>

        <h3>Exiting the Application</h3>

        <p>To exit the URLchive application:</p>

        <ol>
            <li>Click the "File" menu in the menu bar.</li>
            <li>Select "Exit." The application will close.</li>
        </ol>

        <p>Thank you for using URLchive!</p>
        """

        help_label = QLabel()
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setText(help_text)

        layout = QVBoxLayout()
        layout.addWidget(help_label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URLchive")
        self.setFixedSize(600, 400)

        # Set the application icon for the taskbar
        self.setWindowIcon(QIcon(r"..\Images\URL.ico"))  # Replace with the actual path to your icon file

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.home_action = QAction(QIcon(r"..\Images\home_icon.png"), "Home", self)  # Replace with the actual path to your image
        self.home_action.triggered.connect(self.show_home_page)
        self.toolbar.addAction(self.home_action)

        self.home_page = HomePage(self.load_web_page)
        self.stacked_widget.addWidget(self.home_page)

        # Create a menu bar
        menubar = self.menuBar()

        # Create a "File" menu
        file_menu = menubar.addMenu("File")

        # Create an "Exit" action under the "File" menu
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create a "Help" menu
        help_menu = menubar.addMenu("Help")

        # Create a "How to Use" action under the "Help" menu
        how_to_use_action = QAction("How to Use", self)
        how_to_use_action.triggered.connect(self.show_help_dialog)
        help_menu.addAction(how_to_use_action)

    def load_web_page(self):
        url = "https://urlchive.w3spaces.com/"  # Replace with your desired URL
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
