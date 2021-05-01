import sys
import time
import pathlib
from PySide2.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QSpacerItem,
                               QSizePolicy, QLabel, QPlainTextEdit)
from PySide2.QtGui import Qt, QBrush, QColor
from PySide2.QtCore import QRect

from barren_lands import land, utils


class BarrenButton(QPushButton):

    def __init__(self, label, parent, cmd):
        QPushButton.__init__(self, label, parent)
        self.setCursor(Qt.PointingHandCursor)
        # Add the callback
        self.clicked.connect(cmd)


class BarrenLandsWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.app = QApplication.instance()
        self.resources = pathlib.Path(__file__).parent
        self.results = set()
        self.canvas_width = 400
        self.canvas_height = 600

        self.field = land.Field(width=self.canvas_width, height=self.canvas_height)
        self.barren_zones = list()
        self.fertile_zones = list()

        self.setup_window()
        self.build_core_ui()
        self.build_controls()
        self.build_connections()
        self.set_style()

    def setup_window(self):
        self.setWindowTitle("Barren Lands")
        self.setMinimumHeight(600)
        self.setMinimumWidth(700)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def build_core_ui(self):
        """
        setting up scene: https://stackoverflow.com/questions/23174481/pyside-qt-layout-not-working
        """
        self.base_widget = QWidget(self)
        self.base_layout = QHBoxLayout(self.base_widget)
        # Imagery
        scene_zone = QRect(0, 0, self.canvas_width, self.canvas_height)
        self.scene = QGraphicsScene(scene_zone, self)
        self.canvas = QGraphicsView(self.scene, self)
        self.canvas.setFixedSize(self.canvas_width, self.canvas_height)

        self.base_layout.addWidget(self.canvas)
        # Set the core widget to the window
        self.setCentralWidget(self.base_widget)

    def build_controls(self):
        self.controls = QWidget(self)
        self.controlls_layout = QVBoxLayout(self.controls)

        self.input = self.build_coord_input()
        self.btn_add_bzone = BarrenButton(label="Add", parent=self, cmd=self.ctl_add_input)
        self.btn_run = BarrenButton(label="Analyze", parent=self, cmd=self.ctl_run)
        self.btn_clear = BarrenButton(label="Reset", parent=self, cmd=self.ctl_clear_zones)

        self.result_layout = QVBoxLayout()

        self.controlls_layout.addLayout(self.input)
        self.controlls_layout.addWidget(self.btn_add_bzone)
        self.controlls_layout.addWidget(self.btn_run)
        self.controlls_layout.addLayout(self.result_layout)
        self.controlls_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.controlls_layout.addWidget(self.btn_clear)

        self.base_layout.addWidget(self.controls)

    def build_coord_input(self):
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        self.raw_input = QPlainTextEdit()
        self.raw_input.setMaximumHeight(75)
        self.raw_input.setPlaceholderText('example: "0 292 399 307"')
        self.input_layout = QVBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(self.raw_input)
        base_layout.addLayout(self.input_layout)
        return base_layout

    def build_connections(self):
        pass

    def ctl_add_input(self):
        raw_data = self.raw_input.toPlainText()
        if raw_data:
            parsed_input = utils.format_raw_input(raw_data)
            for input in parsed_input:
                start_coord = land.Coord(input[0], input[1])
                end_coord = land.Coord(input[2], input[3])
                zone = land.Zone(start_coord, end_coord)
                self.field.add_zone(zone, barren=True)
                self.draw_zone(zone, barren=True)

    def ctl_run(self):
        self.clear_results()
        for rectangle in self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()

        self.field.check_zones()
        for zone in self.field.fertile_zones:
            self.draw_zone(zone)
            self.canvas.update()
            self.app.processEvents()
            time.sleep(.025)
        for result in sorted([z.get_size() for z in self.field.fertile_zones]):
            label = QLabel(str(result))
            label.setAlignment(Qt.AlignHCenter)
            self.results.add(label)
            self.result_layout.addWidget(label)

    def ctl_clear_zones(self):
        for rectangle in self.barren_zones + self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()
        self.field.barren_zones = set()
        self.clear_results()

    def clear_results(self):
        for result in self.results:
            result.deleteLater()
        self.results = set()

    def draw_zone(self, zone, barren=False):
        new_rectangle = self.scene.addRect(zone.start.x, zone.start.y,
                                           zone.end.x - zone.start.x + 1,
                                           zone.end.y - zone.start.y + 1)
        if barren:
            self.barren_zones.append(new_rectangle)
            brush = QBrush(QColor(10, 10, 10), Qt.Dense2Pattern)
        else:
            self.fertile_zones.append(new_rectangle)
            brush = QBrush(QColor(90, 220, 90, 150), Qt.Dense5Pattern)

        new_rectangle.setBrush(brush)
        new_rectangle.setPen(Qt.NoPen)

    def set_style(self):
        style_sheet = self.resources.joinpath("resources", "style.css")
        with open(style_sheet, "r") as style_file:
            self.setStyleSheet(style_file.read())


if __name__ == "__main__":
    # Test the ui

    case_study_app = QApplication(sys.argv)

    window = BarrenLandsWindow()
    window.show()

    case_study_app.exec_()
    sys.exit(0)
