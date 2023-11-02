import pyvisa
import matplotlib.pyplot as plt
import csv

def ADC(bit):
    return bit * (3.3 / 1023)

def DAC(voltage):
    return voltage / (3.3 / 1023) 

rm = pyvisa.ResourceManager("@py")

ports = rm.list_resources()

device = rm.open_resource(
    "ASRL8::INSTR", read_termination="\r\n", write_termination="\n"
)

U_LED = []
I_LED = []

for i in range(1024):
    value = str(i)
    device.query(f"OUT:CH0 {value}")
    
    q1 = device.query(f"MEAS:CH1?")
    q2 = device.query(f"MEAS:CH2?")

    U1 = ADC(int(q1))
    U2 = ADC(int(q2))
    R = 220
    I = U2 / R
    U_l = U1 - U2

    U_LED.append(U_l)
    I_LED.append(I)

plt.plot(U_LED, I_LED, '.')
plt.savefig('U_I_char.png')

with open('metingen.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U', 'I'])
    for u, i in zip(U_LED, I_LED):
        writer.writerow([u, i])

device.query(f"OUT:CH0 0")


