from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

G = 1_000_000_000
M = 1_000_000
K = 1_000

GHz = G


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
        self._labelUnit = ''

    @property
    def params(self):
        raise NotImplementedError

    @pyqtSlot(float)
    def on_spinParam_valueChanged(self, value):
        self._ui.editFile.setText(f'{value}_{self._labelUnit}')


class PowSweepWidget(SweepWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent, controller=controller)
        self._labelUnit = 'ГГц'

        self._ui.lblParam.setText('F=')
        self._ui.spinParam.setSuffix(' ГГц')
        self._ui.spinParam.setMinimum(0)
        self._ui.spinParam.setMaximum(50)
        self._ui.spinParam.setValue(1)

        self._ui.lblSecMin.setText('Pмин=')
        self._ui.spinSecMin.setSuffix(' дБ')
        self._ui.spinSecMin.setMinimum(-30)
        self._ui.spinSecMin.setMaximum(20)
        self._ui.spinSecMin.setValue(-10)

        self._ui.lblSecMax.setText('Pмакс=')
        self._ui.spinSecMax.setSuffix(' дБ')
        self._ui.spinSecMax.setMinimum(-30)
        self._ui.spinSecMax.setMaximum(20)
        self._ui.spinSecMax.setValue(0)

        self._ui.lblSecStep.setText('Pшаг=')
        self._ui.spinSecStep.setSuffix(' дБ')
        self._ui.spinSecStep.setMinimum(0)
        self._ui.spinSecStep.setMaximum(10)
        self._ui.spinSecStep.setValue(1)

    @property
    def params(self):
        return {
            'F': self._ui.spinParam.value() * GHz,
            'Pmin': self._ui.spinSecMin.value(),
            'Pmax': self._ui.spinSecMax.value(),
            'Pstep': self._ui.spinSecStep.value()
        }


class FreqSweepWidget(SweepWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent, controller=controller)
        self._labelUnit = 'дБ'

        self._ui.lblParam.setText('P=')
        self._ui.spinParam.setSuffix(' дБ')
        self._ui.spinParam.setMinimum(-30)
        self._ui.spinParam.setMaximum(50)
        self._ui.spinParam.setValue(-20)

        self._ui.lblSecMin.setText('Fмин=')
        self._ui.spinSecMin.setSuffix(' ГГц')
        self._ui.spinSecMin.setMinimum(0)
        self._ui.spinSecMin.setMaximum(50)
        self._ui.spinSecMin.setValue(1)

        self._ui.lblSecMax.setText('Fмакс=')
        self._ui.spinSecMax.setSuffix(' ГГц')
        self._ui.spinSecMax.setMinimum(0)
        self._ui.spinSecMax.setMaximum(500)
        self._ui.spinSecMax.setValue(4)

        self._ui.lblSecStep.setText('Fшаг=')
        self._ui.spinSecStep.setSuffix(' ГГц')
        self._ui.spinSecStep.setMinimum(0)
        self._ui.spinSecStep.setMaximum(10)
        self._ui.spinSecStep.setValue(0.5)

    @property
    def params(self):
        return {
            'P': self._ui.spinParam.value(),
            'Fmin': self._ui.spinSecMin.value() * GHz,
            'Fmax': self._ui.spinSecMax.value() * GHz,
            'Fstep': self._ui.spinSecStep.value() * GHz
        }
