import sys
from PySide2.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QSpacerItem,
                               QSizePolicy, QSpinBox)
from PySide2.QtGui import Qt, QBrush, QColor

from barren_lands import land, utils


class CaseStudyWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.canvas_width = 400
        self.canvas_height = 600

        self.field = land.Field(width=self.canvas_width, height=self.canvas_height)
        self.barren_zones = list()
        self.fertile_zones = list()

        self.setup_window()
        self.build_core_ui()
        self.build_controls()
        self.build_connections()

    def setup_window(self):
        self.setWindowTitle("Barren Lands")
        self.setMinimumHeight(600)
        self.setMinimumWidth(700)

    def build_core_ui(self):
        """
        setting up scene: https://stackoverflow.com/questions/23174481/pyside-qt-layout-not-working
        """
        self.base_widget = QWidget(self)
        self.base_layout = QHBoxLayout(self.base_widget)
        # Imagery
        self.scene = QGraphicsScene()
        self.canvas = QGraphicsView(self.scene, self)
        self.canvas.setFixedSize(self.canvas_width + 1, self.canvas_height + 1)

        self.base_layout.addWidget(self.canvas)
        # Set the core widget to the window
        self.setCentralWidget(self.base_widget)

    def build_controls(self):
        self.controls = QWidget(self)
        self.controlls_layout = QVBoxLayout(self.controls)

        # self.input = QLineEdit(self)
        # self.input.setPlaceholderText('"48 192 351 207" "48 392 351 407"')
        self.input = self.build_coord_input()
        self.btn_add_bzone = QPushButton(text="Add", parent=self)
        self.btn_run = QPushButton(text="Run", parent=self)
        self.btn_clear = QPushButton(text="Clear", parent=self)

        self.controlls_layout.addLayout(self.input)
        self.controlls_layout.addWidget(self.btn_add_bzone)
        self.controlls_layout.addWidget(self.btn_run)
        self.controlls_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.controlls_layout.addWidget(self.btn_clear)

        self.base_layout.addWidget(self.controls)

    def build_coord_input(self):
        layout = QHBoxLayout()
        self.input_a = QSpinBox()
        self.input_aa = QSpinBox()
        self.input_b = QSpinBox()
        self.input_bb = QSpinBox()
        for coord in (self.input_a, self.input_aa, self.input_b, self.input_bb):
            coord.setMaximum(self.canvas_height)
            layout.addWidget(coord)
        return layout

    def build_connections(self):
        self.btn_add_bzone.clicked.connect(self.ctl_add_input)
        self.btn_clear.clicked.connect(self.ctl_clear_zones)
        self.btn_run.clicked.connect(self.ctl_run)

    def ctl_add_input(self):
        # input_data = self.input.text().strip().split('" "')
        start_coord = land.Coord(self.input_a.value(), self.input_aa.value())
        end_coord = land.Coord(self.input_b.value(), self.input_bb.value())
        zone = land.Zone(start_coord, end_coord)
        self.field.add_zone(zone, barren=True)
        new_rectangle = self.scene.addRect(zone.start.x, zone.start.y,
                                               zone.end.x - zone.start.x,
                                               zone.end.y - zone.start.y)
        new_rectangle.setBrush(QBrush(QColor(120, 30, 30), Qt.SolidPattern))
        new_rectangle.setPen(Qt.NoPen)
        self.barren_zones.append(new_rectangle)

    def ctl_run(self):
        for rectangle in self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()

        self.field.check_zones()
        for zone in self.field.fertile_zones:
            new_rectangle = self.scene.addRect(zone.start.x, zone.start.y,
                                               zone.end.x - zone.start.x,
                                               zone.end.y - zone.start.y)
            new_rectangle.setBrush(QBrush(QColor(120, 220, 30), Qt.SolidPattern))
            new_rectangle.setPen(Qt.NoPen)
            self.fertile_zones.append(new_rectangle)

    def ctl_clear_zones(self):
        for rectangle in self.barren_zones + self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()
        self.field.barren_zones = set()


if __name__ == "__main__":
    # Test the ui

    case_study_app = QApplication(sys.argv)

    window = CaseStudyWindow()
    window.show()

    case_study_app.exec_()
    sys.exit(0)
