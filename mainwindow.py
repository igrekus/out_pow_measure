from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QModelIndex

from instrumentcontroller import InstrumentController
from connectionwidget import ConnectionWidget
from measuremodel import MeasureModel
from measurewidget import MeasureWidgetWithSecondaryParameters
from primaryplotwidget import PrimaryPlotWidget
from sweepwidget import SweepWidget, make_sweep_widget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)
        self._instrumentController = InstrumentController(parent=self)
        self._connectionWidget = ConnectionWidget(parent=self, controller=self._instrumentController)
        self._measureWidget = MeasureWidgetWithSecondaryParameters(parent=self, controller=self._instrumentController)
        self._powSweepWidget = make_sweep_widget('pow', parent=self, controller=self._instrumentController)
        self._freqSweepWidget = make_sweep_widget('freq', parent=self, controller=self._instrumentController)

        self._measureModel = MeasureModel(parent=self, controller=self._instrumentController)

        # init UI
        self._ui.layInstrs.insertWidget(0, self._connectionWidget)
        self._ui.layInstrs.insertWidget(1, self._measureWidget)
        self._ui.tabWidget.insertTab(0, self._powSweepWidget, 'По мощности')
        self._ui.tabWidget.insertTab(1, self._freqSweepWidget, 'По частоте')
        self._ui.tabWidget.setCurrentIndex(0)

        self._init()

    def _init(self):
        self._connectionWidget.connected.connect(self.on_instrumens_connected)
        self._connectionWidget.connected.connect(self._measureWidget.on_instrumentsConnected)

        self._measureWidget.secondaryChanged.connect(self._instrumentController.on_secondary_changed)

        self._measureWidget.measureComplete.connect(self._measureModel.update)
        self._measureWidget.measureComplete.connect(self.on_measureComplete)

        self._powSweepWidget.paramsChanged.connect(self.on_paramsChanged)
        self._freqSweepWidget.paramsChanged.connect(self.on_paramsChanged)

        self._powSweepWidget.tabResult.setModel(self._measureModel)
        self._freqSweepWidget.tabResult.setModel(self._measureModel)

        self.refreshView()

    # UI utility methods
    def refreshView(self):
        self.resizeTable()

    def resizeTable(self):
        pass
        # self._ui.tableMeasure.resizeRowsToContents()
        # self._ui.tableMeasure.resizeColumnsToContents()

    # event handlers
    def resizeEvent(self, event):
        self.refreshView()

    @pyqtSlot()
    def on_instrumens_connected(self):
        print(f'connected {self._instrumentController}')

    @pyqtSlot()
    def on_measureComplete(self):
        print('meas complete')
        # self._plotWidget.plot()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        self._instrumentController.sweepType = index
        self._instrumentController.secondaryParams = self._ui.tabWidget.currentWidget().params

    @pyqtSlot()
    def on_paramsChanged(self):
        self._instrumentController.secondaryParams = self._ui.tabWidget.currentWidget().params
