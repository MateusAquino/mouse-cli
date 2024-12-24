import re
import sys
import argparse
import pyautogui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QCursor
from PyQt5.QtWidgets import QApplication, QWidget


class Overlay(QWidget):
    def __init__(self, args):
        super().__init__()

        # Set the window to fullscreen
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)

        # Variables
        self.background_color = args.background_color
        self.exclude_numbers = args.exclude_numbers
        self.scroll_factor = args.scroll_factor
        self.active_color = args.active_color
        self.one_by_one = args.one_by_one
        self.opacity = args.opacity
        self.button = args.button
        self.color = args.color
        self.font = args.font
        self.size = args.size
        self.view = args.view
        self.active = None
        self.setWindowOpacity(args.opacity)

        # Set transparency and make the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(args.opacity)
        self.setWindowTitle("Mouse Overlay")

        # Request focus for the window
        self.activateWindow()
        self.raise_()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Escape, Qt.Key_Delete]:
            self.close()
        elif event.key() == Qt.Key_Backspace and self.active == None:
            self.close()
        elif event.key() == Qt.Key_Backspace:
            self.active = None
            self.update()
        elif event.key() == Qt.Key_Space:
            self.setWindowOpacity(1)
        elif event.key() in range(48, 58) or event.key() in range(65, 91):
            if self.active == None and self.x_map.get(chr(event.key())):
                self.active = chr(event.key())
                self.update()
            elif self.active != None and self.y_map.get(chr(event.key())):
                x_pos = self.x_map.get(self.active)
                y_pos = self.y_map.get(chr(event.key()))
                self.hide()
                if self.button != "drag":
                    pyautogui.moveTo(x_pos, y_pos)
                if self.button == "left":
                    pyautogui.click(button="left")
                elif self.button == "right":
                    pyautogui.click(button="right")
                elif self.button == "middle":
                    pyautogui.click(button="middle")
                elif self.button == "double":
                    pyautogui.doubleClick()
                elif self.button == "scroll":
                    pyautogui.scroll(self.scroll_factor)
                elif self.button == "drag":
                    pyautogui.mouseDown()
                    pyautogui.moveTo(x_pos, y_pos)
                    pyautogui.mouseUp()
                self.close()

    def keyReleaseEvent(self, a0):
        if a0.key() == Qt.Key_Space:
            self.setWindowOpacity(self.opacity)
        return super().keyReleaseEvent(a0)

    def paintEvent(self, event):
        # Create QPainter object to draw lines
        painter = QPainter(self)
        painter.eraseRect(self.rect())
        painter.setRenderHint(QPainter.Antialiasing)

        # Set line color and width
        primary_color = qcolor_parser(self.color)
        active_color = qcolor_parser(self.active_color)
        background_color = qcolor_parser(self.background_color)
        painter.fillRect(self.rect(), background_color)
        painter.setPen(primary_color)
        painter.setFont(QFont(self.font, self.size))

        # Divide the window into lines
        numbers = [chr(i) for i in range(48, 58)]
        letters = [chr(i) for i in range(65, 91)]
        chars_y = letters if self.exclude_numbers in ["all", "y"] else letters + numbers
        chars_x = letters if self.exclude_numbers in ["all", "x"] else letters + numbers
        screen_height = self.height()
        screen_width = self.width()
        line_height = screen_height // len(chars_y)
        line_width = screen_width // len(chars_x)
        real_line_height = screen_height / len(chars_y)
        real_line_width = screen_width / len(chars_x)
        self.x_map = {
            char: int((i + 0.5) * real_line_width) for i, char in enumerate(chars_x)
        }
        self.y_map = {
            char: int((i + 0.5) * real_line_height) for i, char in enumerate(chars_y)
        }

        if (self.one_by_one and self.active == None) or not self.one_by_one:
            for i, char in enumerate(chars_y):
                y_position = int(i * real_line_height)
                painter.drawLine(0, y_position, self.width(), y_position)
                if self.active == char:
                    painter.setPen(active_color)
                if self.view == "cartesian":
                    painter.drawText(
                        QRect(0, y_position, line_width, line_height),
                        Qt.AlignCenter,
                        char,
                    )
                elif self.view == "cross":
                    painter.drawText(
                        QRect(screen_width // 2, y_position, line_width, line_height),
                        Qt.AlignCenter,
                        char,
                    )
                painter.setPen(primary_color)
        if (self.one_by_one and self.active != None) or not self.one_by_one:
            for i, char in enumerate(chars_x):
                x_position = int(i * real_line_width)
                painter.drawLine(x_position, 0, x_position, self.height())
                if self.view == "cartesian":
                    painter.drawText(
                        QRect(x_position, 0, line_width, line_height),
                        Qt.AlignCenter,
                        char,
                    )
                elif self.view == "cross":
                    painter.drawText(
                        QRect(x_position, screen_height // 2, line_width, line_height),
                        Qt.AlignCenter,
                        char,
                    )
        if self.view == "grid":
            for i, xChar in enumerate(chars_x):
                for j, yChar in enumerate(chars_y):
                    x_position = int(i * real_line_width)
                    y_position = int(j * real_line_height)

                    if self.active == xChar:
                        painter.setPen(active_color)
                    painter.drawText(
                        QRect(x_position, y_position, line_width, line_height),
                        Qt.AlignCenter,
                        (
                            f"{xChar} {yChar}"
                            if not self.one_by_one
                            else (xChar if self.active == None else yChar)
                        ),
                    )
                    painter.setPen(primary_color)


def qcolor_parser(hex):
    hex = hex[1:] if hex[0] == "#" else hex
    hex = hex[0:1] * 2 + hex[1:2] * 2 + hex[2:3] * 2 if len(hex) == 3 else hex
    hex = (
        hex[0:1] * 2 + hex[1:2] * 2 + hex[2:3] * 2 + hex[3:4] * 2
        if len(hex) == 4
        else hex
    )
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    a = int(hex[6:8], 16) if len(hex) > 6 else 127
    return QColor(r, g, b, a)


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % (x,))
    return x


def hex_parser(arg_value, pat=re.compile(r"^#?[a-f0-9A-F]{3,8}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("invalid hex value")
    return arg_value


def parse_args():
    parser = argparse.ArgumentParser(
        description="Overlay application with adjustable line count."
    )
    parser.add_argument(
        "--exclude-numbers",
        "-en",
        help="Number of lines to divide the screen into.",
        choices=["none", "all", "x", "y"],
        default="none",
    )
    parser.add_argument(
        "--opacity",
        "-o",
        type=restricted_float,
        help="Opacity of the overlay window.",
        default=0.45,
    )
    parser.add_argument(
        "--view",
        "-v",
        help="Define rows and columns view.",
        choices=["grid", "cartesian", "cross"],
        default="grid",
    )
    parser.add_argument(
        "--one-by-one",
        "-obo",
        help="Show only one prompt (row/column) at a time.",
        action="store_const",
        default=False,
        const=not (False),
    )
    parser.add_argument(
        "--color",
        "-c",
        type=hex_parser,
        help="Change default primary color.",
        default="#FFFD007F",
    )
    parser.add_argument(
        "--active-color",
        "-ac",
        type=hex_parser,
        help="Change default active color.",
        default="#FF0000FF",
    )
    parser.add_argument(
        "--background-color",
        "-bc",
        type=hex_parser,
        help="Change default background color.",
        default="#000000FF",
    )
    parser.add_argument(
        "--font", "-f", help="Change default font family.", default="Arial"
    )
    parser.add_argument(
        "--size", "-s", type=int, help="Change default font size.", default="16"
    )
    parser.add_argument(
        "--button",
        "-b",
        help="Mouse button to trigger from the overlay.",
        choices=["left", "right", "middle", "double", "move", "drag", "scroll"],
        default="left",
    )
    parser.add_argument(
        "--use-current-position",
        "-p",
        help="Instantly triggers the action using the current mouse position instead of the overlay.",
        action="store_const",
        default=False,
        const=not (False),
    )
    parser.add_argument(
        "--scroll-factor",
        "-sf",
        type=int,
        help="Change default scroll factor.",
        default="1",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.use_current_position:
        position = pyautogui.position()

        if args.button == "drag":
            pyautogui.mouseDown()
            pyautogui.moveTo(position)
            pyautogui.mouseUp()
        else:
            pyautogui.moveTo(position)
            if args.button == "left":
                pyautogui.click(button="left")
            elif args.button == "right":
                pyautogui.click(button="right")
            elif args.button == "middle":
                pyautogui.click(button="middle")
            elif args.button == "double":
                pyautogui.doubleClick()
            elif args.button == "scroll":
                pyautogui.scroll(args.scroll_factor)

    else:
        app = QApplication(sys.argv)

        overlay = Overlay(args)
        overlay.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
