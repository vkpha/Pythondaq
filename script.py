import pyvisa
import matplotlib.pyplot as plt
import csv

class ArduinoVISADevice:
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination="\r\n", write_termination="\n")
    
    def get_indentification(self):
        return self.device.query("*IDN?")
    
    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")
    
    def get_output_value(self):
        return int(self.device.query(f"MEAS:CH0?"))
    
    def get_input_value(self, channel):
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    def get_input_voltage(self, channel):
        return float(self.get_input_value(channel) * (3.3 / 1023))


port = "ASRL8::INSTR"
device = ArduinoVISADevice(port = port)

U_LED = []
I_LED = []

for i in range(1024):
    device.set_output_value(value = i)
    
    q1 = device.get_input_value(channel = 1)
    q2 = device.get_input_value(channel = 2)

    U1 = device.get_input_voltage(channel = 1)
    U2 = device.get_input_voltage(channel = 2)

    R = 220
    I = U2 / R
    U_l = U1 - U2

    U_LED.append(U_l)
    I_LED.append(I)

plt.plot(U_LED, I_LED, '.')
plt.show()
plt.savefig('U_I_char_001.png')

with open('metingen_001.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U', 'I'])
    for u, i in zip(U_LED, I_LED):
        writer.writerow([u, i])

device.set_output_value(value = 0)


