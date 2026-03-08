import sys
import psutil
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont


class SpeedMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Internet Speed")
        self.setGeometry(100, 100, 160, 70)

        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout
        layout = QVBoxLayout()

        self.download_label = QLabel("↓ 0 KB/s")
        self.upload_label = QLabel("↑ 0 KB/s")

        font = QFont("Segoe UI", 10)

        self.download_label.setFont(font)
        self.upload_label.setFont(font)

        self.download_label.setAlignment(Qt.AlignCenter)
        self.upload_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.download_label)
        layout.addWidget(self.upload_label)

        self.setLayout(layout)

        # Style
        self.setStyleSheet("""
            QWidget{
                background-color: rgba(30,30,30,200);
                border-radius:10px;
                color:white;
            }
        """)

        # Network baseline
        self.old_data = psutil.net_io_counters()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

    def format_speed(self, bytes_per_sec):

        kb = bytes_per_sec / 1024

        if kb >= 1024:
            return f"{kb/1024:.2f} MB/s"
        else:
            return f"{kb:.1f} KB/s"

    def update_speed(self):
        new = psutil.net_io_counters()

        download = new.bytes_recv - self.old_data.bytes_recv
        upload = new.bytes_sent - self.old_data.bytes_sent

        self.download_label.setText(f"↓ {self.format_speed(download)}")
        self.upload_label.setText(f"↑ {self.format_speed(upload)}")

        self.old_data = new

    # Make widget draggable
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


app = QApplication(sys.argv)

window = SpeedMonitor()
window.show()

sys.exit(app.exec_())