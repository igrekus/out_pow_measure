from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


def make_sweep_widget(which='pow', parent=None, controller=None):
    if which == 'pow':
        return PowSweepWidget(parent=parent, controller=controller)
    elif which == 'freq':
        return FreqSweepWidget(parent=parent, controller=controller)


class SweepWidget(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent)

        self._ui = uic.loadUi('sweepwidget.ui', self)
        self._controller = controller


class PowSweepWidget(SweepWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent, controller=controller)

        self._ui.lblParam.setText('F=')
        self._ui.spinParam.setSuffix(' ГГц')
        self._ui.spinParam.setMinimum(0)
        self._ui.spinParam.setMaximum(50)
        self._ui.spinParam.setValue(1)

        self._ui.lblSecMin.setText('Pmin=')
        self._ui.spinSecMin.setSuffix(' дБ')
        self._ui.spinSecMin.setMinimum(-30)
        self._ui.spinSecMin.setMaximum(20)
        self._ui.spinSecMin.setValue(-20)

        self._ui.lblSecMax.setText('Pmax=')
        self._ui.spinSecMax.setSuffix(' дБ')
        self._ui.spinSecMax.setMinimum(-30)
        self._ui.spinSecMax.setMaximum(20)
        self._ui.spinSecMax.setValue(0)

        self._ui.lblSecStep.setText('Pstep=')
        self._ui.spinSecStep.setSuffix(' дБ')
        self._ui.spinSecStep.setMinimum(0)
        self._ui.spinSecStep.setMaximum(10)
        self._ui.spinSecStep.setValue(0.1)


class FreqSweepWidget(SweepWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent, controller=controller)

        self._ui.lblParam.setText('P=')
        self._ui.spinParam.setSuffix(' дБ')
        self._ui.spinParam.setMinimum(-30)
        self._ui.spinParam.setMaximum(50)
        self._ui.spinParam.setValue(-20)

        self._ui.lblSecMin.setText('Fmin=')
        self._ui.spinSecMin.setSuffix(' ГГц')
        self._ui.spinSecMin.setMinimum(0)
        self._ui.spinSecMin.setMaximum(50)
        self._ui.spinSecMin.setValue(1)

        self._ui.lblSecMax.setText('Fmax=')
        self._ui.spinSecMax.setSuffix(' ГГц')
        self._ui.spinSecMax.setMinimum(0)
        self._ui.spinSecMax.setMaximum(500)
        self._ui.spinSecMax.setValue(4)

        self._ui.lblSecStep.setText('Pstep=')
        self._ui.spinSecStep.setSuffix(' ГГц')
        self._ui.spinSecStep.setMinimum(0)
        self._ui.spinSecStep.setMaximum(10)
        self._ui.spinSecStep.setValue(0.1)

