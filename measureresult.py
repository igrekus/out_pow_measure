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
        self._processed_data = [[1, 1, 1, 1], [2, 1, 2, 2], [3, 1, 3, 3]]


class FreqSweepResult(MeasureResult):
    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.headers = ['#', 'Pвх', 'F', 'Pвых']

        self.process()

    def process(self):
        self._processed_data = [[1, 1, 'a', 'a'], [2, 1, 'b', 'b'], [3, 1, 'c', 'c']]
