import pyvisa


def ADC(bit):
    return bit * (3.3 / 1023)
def DAC(voltage):
    return voltage / (3.3 / 1023)

rm = pyvisa.ResourceManager("@py")

ports = rm.list_resources()

device = rm.open_resource(
    "ASRL8::INSTR", read_termination="\r\n", write_termination="\n"
)

CH1 = []
CH2 = []

for i in range(1024):
    value = str(i)
    device.query(f"OUT:CH0 {value}")

    q1 = device.query(f"MEAS:CH1?")
    CH1.append((int(q1)))
    q2 = device.query(f"MEAS:CH2?")
    CH2.append(int(q2))

    print(f"On LED: {i} ({ADC(i)} V)    Over resistor: {q2} ({ADC(int(q2))} V)")


