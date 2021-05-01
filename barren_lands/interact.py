import sys
import time
import pathlib
from PySide2.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QSpacerItem,
                               QSizePolicy, QLabel, QPlainTextEdit)
from PySide2.QtGui import Qt, QBrush, QColor, QIcon
from PySide2.QtCore import QRect

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
        self.hover = QBrush(QColor(90, 220, 90, 150), Qt.DiagCrossPattern)
        self.base = QBrush(QColor(90, 220, 90, 150), Qt.Dense5Pattern)

    def enterEvent(self, event):
        """Sets the corresponding rectangle's color to hove.

        Args:
            event (QEvent): The event handler.
        """
        self.rectangle.setBrush(self.hover)

    def leaveEvent(self, event):
        """Sets the corresponding rectangle's color back to default.

        Args:
            event (QEvent): The event handler.
        """
        self.rectangle.setBrush(self.base)


class BarrenLandsWindow(QMainWindow):
    """User interface to interact with the barren lands library."""
    def __init__(self, width=400, height=600):
        QMainWindow.__init__(self)
        self.app = QApplication.instance()
        self.resources = pathlib.Path(__file__).parent
        self.results = set()
        self.canvas_width = width
        self.canvas_height = height
        self.brush_barren = QBrush(QColor(10, 10, 10), Qt.Dense2Pattern)
        self.brush_fertile = QBrush(QColor(90, 220, 90, 150), Qt.Dense5Pattern)

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
            setting up scene:
                https://stackoverflow.com/questions/23174481/pyside-qt-layout-not-working
        """
        self.base_widget = QWidget(self)
        self.base_layout = QHBoxLayout(self.base_widget)
        # Setup the QGraphics items to display out zones as active elements.
        scene_zone = QRect(0, 0, self.canvas_width, self.canvas_height)
        self.scene = QGraphicsScene(scene_zone, self)
        self.canvas = QGraphicsView(self.scene, self)
        self.canvas.setFixedSize(self.canvas_width, self.canvas_height)

        self.base_layout.addWidget(self.canvas)
        # Set the core widget to the window
        self.setCentralWidget(self.base_widget)

    def build_controls(self):
        """Build the control panel that contains all the inputs."""
        self.controls = QWidget(self)
        self.controls_layout = QVBoxLayout(self.controls)
        # Initialize the text box for user input
        self.input = self.build_coord_input()
        # Create the buttons
        self.btn_add_bzone = BarrenButton(label="Add", parent=self, cmd=self.ctl_add_input)
        self.btn_run = BarrenButton(label="Analyze", parent=self, cmd=self.ctl_run)
        self.btn_reset = BarrenButton(label="Reset", parent=self, cmd=self.ctl_clear_zones)
        # Add a layout to hold all the results from the Analysis.
        self.result_layout = QVBoxLayout()
        # Add everything to the controls layout
        self.controls_layout.addLayout(self.input)
        self.controls_layout.addWidget(self.btn_add_bzone)
        self.controls_layout.addWidget(self.btn_run)
        self.controls_layout.addLayout(self.result_layout)
        self.controls_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.controls_layout.addWidget(self.btn_reset)
        # Add to the windows base layout.
        self.base_layout.addWidget(self.controls)

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
        # Format and draw the results in the QGraphicsScene.
        for zone in self.field.fertile_zones:
            rectangle = self.draw_zone(zone)
            self.results.add(ResultLabel(label=str(zone.get_size()),
                                         rectangle=rectangle, zone=zone))
            self.canvas.update()
            self.app.processEvents()
            # Dont show all at the same time. (For more pleasing visual)
            time.sleep(.025)

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
