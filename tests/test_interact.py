import sys
import pytest
from PySide2.QtWidgets import QApplication

from barren_lands.interact import BarrenLandsWindow


class TestGUI:
    app = QApplication(sys.argv)
    # Initialize the window with a small field for faster testing.
    window = BarrenLandsWindow(width=5, height=5)

    def test_setup(self):
        assert self.window.windowTitle() == "Barren Lands"

    def test_raw_input(self):
        # Make sure that the raw input results in a barren zone
        self.window.raw_input.setPlainText('"0 3 5 3"')
        # 'click' the Add button.
        self.window.btn_add_bzone.click()

        assert len(self.window.barren_zones) == 1

    def test_run(self):
        # Test running the analysis and check results.
        # 'click' the Run button
        self.window.btn_run.click()

        assert len(self.window.fertile_zones) == 2

    def test_clear(self):
        # Make sure the reset, clears out all of the required data.
        # 'click' the Reset button
        self.window.btn_reset.click()

        assert len(self.window.fertile_zones) == 0
        assert len(self.window.barren_zones) == 0
        assert len(self.window.field.barren_zones) == 0
        assert len(self.window.field.fertile_zones) == 0
