from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


def make_sweep_widget(which='pow', parent=None, controller=None):
    if which == 'pow':
        return SweepWidget(parent=parent, controller=controller)
    elif which == 'freq':
        return SweepWidget(parent=parent, controller=controller)


class SweepWidget(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent)

        self._ui = uic.loadUi('sweepwidget.ui', self)
        self._controller = controller
