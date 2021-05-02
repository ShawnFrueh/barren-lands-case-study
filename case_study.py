import sys
import argparse
from barren_lands import land, utils

# Generate the arguments for the command line input.
parser = argparse.ArgumentParser(
    description="Generates a list of rectangular zones that do not enter the 'barron-zones'.")
parser.add_argument("--zones", type=str, nargs="+",
                    help="List of space-separated barren zones.\n"
                         "example input: '0 292 351 207'\n"
                         "example multi input: '48 192 351 207' '48 392 351 407'")
parser.add_argument("--width", type=int, default=400,
                    help="The width of the available land for zoning.")
parser.add_argument("--height", type=int, default=600,
                    help="The height of the available land for zoning.")
parser.add_argument("--vis", dest="vis", action="store_true",
                    help="Render the zones into an image and display it.")
parser.add_argument("--gui", dest="gui", action="store_true",
                    help="Opens the GUI for visual feedback.")
BARREN_DATA = parser.parse_args()


if __name__ == "__main__":

    if BARREN_DATA.gui:
        from PySide2.QtWidgets import QApplication
        from barren_lands.interact import BarrenLandsWindow
        # Initialize the Qt Application
        case_study_app = QApplication(sys.argv)
        # Initialize the window
        window = BarrenLandsWindow(width=BARREN_DATA.width, height=BARREN_DATA.height)
        # Display the UI
        window.show()
        # Kickstart the application
        case_study_app.exec_()
        sys.exit(0)
    else:

        # Generate the initial field in which the barron zones are placed.
        Field = land.Field(BARREN_DATA.width, BARREN_DATA.height)
        # Add all zones from the command line into the field.
        for barren_coord in BARREN_DATA.zones:
            barren_zone = utils.format_input(barren_coord)
            Field.add_zone(barren_zone, barren=True)

        # Run the tool to find the rectangular zones.
        Field.check_zones()

        if BARREN_DATA.vis:
            # Create and display an image of the data.
            Field.display()

        # Return the zone areas sorted from least to most surface area.
        print(sorted([zone.get_size() for zone in Field.fertile_zones]))
