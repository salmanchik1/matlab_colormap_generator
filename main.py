from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QSlider, QTextEdit
from PySide6.QtGui import QValidator
from PySide6.QtCore import Qt


class ColormapGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Colormap Generator")

        # Color scale
        self.color_scale = QSlider()
        self.color_scale.setOrientation(Qt.Horizontal)
        self.color_scale.setRange(0, 100)
        self.color_scale.setValue(50)
        self.color_scale.valueChanged.connect(self.update_colormap)

        # Color anchors
        self.color_anchors_label = QLabel("Color Anchors:")
        self.color_anchors = QLineEdit("0.25, 0.5, 0.75")
        self.color_anchors.setValidator(FloatListValidator())
        self.color_anchors.textChanged.connect(self.update_colormap)

        # Generate button
        self.generate_button = QPushButton("Generate Colormap")
        self.generate_button.clicked.connect(self.update_colormap)

        # Generated colormap text
        self.generated_text_label = QLabel("Generated Colormap:")
        self.generated_text = QTextEdit()
        self.generated_text.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.color_scale)
        layout.addWidget(self.color_anchors_label)
        layout.addWidget(self.color_anchors)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.generated_text_label)
        layout.addWidget(self.generated_text)

        self.setLayout(layout)

        # Initial update
        self.update_colormap()


    def update_colormap(self):
        base_color = self.color_scale.value() / 100
        anchors = [float(anchor) for anchor in self.color_anchors.text().split(', ')]

        # Generate colormap
        colormap = []
        for anchor in anchors:
            colormap.append([base_color * anchor, base_color, 1.0000])
        colormap.extend([[1.0000, 1.0000, 1.0000], [1.0000, base_color, base_color]])

        # Display colormap in the text window
        self.generated_text.clear()
        for color in colormap:
            self.generated_text.append(f"{color[0]:.4f}, {color[1]:.4f}, {color[2]:.4f}")


class FloatListValidator(QValidator):
    def validate(self, input_str, pos):
        try:
            [float(val) for val in input_str.split(', ')]
            return QValidator.Acceptable, pos
        except ValueError:
            return QValidator.Invalid, pos


if __name__ == "__main__":
    app = QApplication([])
    colormap_app = ColormapGeneratorApp()
    colormap_app.show()
    app.exec_()
