import datetime


class MeasureResult:
    def __init__(self, raw_data):
        self._xlsx_fn = 'abs'
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
        return f'{self._xlsx_fn}_{datetime.datetime.now().isoformat()}.xlsx'

class PowSweepResult(MeasureResult):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self._xlsx_fn = 'pow_sweep'
        self.headers = ['#', 'F', 'Pвх', 'Pвых']

        self.process()

    def process(self):
        self._processed_data = list(self._raw_data)


class FreqSweepResult(MeasureResult):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self._xlsx_fn = 'freq_sweep'
        self.headers = ['#', 'Pвх', 'F', 'Pвых']

        self.process()

    def process(self):
        self._processed_data = list(self._raw_data)
