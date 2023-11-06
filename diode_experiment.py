from arduino_device import ArduinoVISADevice, list_devices


class DiodeExperiment:
    def __init__(self, R, port):
        self.device = ArduinoVISADevice(port=port)
        self.R = R
        return

    def scan(self, start, stop):
        U_LED = []
        I_LED = []

        for i in range(start, stop):
            self.device.set_output_value(value=i)

            U1 = self.device.get_input_voltage(channel=1)
            U2 = self.device.get_input_voltage(channel=2)

            I = U2 / self.R
            U_l = U1 - U2

            U_LED.append(U_l)
            I_LED.append(I)

        self.device.set_output_value(value=0)

        return U_LED, I_LED
