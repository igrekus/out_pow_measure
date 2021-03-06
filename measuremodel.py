from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant


class MeasureModel(QAbstractTableModel):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)

        self._controller = controller

        self._data = list()
        self._headers = list()

        self._init()

    def _init(self):
        self._initHeader()

    def _initHeader(self):
        self.beginResetModel()
        if self._controller.result:
            self._headers = self._controller.result.headers
        self.endResetModel()

    def update(self):
        self._init()
        self.beginResetModel()
        self._data = self._controller.result.data
        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        try:
            return len(self._controller.result.data)
        except AttributeError:
            return 0

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if col == 0:
                return QVariant(row + 1)
            else:
                return QVariant(self._data[row][col - 1])

        return QVariant()
