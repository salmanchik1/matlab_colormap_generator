import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QLinearGradient
from PySide6.QtCore import Qt


class GradientBar(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        gradient = QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, Qt.red)
        gradient.setColorAt(0.5, Qt.green)
        gradient.setColorAt(1, Qt.blue)

        painter.fillRect(rect, gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gradient_bar = GradientBar()
    gradient_bar.resize(300, 30)
    gradient_bar.show()
    sys.exit(app.exec_())
