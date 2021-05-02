import sys
import time
import random
import pathlib
from PySide2.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QSpacerItem,
                               QSizePolicy, QLabel, QPlainTextEdit, QGroupBox)
from PySide2.QtGui import Qt, QBrush, QColor, QIcon, QPen
from PySide2.QtCore import QRect, QRectF

from barren_lands import land, utils


class BarrenButton(QPushButton):
    """Custom button class to make sure all buttons are the same."""

    def __init__(self, label, parent, cmd):
        """Initialization of the BarrenButton.

        Args:
            label (str): Text to display on the button.
            parent (QWidget): Parent widget.
            cmd (callback): Method to call once clicked.
        """
        QPushButton.__init__(self, label, parent)
        self.setCursor(Qt.PointingHandCursor)
        # Add the callback
        self.clicked.connect(cmd)


class ResultLabel(QLabel):
    """Custom label to help visualize the zone this result comes from."""

    def __init__(self, label, rectangle, zone, parent=None):
        """Initialization fo the ResultLabel.

        Args:
            label (str): Text to display on the label.
            rectangle (QGraphicsItem): The rectangle that is within the canvas.
            zone (Zone): The zone data.
            parent (QWidget): Parent widget.
        """
        QLabel.__init__(self, label, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(20)
        self.rectangle = rectangle
        self.zone = zone
        self.hover_pen = QPen(QColor(120, 220, 120))
        self.base_pen = Qt.NoPen

    def enterEvent(self, event):
        """Sets the corresponding rectangle's color to hove.

        Args:
            event (QEvent): The event handler.
        """
        self.rectangle.setPen(self.hover_pen)

    def leaveEvent(self, event):
        """Sets the corresponding rectangle's color back to default.

        Args:
            event (QEvent): The event handler.
        """
        self.rectangle.setPen(self.base_pen)


class BarrenLandsWindow(QMainWindow):
    """User interface to interact with the barren lands library."""

    def __init__(self, width=400, height=600):
        QMainWindow.__init__(self)
        self.app = QApplication.instance()
        self.resources = pathlib.Path(__file__).parent
        self.results = set()
        self.canvas_width = width
        self.canvas_height = height
        # Colors for drawing onto the QGraphicsScene
        self.brush_barren = QBrush(QColor(120, 120, 75), Qt.Dense2Pattern)
        self.brush_overlay = QBrush(QColor(20, 20, 20, 35), Qt.SolidPattern)
        self.brush_innerlay = QBrush(QColor(32, 37, 44), Qt.SolidPattern)
        self.brush_fertile = QBrush(QColor(90, 220, 90, 150), Qt.Dense5Pattern)

        # Setup the filed class that will handle our calculations.
        self.field = land.Field(width=self.canvas_width, height=self.canvas_height)
        self.barren_zones = list()
        self.fertile_zones = list()

        self.setup_window()
        self.build_core_ui()
        self.build_controls()

    def setup_window(self):
        """Setup all the window related settings/flags."""
        self.setWindowTitle("Barren Lands")
        self.setMinimumHeight(600)
        self.setMinimumWidth(700)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(utils.get_icon()))
        self.setStyleSheet(utils.get_css())

    def build_core_ui(self):
        """Sets up the core elements of this window.

        Notes:
            Setting up QGraphicsScene:
                https://stackoverflow.com/questions/23174481/pyside-qt-layout-not-working
        """
        self.base_widget = QWidget(self)
        self.base_layout = QHBoxLayout(self.base_widget)
        # Setup the QGraphics items to display out zones as active elements.
        scene_zone = QRect(0, 0, self.canvas_width, self.canvas_height)
        self.scene = QGraphicsScene(scene_zone, self)
        self.canvas = QGraphicsView(self.scene, self)
        self.canvas.setFixedSize(self.canvas_width, self.canvas_height)
        # Draw faint bullseye for target.
        self.scene.addEllipse(self.get_center_rect(300), Qt.NoPen, self.brush_overlay)
        self.scene.addEllipse(self.get_center_rect(200), Qt.NoPen, self.brush_innerlay)
        self.scene.addEllipse(self.get_center_rect(100), Qt.NoPen, self.brush_overlay)
        self.base_layout.addWidget(self.canvas)
        # Set the core widget to the window.
        self.setCentralWidget(self.base_widget)

    def get_center_rect(self, size):
        """Generates a QRect that is at the center of the canvas and it's width/height set to size.

        Args:
            size (int): The size to set the bounds to.

        Returns:
            (QRectF): A rectangle coordinate that is center on the canvas with a given size.
        """
        return QRectF(self.canvas_width * 0.5 - (size * 0.5),
                      self.canvas_height * 0.5 - (size * 0.5), size, size)

    def build_controls(self):
        """Build the control panel that contains all the inputs."""
        self.controls = QWidget(self)
        self.controls_layout = QVBoxLayout(self.controls)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        # Initialize the text box for user input
        self.input = self.build_coord_input()
        # Create the buttons
        self.btn_add_bzone = BarrenButton(label="Add", parent=self, cmd=self.ctl_add_input)
        self.btn_run = BarrenButton(label="Analyze", parent=self, cmd=self.ctl_run)
        # Build the utility buttons
        self.btm_layout = QHBoxLayout()
        self.btm_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_reset = BarrenButton(label="Reset", parent=self, cmd=self.ctl_clear_zones)
        self.btn_debug = BarrenButton(label="Debug", parent=self, cmd=self.ctr_debug)
        self.btm_layout.addWidget(self.btn_debug)
        self.btm_layout.addWidget(self.btn_reset)
        self.results_grp = self.build_results_group()
        # Add everything to the controls layout
        self.controls_layout.addLayout(self.input)
        self.controls_layout.addWidget(self.btn_add_bzone)
        self.controls_layout.addWidget(self.btn_run)
        self.controls_layout.addWidget(self.results_grp)
        self.controls_layout.addLayout(self.btm_layout)
        # Add to the windows base layout.
        self.base_layout.addWidget(self.controls)

    def build_results_group(self):
        """Build the results group to contain the results of analysis.

        Returns:
            results_grp (QGroupBox): The group box that contains the results layout.
        """
        results_grp = QGroupBox("results")
        results_grp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Add a layout to hold all the results from the Analysis.
        self.result_layout = QVBoxLayout()
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        results_grp.setLayout(self.result_layout)
        return results_grp

    def build_coord_input(self):
        """Build the necessary elements for the user input text box.

        Returns:
            (QVBoxLayout): The base layout of the coord input.
        """
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

    def ctr_debug(self):
        """CONTROL: Called by the 'debug' button to randomly assign colors to the zones."""
        for result in self.results:
            rand_color = [random.randint(0, 255) for i in range(3)]
            rand_color = QColor(*rand_color)
            brush = QBrush(rand_color, Qt.Dense5Pattern)
            result.rectangle.setBrush(brush)
            result.base = brush

    def ctl_add_input(self):
        """CONTROL: Called by the 'Add' button to handle parsing the raw input."""
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
        """CONTROL: Called by the 'Run' button to initialize the final analysis."""
        # Make sure some values are cleared ahead of the analysis.
        self.clear_results()
        for rectangle in self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()

        # Run the analysis
        self.field.check_zones()
        total_area = 0
        # Format and draw the results in the QGraphicsScene.
        for zone in self.field.fertile_zones:
            rectangle = self.draw_zone(zone)
            size = zone.get_size()
            self.results.add(ResultLabel(label=str(size), rectangle=rectangle, zone=zone))
            self.canvas.update()
            self.app.processEvents()
            # Dont show all at the same time. (For more pleasing visual)
            time.sleep(.025)
            total_area += size
        print(total_area)

        # Sort the results by their zones area.
        for result in sorted(self.results, key=lambda x: x.zone.get_size()):
            # Add the result to the results layout in the UI
            self.result_layout.addWidget(result)

    def ctl_clear_zones(self):
        """CONTROL: Called by the 'Reset' button to handle resetting the data and graphics."""
        for rectangle in self.barren_zones + self.fertile_zones:
            self.scene.removeItem(rectangle)
        self.field.fertile_zones = set()
        self.fertile_zones = list()
        self.field.barren_zones = set()
        self.barren_zones = list()
        self.clear_results()

    def clear_results(self):
        """Clears the results set in preparation for incoming new results."""
        for result in self.results:
            result.deleteLater()
        self.results = set()

    def draw_zone(self, zone, barren=False):
        """

        Args:
            zone:
            barren (bool): barren colors if True else fertile color.

        Returns:
            (QGraphicsRecItem): The drown rectangle that is added to the canvas.
        """
        # Build the QGraphicsRecItem from the zone data.
        rectangle = self.scene.addRect(zone.start.x, zone.start.y,
                                       zone.end.x - zone.start.x + 1,
                                       zone.end.y - zone.start.y + 1)
        if barren:
            self.barren_zones.append(rectangle)
            brush = self.brush_barren
        else:
            self.fertile_zones.append(rectangle)
            brush = self.brush_fertile
        # Apply the color to the rectangle item.
        rectangle.setBrush(brush)
        # Remove the default border
        rectangle.setPen(Qt.NoPen)
        return rectangle


if __name__ == "__main__":
    # Test the ui

    case_study_app = QApplication(sys.argv)

    window = BarrenLandsWindow()
    window.show()

    case_study_app.exec_()
    sys.exit(0)
