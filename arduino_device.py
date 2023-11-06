import pyvisa


class ArduinoVISADevice:
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n")

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


def list_devices():
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()
