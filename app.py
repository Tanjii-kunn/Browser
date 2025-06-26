from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
# from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor
import re

class Myweb_browser(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Myweb_browser, self).__init__(*args, **kwargs)

        self.setWindowTitle("Zeni Browser")
        self.setMinimumSize(1024, 768)

        # Layouts
        self.layout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        # URL bar
        self.url_bar = MyUrlBar()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setPlaceholderText("Enter URL here")
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.setStyleSheet("QLineEdit { padding: 5px; }")

        # Buttons
        self.go_button = QPushButton("➤")
        self.bk_button = QPushButton("←")
        self.fwd_button = QPushButton("→")
        self.refresh_button = QPushButton("⟳")
        self.new_tab_button = QPushButton("➕")

        for btn in [self.bk_button, self.fwd_button, self.refresh_button, self.go_button, self.new_tab_button]:
            btn.setFixedHeight(36)
            btn.setFixedWidth(36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add widgets to horizontal layout
        self.horizontalLayout.addWidget(self.bk_button)
        self.horizontalLayout.addWidget(self.fwd_button)
        self.horizontalLayout.addWidget(self.refresh_button)
        self.horizontalLayout.addWidget(self.url_bar)
        self.horizontalLayout.addWidget(self.new_tab_button)
        self.horizontalLayout.addWidget(self.go_button)

        # Browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://portfolio-web-teal-one.vercel.app/homepage.html"))

        # Add layouts
        self.layout.addLayout(self.horizontalLayout)
        self.layout.addWidget(self.browser)

        # Main layout set
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Logic-
        self.go_button.clicked.connect(self.navigate_to_url)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.bk_button.clicked.connect(self.browser.back)
        self.fwd_button.clicked.connect(self.browser.forward)
        self.refresh_button.clicked.connect(self.browser.reload)
        self.new_tab_button.clicked.connect(lambda: self.browser.setUrl(QUrl("https://portfolio-web-teal-one.vercel.app/homepage.html")))
        self.browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        self.browser.titleChanged.connect(self.setWindowTitle)
        self.go_button.setToolTip("Go to URL")
        self.bk_button.setToolTip("Back")
        self.new_tab_button.setToolTip("New Tab")
        self.fwd_button.setToolTip("Forward")
        self.refresh_button.setToolTip("Refresh")   
        self.url_bar.setToolTip("Enter URL and press Enter or click Go")
        self.browser.iconChanged.connect(self.update_window_icon)


        # Set initial window icon
        self.update_window_icon(QIcon("default.png"))
        self.browser.loadFinished.connect(self.handle_load_result)

        # Intercept requests for downloads
        self.browser.page().profile().downloadRequested.connect(self.handle_download)
    
    def handle_download(self , item):
        path = QFileDialog.getSaveFileName(None, "Save File", item.downloadFileName())[0]
        if path:
            item.setPath(path)
            item.accept()
        

        
    def handle_load_result(self, success):
            if not success:
                self.browser.setHtml("<h1>Failed to load page</h1>")

    def update_window_icon(self, icon):
        if not icon.isNull():
            self.setWindowIcon(icon)
        else:
            self.setWindowIcon(QIcon("web_browser/icons8-favicon-100.png"))


    @staticmethod
    def is_valid_url(url):
        pattern = re.compile(
            r"^(https?:\/\/)?(www\.)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}(\/\S*)?$"
        )
        return re.match(pattern, url)

    def smart_url_fix(self, raw):
        if self.is_valid_url(raw):
            return raw if raw.startswith("http") else "https://" + raw

        # If it's just a word, treat it as a search
        return f"https://www.google.com/search?q={raw}"

    def navigate_to_url(self):
        raw = self.url_bar.text()
        final_url = self.smart_url_fix(raw)
        self.browser.setUrl(QUrl(final_url))


class MyUrlBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)


    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.acceptProposedAction()

    def dropEvent(self, e):
        dropped = e.mimeData().text()
        self.setText(dropped)


import sys

app = QApplication(sys.argv)
window = Myweb_browser()
window.show()
app.exec()
