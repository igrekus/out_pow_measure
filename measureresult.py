import datetime

import openpyxl


class MeasureResult:
    def __init__(self, raw_data, suffix=''):
        self._xlsx_fn = suffix
        self._title_str = 'abs title'
        self._raw_data = raw_data
        self.headers = list()
        self._processed_data = list()

    def process(self):
        raise NotImplementedError

    @property
    def data(self):
        return self._processed_data

    @property
    def xlsx_filename(self):
        return f'{self._xlsx_fn}_{datetime.datetime.now().isoformat().replace(":","-")}.xlsx'

    def save_xlsx(self):
        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append([self.headers[0]] + self.headers[2:])
        ws.append([self._title_str])
        for i, row in enumerate(self.data):
            ws.append([i + 1] + row[1:])

        wb.save(self.xlsx_filename)


class PowSweepResult(MeasureResult):
    def __init__(self, raw_data, suffix=''):
        super().__init__(raw_data, suffix=suffix)
        self.headers = ['#', 'F', 'Pвх, дБ', 'Pвых, дБ']

        self.process()
        self.save_xlsx()

    def process(self):
        print(self.xlsx_filename)
        self._processed_data = list(self._raw_data)
        self._title_str = f'F = {self.data[0][0] / 1_000_000_000} ГГц'


class FreqSweepResult(MeasureResult):
    def __init__(self, raw_data, suffix=''):
        super().__init__(raw_data, suffix=suffix)
        self.headers = ['#', 'Pвх', 'F, ГГц', 'Pвых, дБ']

        self.process()
        self.save_xlsx()

    def process(self):
        print(self.xlsx_filename)
        self._processed_data = list(self._raw_data)
        self._title_str = f'P = {self.data[0][0]} дБ'

