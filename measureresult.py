class MeasureResult:
    def __init__(self, raw_data):
        self.headers = []
        self._raw_data = raw_data
        self._processed_data = list()

    def process(self):
        self._processed_data = [1, 2, 3]
