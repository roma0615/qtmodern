from os.path import join, dirname, abspath

from qtpy.QtCore import Qt, QMetaObject, Signal, Slot
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                            QLabel, QSizePolicy, QSpacerItem, QDesktopWidget, QMessageBox,
                            QFrame)
from PyQt5 import QtGui, QtCore

from ._utils import QT_VERSION

_FL_STYLESHEET = ':/resources/frameless.qss'
""" str: Frameless window stylesheet. """


def print_args(*args):
    for a in args:
        print(a)

class WindowDragger(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    doubleClicked = Signal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(self._windowPos +
                              (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, w, parent=None, logo=None, resize=True, osx_buttons=False):
        QWidget.__init__(self, parent)
        self.resizable = resize

        self.setupUi(logo, osx_buttons)
        self.setupEvents(w)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())

        if not resize:
            self.setFixedSize(self.size())

        # Center
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setupUi(self, logo, osx_buttons):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Fixed))

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        if logo is not None:
            self.logoLbl = QLabel()
            pixmap = QtGui.QPixmap(logo)
            self.logoLbl.setScaledContents(True)
            self.logoLbl.setPixmap(pixmap)
            self.logoLbl.setMaximumSize(QtCore.QSize(30, 30))
            if osx_buttons:
                self.logoLbl.setContentsMargins(0, 3, 3, 0)
            else:
                self.logoLbl.setContentsMargins(3, 3, 0, 0)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setStyleSheet('QLabel { color: #bbb; }')
        self.lblTitle.setContentsMargins(10, 0, 0, 0)
        self.lblTitle.setAlignment(Qt.AlignCenter)


        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)

        if self.resizable:
            self.btnRestore = QToolButton(self.titleBar)
            self.btnRestore.setObjectName('btnRestore')
            self.btnRestore.setSizePolicy(spButtons)
            self.btnRestore.setVisible(False)

            self.btnMaximize = QToolButton(self.titleBar)
            self.btnMaximize.setObjectName('btnMaximize')
            self.btnMaximize.setSizePolicy(spButtons)

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)


        # Add everything to hboxTitle
        if osx_buttons:
            self.hboxTitle.addItem(QSpacerItem(4, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
            m = [10]*4
            self.btnClose.setContentsMargins(*m)
            self.btnMinimize.setContentsMargins(*m)

            self.hboxTitle.addWidget(self.btnClose)
            self.hboxTitle.addWidget(self.btnMinimize)
            
            if self.resizable:
                self.btnRestore.setContentsMargins(*m)
                self.btnMaximize.setContentsMargins(*m)

                self.hboxTitle.addWidget(self.btnRestore)
                self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.lblTitle)
            self.hboxTitle.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            if logo is not None:
                self.hboxTitle.addWidget(self.logoLbl)

        else:
            if logo is not None:
                self.hboxTitle.addWidget(self.logoLbl)
            self.hboxTitle.addWidget(self.lblTitle)
            self.hboxTitle.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.hboxTitle.addWidget(self.btnMinimize)
            if self.resizable:
                self.hboxTitle.addWidget(self.btnMaximize)
                self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnClose)

            self.hboxTitle.setAlignment(self.btnClose, Qt.AlignTop)
            self.hboxTitle.setAlignment(self.btnMinimize, Qt.AlignTop)
            if self.resizable:
                self.hboxTitle.setAlignment(self.btnRestore, Qt.AlignTop)
                self.hboxTitle.setAlignment(self.btnMaximize, Qt.AlignTop)



        # set window flags
        self.setWindowFlags(
                Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        if QT_VERSION >= (5,):
            self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        # with open(_FL_STYLESHEET) as stylesheet:
        #     self.setStyleSheet(stylesheet.read())
        stream = QtCore.QFile(_FL_STYLESHEET)
        stream.open(QtCore.QIODevice.ReadOnly)
        _FL_TITLEBAR_BUTTONS = ':/resources/windows_titlebar.qss'
        if osx_buttons:
            _FL_TITLEBAR_BUTTONS = ':/resources/osx_titlebar.qss'
        stream2 = QtCore.QFile(_FL_TITLEBAR_BUTTONS)
        stream2.open(QtCore.QIODevice.ReadOnly)

        bytestream = QtCore.QTextStream(stream).readAll()
        print(bytestream)
        bytestream += QtCore.QTextStream(stream2).readAll()

        self.setStyleSheet(bytestream)

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def setupEvents(self, w):
        w.close = self.close
        self.closeEvent = w.closeEvent

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        self.lblTitle.setText(title)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)
        print('Minimized clicked')

    @Slot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)
        print('Restore clicked')

    @Slot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        self.btnMaximize.setVisible(False)

        # self.setWindowState(Qt.WindowMaximized)
        self.showMaximized()
        print('Maximized clicked')

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if self.btnMaximize.isVisible():
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()
