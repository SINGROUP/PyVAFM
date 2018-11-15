#from vafmbase import Circuit
from vafmcircuits import Machine
import math


# \package customs
# Contain the assembly functions for composite PLL circuits.


# \brief Analog PLL composite circuit.
# Assembly function for analog PLL composite circuit.
# The Phase-Frequency Detector (PFD) multiplies the signals, and the result
# is passed to a series of lowpass Sallen-Key filters. The mount of filters
# and their cutoff frequencies are taken from the input parameter \a filters.
#
# \note For this to work, the output \a sin should be connected to \a signal2 in the parent circuit (as shown in example).
# Also, both signals should be normalised (amplitude = 1) and their offset should be removed.
#
#
# \image html apll.png "schema"
#
# \b Initialisation \b parameters:
# - filters = list of cutoff frequencies for PFD lowpass filters
# - Kp = proportional constant of the charge pump
# - Ki = integral constant of the charge pump
# - gain = gain on the charge pump output
# - pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# - \a signal1 = incoming signal
# - \a signal2 = reference signal
# - \a f0 = fundamental frequency
#
# \b Output \b channels:
# - \a sin = sine wave of the internal VCO
# - \a cos = cosine wave of the internal VCO
# - \a df = frequency shift from \a f0
#
#
# \b Example:
# \code{.py}
#machine = Machine(name='machine', dt=1.0e-8, pushed=True);
#
# machine.AddCircuit(type="Machine",name='pll', assembly=aPLL, filters=[1000,500],
#	gain=600.0, f0=1.0e5, Kp=0.4, Ki=500)
#
# machine.Connect("pll.sin","pll.signal2")
# \endcode
#
def aPLL(compo, **keys):

    # I/O
    compo.AddInput("signal1")
    compo.AddInput("signal2")
    compo.AddInput("f0")

    compo.AddOutput("sin")
    compo.AddOutput("cos")
    compo.AddOutput("df")
    compo.AddOutput("phase")

    filters = keys['filters']
    print("prefilters cutoffs: ", filters)

    compo.AddCircuit(type='opMul', name='pfd', pushed=True)
    for i in range(len(filters)):
        f = filters[i]
        compo.AddCircuit(type='SKLP', name='lp'+str(i+1), fc=f, pushed=True)

    compo.AddCircuit(type='PI', name='pump',
                     Kp=keys['Kp'], Ki=keys['Ki'], set=0, pushed=True)
    compo.AddCircuit(type='gain', name='dfgain',
                     gain=keys['gain'], pushed=True)
    compo.AddCircuit(type='opAdd', name='fsum', pushed=True)
    compo.AddCircuit(type='waver', name='vco', amp=1, pushed=True)

    # connections
    compo.Connect("global.signal1", "pfd.in1")
    compo.Connect("global.signal2", "pfd.in2")

    compo.Connect("pfd.out", "lp1.signal")
    for i in range(1, len(filters)):
        compo.Connect("lp"+str(i)+".out", "lp"+str(i+1)+".signal")

    compo.Connect("lp"+str(len(filters))+".out", "pump.signal", "global.phase")
    compo.Connect("pump.out", "dfgain.signal")
    compo.Connect("dfgain.out", "fsum.in1", "global.df")
    compo.Connect("global.f0", "fsum.in2")
    compo.Connect("fsum.out",   "vco.freq")
    compo.Connect("vco.sin",   "global.sin")
    compo.Connect("vco.cos",   "global.cos")
    #compo.Connect("pfd.out",   "global.dbg")

    print("analog PLL assembled!")


# \brief Digital PLL composite circuit.
# Compares the delay between two flip flops becomoing positive allowing frequency shift between two signals to be measured.
#
#
# \note For this to work, the output \a sin should be connected to \a signal2 in the parent circuit (as shown in example).
# Also, both signals should be normalised (amplitude = 1) and their offset should be removed.
#
#
# \b Initialisation \b parameters:
# - fcut = Cutoff frequencies for dPFD lowpass filter
# - Kp = proportional constant of the charge pump
# - Ki = integral constant of the charge pump
# - gain = gain on the charge pump output
# - pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# - \a ref = incoming signal
# - \a vco = reference signal
# - \a f0 = fundamental frequency
#
# \b Output \b channels:
# - \a sin = sine wave of the internal VCO
# - \a cos = cosine wave of the internal VCO
# - \a df = frequency shift from \a f0
#
#
# \b Example:
# \code{.py}
#machine = Machine(name='machine', dt=1.0e-8, pushed=True);
#
# machine.AddCircuit(type="Machine",name='pll', assembly=dPFD, filters=[1000,500],
# gain=600.0, f0=1.0e5, Kp=0.4, Ki=500)
#
# machine.Connect("pll.sin","pll.signal2")
# \endcode
#


def dPFD(compo, **keys):

    # I/O
    compo.AddInput("ref")
    compo.AddInput("vco")
    compo.AddInput("f0")
    compo.AddInput("KI")
    compo.AddInput("KP")

    compo.AddOutput("sin")
    compo.AddOutput("cos")
    compo.AddOutput("df")
    compo.AddOutput("dbg")

    compo.AddCircuit(type='DRFlipFlop', name='ffdr1', D=1, pushed=True)
    compo.AddCircuit(type='DRFlipFlop', name='ffdr2', D=1, pushed=True)

    compo.AddCircuit(type='AND', name='and', pushed=True)
    compo.AddCircuit(type='flip', name='norflp', pushed=True)

    compo.AddCircuit(type='opSub', name='sub', pushed=True)
    compo.AddCircuit(type='gain', name='dfgain',
                     gain=keys["gain"], pushed=True)
    compo.AddCircuit(type='SKLP', name='lowpass', fc=keys["fcut"], pushed=True)

    compo.AddCircuit(type='PI', name='pi', set=0, pushed=True)

    compo.AddCircuit(type='opAdd', name='fsum', pushed=True)
    compo.AddCircuit(type='waver', name='vco', amp=1, pushed=True)

    # connections
    compo.Connect("global.KI", "pi.Ki")
    compo.Connect("global.KP", "pi.Kp")
    compo.Connect("global.ref", "ffdr1.clock")
    compo.Connect("global.vco", "ffdr2.clock")
    compo.Connect("ffdr1.Q", "and.in1", "sub.in2")
    compo.Connect("ffdr2.Q", "and.in2", "sub.in1")
    compo.Connect("and.out", "norflp.signal")
    compo.Connect("norflp.tick", "ffdr1.R", "ffdr2.R")
    compo.Connect("sub.out", "pi.signal")
    compo.Connect("pi.out", "lowpass.signal")
    compo.Connect("lowpass.out", "dfgain.signal")
    compo.Connect("dfgain.out", "fsum.in1", "global.df")
    compo.Connect("global.f0", "fsum.in2")
    compo.Connect("fsum.out",   "vco.freq")
    compo.Connect("vco.sin",   "global.sin")
    compo.Connect("vco.cos",   "global.cos")
    compo.Connect("pi.out",   "global.dbg")

    print("digital PFD assembled!")


# \brief Analogue amplitude detection circuit.
# Passed a singal throuhg a low pass filter to calculate the amplitude of it.
#
# \b Initialisation \b parameters:
# - fcut = Cut off frequency for the low pass filter
#
#
# \b Input \b channels:
# - \a signal = incoming signal
#
# \b Output \b channels:
# - \a amp = Amplitude of the incoming wave
# - \a norm = normalaised input wave.
#
#
# \b Example:
# \code{.py}
# machine.AddCircuit(type="Machine",name='amp', fcut=10000, assembly=aAMPD, pushed=True)
# \endcode

def aAMPD(compo, **keys):

    compo.AddInput("signal")
    compo.AddOutput("amp")
    compo.AddOutput("norm")

    compo.AddCircuit(type='opAbs', name='abs', pushed=True)
    #compo.AddCircuit(type='SKLP', name='lp', fc=keys["fcut"], pushed=True)

    filters = keys['fcut']

    for i in range(len(filters)):
        f = filters[i]
        compo.AddCircuit(type='SKLP', name='lp'+str(i+1), fc=f, pushed=True)

    compo.AddCircuit(type='opDiv', name='nrm', pushed=True)
    compo.AddCircuit(type='limiter', name='lim', min=-1, max=1, pushed=True)

    compo.Connect('global.signal', 'abs.signal')
    compo.Connect('abs.out', 'lp1.signal')

    for i in range(1, len(filters)):
        compo.Connect("lp"+str(i)+".out", "lp"+str(i+1)+".signal")

    compo.Connect("lp"+str(i+1)+".out", 'global.amp')

    compo.Connect('global.signal', 'nrm.in1')
    compo.Connect("lp"+str(i+1)+".out", 'nrm.in2')
    compo.Connect('nrm.out', 'lim.signal')
    compo.Connect('lim.out', 'global.norm')


def dAMPD(compo, **keys):

    compo.AddInput("signal")
    compo.AddOutput("amp")
    compo.AddOutput("norm")

    compo.AddCircuit(type='minmax', name='MinandMax',
                     CheckTime=keys['checktime'])
    compo.AddCircuit(type='avg', name='average',
                     time=keys['avgtime'], moving=False, pushed='True')
    compo.AddCircuit(type='limiter', name='lim', min=-1, max=1, pushed=True)
    compo.AddCircuit(type='opDiv', name='nrm', pushed=True)
    compo.AddCircuit(type='SKLP', name='lp', fc=keys['fc'], pushed=True)

    compo.Connect('global.signal', 'MinandMax.signal')
    compo.Connect('MinandMax.amp', 'global.amp', 'nrm.in2')
    compo.Connect('global.signal', 'nrm.in1')
    compo.Connect('nrm.out', 'global.norm')


def FakePLL(compo, **keys):
    compo.AddInput("signal")
    compo.AddOutput("freq")
    compo.AddOutput("df")
    compo.AddOutput("debug")

    compo.AddCircuit(type='peaker', name='peaker', up=1, pushed=True)
    compo.AddCircuit(type='opDiv', name='div', in1=1, pushed=True)
    compo.AddCircuit(type='opSub', name='sub', in2=keys["fo"], pushed=True)
    compo.AddCircuit(type='avg', name='average',
                     time=keys['AvgTime'], moving=False, pushed='True')

    compo.Connect('global.signal', 'peaker.signal')
    compo.Connect('peaker.delay', 'div.in2')

    compo.Connect('div.out', 'sub.in1')
    compo.Connect('div.out', 'global.freq')

    # compo.Connect('sub.out','global.df')
    compo.Connect('sub.out', 'average.signal')
    compo.Connect('average.out', 'global.df')


# \brief Lock in amplifier.
# Calculates the complex  phase shift and magnitude of a given signal
#
# \b Initialisation \b parameters:
# - fcut = Cut off frequency for the low pass filter
# - intTime = Integration time of the lock in amp
# - CentFreq = the central frequency of the lock in amp signal
# - OutAmp = the outputted amplitude of the reference signal
# - Gain = gain of the final outputted signal
#
# \b Input \b channels:
# - \a signal = incoming signal
# - \a CentFreq = incoming signal
#
# \b Output \b channels:
# - \a amp = Complex magnitude of the signal.
# - \a phase = Complex phase of the signal.
# - \a refWave = the reference wave used in the lock in amp, oscilating at the central frequency.
# - \a X = Real part of the complex output.
# - \a Y = Imaginary part of the complex output.

#
#
# \b Example:
# \code{.py}
#f0 = 10000
# machine.AddCircuit(type="Machine",name='LockInAmp', intTime=1.0/f0 * 100, CentFreq=f0, OutAmp=Az , Gain=2 ,assembly=LockInAmp, pushed=True)
# \endcode


def LockInAmp(compo, **keys):

    compo.AddInput("signal")
    compo.AddInput("CentFreq")

    compo.AddOutput("amp")
    compo.AddOutput("phase")
    compo.AddOutput("refWave")

    compo.AddOutput("X")
    compo.AddOutput("Y")

    compo.AddCircuit(type='waver', name='WaveGen',
                     freq=keys["CentFreq"], amp=1, pushed=True)
    compo.AddCircuit(type='opMul', name='Xmul', pushed=True)
    compo.AddCircuit(type='opMul', name='Ymul', pushed=True)

    compo.AddCircuit(type='opMul', name='gain',
                     pushed=True, in2=keys["OutAmp"])
    compo.AddCircuit(type='opMul', name='AmpGain',
                     pushed=True, in2=keys["Gain"])

    compo.AddCircuit(type='RCLP', name='lpX', order=4,
                     fc=1.0/keys["intTime"], pushed=True)
    compo.AddCircuit(type='RCLP', name='lpY', order=4,
                     fc=1.0/keys["intTime"], pushed=True)

    compo.AddCircuit(type='ComplexMagAndPhase', name='Complex')

    compo.Connect('global.CentFreq', 'WaveGen.freq')

    compo.Connect('global.signal', 'Xmul.in1')
    compo.Connect('WaveGen.cos', 'Xmul.in2')
    compo.Connect('Xmul.out', 'lpX.signal')

    compo.Connect('global.signal', 'Ymul.in1')
    compo.Connect('WaveGen.sin', 'Ymul.in2')
    compo.Connect('Ymul.out', 'lpY.signal')

    compo.Connect('lpX.out', 'Complex.Real')
    compo.Connect('lpY.out', 'Complex.Complex')

    compo.Connect('Complex.Mag', 'AmpGain.in1')
    compo.Connect('AmpGain.out', 'global.amp')

    compo.Connect('Complex.Phase', 'global.phase')

    compo.Connect('WaveGen.cos', 'gain.in1')
    compo.Connect('gain.out', 'global.refWave')

    compo.Connect('lpX.out', 'global.X')
    compo.Connect('lpY.out', 'global.Y')
