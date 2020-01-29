class MeasureResult:
    def __init__(self, raw_data):
        self.headers = []
        self._raw_data = raw_data
        self._processed_data = list()

    def process(self):
        raise NotImplementedError

    @property
    def data(self):
        return self._processed_data


class PowSweepResult(MeasureResult):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.headers = ['#', 'F', 'Pвх', 'Pвых']

        self.process()

    def process(self):
        self._processed_data = list(self._raw_data)


class FreqSweepResult(MeasureResult):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.headers = ['#', 'Pвх', 'F', 'Pвых']

        self.process()

    def process(self):
        self._processed_data = list(self._raw_data)
