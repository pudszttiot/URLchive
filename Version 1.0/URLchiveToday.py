import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,  # Use QGridLayout instead of QHBoxLayout
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

def open_webview():
    """
    Function to open a web view of the website and handle file downloads.
    """
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    webview = QWebEngineView()
    loading_label = QLabel("Loading, please wait...")  # Create a loading label

    # Apply a zoom factor to make the text smaller (0.8 means 80% of the original size)
    webview.setZoomFactor(0.8)

    # Function to hide the loading label when the page is fully loaded
    def hide_loading_label():
        loading_label.hide()

    # Create a custom download handler
    def download_requested(download):
        # Prompt the user to choose the download path
        save_path, _ = QFileDialog.getSaveFileName(window, "Save File", os.path.expanduser("~"), "All Files (*.*)")
        if save_path:
            download.setPath(save_path)
            download.accept()

    # Set the custom download handler for the web view
    profile = QWebEngineProfile.defaultProfile()
    profile.downloadRequested.connect(download_requested)

    webview.loadFinished.connect(hide_loading_label)  # Connect the hide_loading_label function to the loadFinished signal

    webview.load(QUrl('https://archive.md'))

    layout.addWidget(webview)
    layout.addWidget(loading_label)  # Add the loading label to the layout

    window.setCentralWidget(central_widget)
    window.setWindowTitle('URLchive Today')
    window.setGeometry(100, 100, 550, 350)

    # Set the window icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'G:\Software\py\Python Creations\Completed\Projects')
    window.setWindowIcon(QIcon(icon_path))

    # Apply a custom stylesheet for a cool and modern look
    with open("style.qss", "r") as style_file:
        window.setStyleSheet(style_file.read())

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    window.setCentralWidget(central_widget)
    window.setWindowTitle('URLchive Today')
    window.setGeometry(100, 100, 300, 260)  # Reduced the window height to fit the gifs more closely

    # Set the window icon (Icon path is updated to use a valid icon file)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
    window.setWindowIcon(QIcon(icon_path))

    # Apply a custom stylesheet for a cool and modern look
    with open("style.qss", "r") as style_file:
        window.setStyleSheet(style_file.read())

    # Create a grid layout to reduce spacing between the gifs
    grid_layout = QGridLayout()
    layout.addLayout(grid_layout)

    # Add the title heading .gif image using QMovie
    image_label = QLabel()
    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example1.gif')
    movie = QMovie(gif_path)
    
    # Set the desired scaled size for the title heading .gif image (adjust width and height as needed)
    scaled_width = 350
    scaled_height = 110
    movie.setScaledSize(movie.currentImage().size().scaled(scaled_width, scaled_height, Qt.KeepAspectRatio))
    
    image_label.setMovie(movie)
    movie.start()

    grid_layout.addWidget(image_label, 0, 0, alignment=Qt.AlignHCenter)  # Added alignment to center the label horizontally

    # Add the search animation .gif image using QMovie
    image_label = QLabel()
    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.gif')
    movie = QMovie(gif_path)
    
    # Set the desired scaled size for the search animation .gif image (adjust width and height as needed)
    scaled_width = 700
    scaled_height = 60
    movie.setScaledSize(movie.currentImage().size().scaled(scaled_width, scaled_height, Qt.KeepAspectRatio))
    
    image_label.setMovie(movie)
    movie.start()

    grid_layout.addWidget(image_label, 1, 0, alignment=Qt.AlignHCenter)  # Added alignment to center the label horizontally

    # Add the button below the centered gifs
    button = QPushButton('Click here to start URLchive Today')
    button.clicked.connect(open_webview)
    layout.addWidget(button, alignment=Qt.AlignHCenter)  # Added alignment to center the button horizontally

    window.show()
