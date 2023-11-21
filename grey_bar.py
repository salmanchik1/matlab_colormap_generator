import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QColorDialog, QLineEdit, QMessageBox, QPushButton
from PySide6.QtGui import QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt, Signal


class GradientBar(QWidget):
    def __init__(self):
        super().__init__()
        rect = self.rect()

        self.gradient_colors = []
        self.gradient = QLinearGradient(rect.topLeft(), rect.topRight())

    def set_gradient_colors(self, gradient_colors):
        self.gradient_colors = gradient_colors
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        self.gradient = QLinearGradient(rect.topLeft(), rect.topRight())

        for position, color in self.gradient_colors:
            self.gradient.setColorAt(position, color)

        painter.fillRect(rect, self.gradient)
        painter.end()

    def interpolate_color(self, gradient, position):
        stops = gradient.stops()
        start_position, start_color = stops[0]
        end_position, end_color = stops[-1]
        if len(stops) < 1:
            return QColor()
        if start_position > position:
            interpolated_color = QColor(
                int(start_color.red()),
                int(start_color.green()),
                int(start_color.blue())
            )
            return interpolated_color
        if end_position < position:
            interpolated_color = QColor(
                int(end_color.red()),
                int(end_color.green()),
                int(end_color.blue())
            )
            return interpolated_color
        for i in range(len(stops) - 1):
            start_position, start_color = stops[i]
            end_position, end_color = stops[i + 1]

            if start_position <= position <= end_position:
                alpha = (position - start_position) / (end_position - start_position)
                interpolated_color = QColor(
                    int((1 - alpha) * start_color.red() + alpha * end_color.red()),
                    int((1 - alpha) * start_color.green() + alpha * end_color.green()),
                    int((1 - alpha) * start_color.blue() + alpha * end_color.blue())
                )
                return interpolated_color


        return QColor()  # Return a default color if all conditions are false


class ColoredBar(QWidget):
    colorChanged = Signal(list)  # Signal emitted when color changes

    def __init__(self, gradient_bar, matlab_line_edit):
        super().__init__()

        self.gradient_bar = gradient_bar
        self.matlab_line_edit = matlab_line_edit
        self.cell_states = [False] * 64  # Initial state: All cells unpicked

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.cells = []
        for _ in range(64):
            cell = QLabel(self)
            cell.setFixedSize(20, 50)  # Adjust the size as needed
            cell.setAlignment(Qt.AlignCenter)
            cell.setStyleSheet("background-color: gray;")
            cell.mousePressEvent = lambda event, cell=cell: self.handle_mouse_press(event, cell)
            layout.addWidget(cell)
            self.cells.append(cell)

        self.setLayout(layout)

    def handle_mouse_press(self, event, cell):
        index = self.cells.index(cell)

        if event.button() == Qt.LeftButton:
            self.show_color_dialog(cell, index)
        elif event.button() == Qt.RightButton:
            self.remove_color(cell, index)

    def show_color_dialog(self, cell, index):
        color_dialog = QColorDialog(self)
        current_color = cell.palette().color(cell.backgroundRole())
        color_dialog.setCurrentColor(current_color)

        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            cell.setStyleSheet(f"background-color: {selected_color.name()};")
            cell.setToolTip(f"Selected Color: {selected_color.name()}")
            self.cell_states[index] = True
            self.colorChanged.emit(self.get_colors())
            self.update_matlab_line_edit()

    def remove_color(self, cell, index):
        cell.setStyleSheet("background-color: gray;")
        cell.setToolTip("Color Removed")
        self.cell_states[index] = False
        self.colorChanged.emit(self.get_colors())
        self.update_matlab_line_edit()

    def get_matlab_colors(self):
        colors = []
        for i_cell, cell in enumerate(self.cells):
            position = i_cell / len(self.cells)
            color = self.gradient_bar.interpolate_color(self.gradient_bar.gradient, position)
            colors.append((position, color))
        return colors

    def get_colors(self):
        return [(cell.pos().x() / self.width(), cell.palette().color(cell.backgroundRole())) for cell, picked in zip(self.cells, self.cell_states) if picked]

    def update_matlab_line_edit(self):
        colormap_str = "[" + "; ".join([f"{color.redF():.4f} {color.greenF():.4f} {color.blueF():.4f}" for _, color in self.get_matlab_colors()]) + "]"
        self.matlab_line_edit.setText(colormap_str)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        gradient_bar = GradientBar()
        self.matlab_line_edit = QLineEdit(self)
        self.matlab_line_edit.setReadOnly(True)

        colored_bar = ColoredBar(gradient_bar, self.matlab_line_edit)
        colored_bar.colorChanged.connect(gradient_bar.set_gradient_colors)
        copy_button = QPushButton('Copy to Clipboard', self)

        # Connect the button to the copy function
        copy_button.clicked.connect(self.copy_to_clipboard)

        layout.addWidget(gradient_bar)
        layout.addWidget(colored_bar)
        layout.addWidget(self.matlab_line_edit)
        layout.addWidget(copy_button)

        self.setLayout(layout)
        self.setWindowTitle('Gradient Color Picker')
        self.setGeometry(100, 100, 700, 200)  # Adjust the geometry as needed

    def copy_to_clipboard(self):
        # Get the text from the edit field
        text_to_copy = self.matlab_line_edit.text()

        # Check if there's text to copy
        if text_to_copy:
            # Copy text to clipboard
            QApplication.clipboard().setText(text_to_copy)
            QMessageBox.information(self, 'Copied', 'Content copied to clipboard.')
        else:
            QMessageBox.warning(self, 'Empty Field', 'The edit field is empty.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

