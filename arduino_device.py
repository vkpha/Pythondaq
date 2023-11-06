# This is the controller class. We communicate with the device and return to model class.

import pyvisa


class ArduinoVISADevice:
    def __init__(self, port):
        # Connect with device
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n")

    # Different functions to send queries to device
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

# List devices out of class to know which port to use


def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()
