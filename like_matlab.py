import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSlider
from PySide6.QtGui import QPixmap, QLinearGradient, QColor, QPainter
from PySide6.QtCore import Qt


class GradientEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a QGraphicsScene and QGraphicsView
        scene = QGraphicsScene()
        view = QGraphicsView(scene)
        layout.addWidget(view)

        # Create a gradient with default stops
        self.gradient_stops = [(0.0, Qt.red), (0.5, Qt.green), (1.0, Qt.blue)]

        # Create a pixmap to display the gradient
        pixmap = self.generate_gradient_pixmap()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # Create a slider to adjust the color stops
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.valueChanged.connect(self.update_gradient)

        layout.addWidget(slider)

        self.setLayout(layout)
        self.setWindowTitle('Gradient Editor')
        self.setGeometry(100, 100, 400, 200)

    def generate_gradient_pixmap(self):
        pixmap_width = 400
        pixmap_height = 50

        pixmap = QPixmap(pixmap_width, pixmap_height)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        gradient_rect = pixmap.rect()

        gradient = QLinearGradient(gradient_rect.topLeft(), gradient_rect.topRight())

        for position, color in self.gradient_stops:
            gradient.setColorAt(position, color)

        painter.fillRect(gradient_rect, gradient)
        painter.end()

        return pixmap

    def update_gradient(self, value):
        # Update the gradient stops based on the slider value
        position = value / 100.0
        stop = (position, QColor(255, 255, 255))
        self.gradient_stops = [(0.0, Qt.red), stop, (1.0, Qt.blue)]

        # Update the displayed pixmap
        pixmap = self.generate_gradient_pixmap()
        pixmap_item = self.findChild(QGraphicsPixmapItem)
        pixmap_item.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = GradientEditor()
    editor.show()
    sys.exit(app.exec())


