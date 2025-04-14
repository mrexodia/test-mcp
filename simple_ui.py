import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
import argparse
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Display a simple dialog with title and content.")
    parser.add_argument("--title", required=True, help="The title of the dialog.")
    parser.add_argument("--content", required=True, help="The content of the dialog.")
    parser.add_argument("--timeout", type=int, default=0, help="The timeout in seconds before the application closes automatically. Default is 0 (infinite).")
    args = parser.parse_args()

    # Create the application
    app = QApplication([])

    # Corrected to set the application icon in the dock
    app.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))

    # Create the dialog
    dialog = QDialog()
    dialog.setWindowTitle(args.title)
    dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlag(Qt.Dialog)
    dialog.setFocusPolicy(Qt.StrongFocus)
    dialog.setModal(True)

    # Remove maximize button on macOS by setting appropriate window flags
    dialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

    # Set the window icon to SP_MessageBoxInformation style standard icon
    dialog.setWindowIcon(dialog.style().standardIcon(QStyle.SP_MessageBoxInformation))

    # Set up the layout
    layout = QVBoxLayout()
    label = QLabel()
    label.setWordWrap(True)

    # Set the label to support rich text
    label.setTextFormat(Qt.RichText)
    label.setText(args.content)

    layout.addWidget(label)

    # Add a close button
    close_button = QPushButton("Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    dialog.setLayout(layout)

    # Set the default size of the dialog and fix the width
    dialog.setFixedWidth(400)

    # Show the dialog
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()

    dialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
    dialog.adjustSize()

    # If a timeout is specified, set a timer to close the application
    if args.timeout > 0:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(args.timeout * 1000, app.quit)

    # Execute the application
    app.exec()
    sys.exit(0)