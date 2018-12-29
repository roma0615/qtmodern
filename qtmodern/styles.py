from os.path import join, dirname, abspath

from qtpy.QtGui import QPalette, QColor
from PyQt5 import QtCore

from ._utils import QT_VERSION

_STYLESHEET = ':/resources/style.qss'
""" str: Main stylesheet. """


def _apply_base_theme(app):
    """ Apply base theme to the application.

        Args:
            app (QApplication): QApplication instance.
    """

    if QT_VERSION < (5,):
        app.setStyle('plastique')
    else:
        app.setStyle('Fusion')

    stream = QtCore.QFile(_STYLESHEET)
    stream.open(QtCore.QIODevice.ReadOnly)
    app.setStyleSheet(QtCore.QTextStream(stream).readAll())


def dark(app):
    """ Apply Dark Theme to the Qt application instance.

        Args:
            app (QApplication): QApplication instance.
    """

    _apply_base_theme(app)

    darkPalette = QPalette()

    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53));
    darkPalette.setColor(QPalette.WindowText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127));
    darkPalette.setColor(QPalette.Base, QColor(42, 42, 42));
    darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66));
    darkPalette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255));
    darkPalette.setColor(QPalette.ToolTipText, QColor(53, 53, 53));
    darkPalette.setColor(QPalette.Text, QColor(255, 255, 255));
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127));
    darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35));
    darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20));
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53));
    darkPalette.setColor(QPalette.ButtonText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127));
    darkPalette.setColor(QPalette.BrightText, QColor(255, 0, 0));
    darkPalette.setColor(QPalette.Link, QColor(42, 130, 218));
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218));
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80));
    darkPalette.setColor(QPalette.HighlightedText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127));

    app.setPalette(darkPalette)
