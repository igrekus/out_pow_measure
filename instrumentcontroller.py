from os.path import isfile
from PyQt5.QtCore import QObject, pyqtSlot

from instr.instrumentfactory import NetworkAnalyzerFactory, PowerMeterFactory
from measureresult import MeasureResult

is_mock = True


class InstrumentController(QObject):
    phases = [
        22.5,
        45.0,
        90.0,
        180.0
    ]

    states = {
        # i: f'{i:06b}' for i in range(64)
        i: i for i in range(64)
    }

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.requiredInstruments = {
            'Генератор': NetworkAnalyzerFactory('GPIB2::18::INSTR'),
            'Измеритель мощности': PowerMeterFactory('GPIB2::10::INSTR')
        }

        self.deviceParams = {
            'Прибор 1': {
                'F': [1.15, 1.35, 1.75, 1.92, 2.25, 2.54, 2.7, 3, 3.47, 3.86, 4.25],
                'mul': 2,
                'P1': 15,
                'P2': 21,
                'Istat': [None, None, None],
                'Idyn': [None, None, None]
            },
        }

        if isfile('./params.ini'):
            import ast
            with open('./params.ini', 'rt', encoding='utf-8') as f:
                raw = ''.join(f.readlines())
                self.deviceParams = ast.literal_eval(raw)

        self.secondaryParams = {
            'F': 1.0,
            'Pmin': -20.0,
            'Pmax': 0,
            'Pstep': 0.1
        }

        self._sweepType = 0

        self.span = 0.1

        self._instruments = dict()
        self.found = False
        self.present = False
        self.hasResult = False

        self.result = None

    def __str__(self):
        return f'{self._instruments}'

    def connect(self, addrs):
        print(f'searching for {addrs}')
        for k, v in addrs.items():
            self.requiredInstruments[k].addr = v
        self.found = self._find()

    def _find(self):
        self._instruments = {
            k: v.find() for k, v in self.requiredInstruments.items()
        }
        return all(self._instruments.values())

    def check(self, params):
        print(f'call check with {params}')
        device, secondary = params
        self.present = self._check(device, secondary)
        print('sample pass')

    def _check(self, device, secondary):
        print(f'launch check with {self.deviceParams[device]} {self.secondaryParams}')
        return self._runCheck(self.deviceParams[device], self.secondaryParams)

    def _runCheck(self, param, secondary):
        print(f'run check with {param}, {secondary}')
        return True

    def measure(self, params):
        print(f'call measure with {params}')
        device, secondary = params

        res = self._measure(device, secondary)
        self.result = MeasureResult(res)

    def _measure(self, device, secondary):
        param = self.deviceParams[device]
        secondary = self.secondaryParams
        print(f'launch measure with {param} {secondary}')

        self._init()

        if self._sweepType == 0:
            self._run_pow_sweep(secondary)
        elif self._sweepType == 1:
            self._run_freq_sweep(secondary)

        return [1, 2]

    def _init(self):
        gen = self._instruments['Генератор']
        meter = self._instruments['Измеритель мощности']

        gen.send('SYST:PRES')
        gen.query('*OPC?')

        meter.send('SYST:PRES')
        gen.query('*OPC?')

    def _run_pow_sweep(self, params):
        print('pow sweep', params)

    def _run_freq_sweep(self, params):
        print('freq sweep', params)

    @pyqtSlot(dict)
    def on_secondary_changed(self, params):
        self.secondaryParams = params

    @property
    def status(self):
        return [i.status for i in self._instruments.values()]

    @property
    def sweepType(self):
        return self._sweepType

    @sweepType.setter
    def sweepType(self, value):
        self._sweepType = value


def parse_float_list(lst):
    return [float(x) for x in lst.split(',')]
