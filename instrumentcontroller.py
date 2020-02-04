import time
from os.path import isfile
from PyQt5.QtCore import QObject, pyqtSlot

from instr.instrumentfactory import PowerMeterFactory, GeneratorFactory
from measureresult import PowSweepResult, FreqSweepResult

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
            'Генератор': GeneratorFactory('GPIB0::20::INSTR'),
            'Измеритель мощности': PowerMeterFactory('GPIB0::1::INSTR')
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
        if self.sweepType == 0:
            self.result = PowSweepResult(res, self.secondaryParams['file'])
        else:
            self.result = FreqSweepResult(res, self.secondaryParams['file'])

    def _measure(self, device, secondary):
        param = self.deviceParams[device]
        secondary = self.secondaryParams
        print(f'launch measure with {param} {secondary}')

        self._init()

        if self._sweepType == 0:
            ret = self._run_pow_sweep(secondary)
        else:
            ret = self._run_freq_sweep(secondary)

        self._instruments['Генератор'].set_output(state='OFF')
        return ret

    def _init(self):
        gen = self._instruments['Генератор']
        meter = self._instruments['Измеритель мощности']

        gen.send('SYST:PRES')
        gen.query('*OPC?')

        meter.send('SYST:PRES')
        meter.query('*OPC?')
        meter.send('SENSe1:AVERage ON')
        meter.send('SENSe:AVERage:COUNt 10')
        meter.send('FORMat ASCII')

    def _run_pow_sweep(self, params):
        print('pow sweep', params)
        gen = self._instruments['Генератор']
        meter = self._instruments['Измеритель мощности']

        freq = params['F']
        meter.send(f'SENSe1:FREQuency {freq}')
        gen.set_freq(value=freq, unit='Hz')
        gen.set_output(state='ON')

        p_out = list()
        p_in = list()
        for pwr in self._range(params['Pmin'], params['Pmax'], params['Pstep']):
            gen.set_pow(value=pwr, unit='dB')
            time.sleep(1)
            meter.send('ABORT')
            meter.send('INIT')
            p_out.append(meter.query('FETCH?'))
            p_in.append(pwr)

        return [[freq, i, round(float(o), 2)] for i, o in zip(p_in, p_out)]

    def _run_freq_sweep(self, params):
        print('freq sweep', params)

        gen = self._instruments['Генератор']
        meter = self._instruments['Измеритель мощности']

        pwr = params['P']
        gen.set_pow(value=pwr, unit='dB')
        gen.set_output(state='ON')

        p_out = list()
        f_in = list()
        for frq in self._range(params['Fmin'], params['Fmax'], params['Fstep']):
            gen.set_freq(value=frq, unit='Hz')
            meter.send(f'SENSe1:FREQuency {frq}')
            time.sleep(1)
            meter.send('ABORT')
            meter.send('INIT')
            p_out.append(meter.query('FETCH?'))
            f_in.append(frq)

        return [[pwr, i, round(float(o), 2)] for i, o in zip(f_in, p_out)]

    def _range(self, start, end, step):
        return [start + i * step for i in range(int((end - start) / step) + 1)]

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
