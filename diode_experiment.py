from arduino_device import ArduinoVISADevice, list_devices


class DiodeExperiment:
    def __init__(self, port):
        self.device = ArduinoVISADevice(port=port)
        self.R = 220
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

    def scan_with_error(self, N, start, stop):
        U_LED_values = []
        I_LED_values = []

        U_mean = [0] * (stop - start)
        I_mean = [0] * (stop - start)
        for i in range(N):
            U, I = self.scan(start, stop)
            for j in range(start, stop):
                U_mean[j] += U[j]
                I_mean[j] += I[j]
            U_LED_values.append(U)
            I_LED_values.append(I)

        for i in range(start, stop):
            U_mean[i] /= N
            I_mean[i] /= N

        std_U = [0] * (stop - start)
        std_I = [0] * (stop - start)

        for i in range(N):
            for j in range(start, stop):
                std_U[j] += (U_LED_values[i][j] - U_mean[j])**2
                std_I[j] += (I_LED_values[i][j] - I_mean[j])**2

        for i in range(start, stop):
            std_U[i] = (std_U[i] / (N - 1))**0.5
            std_I[i] = (std_I[i] / (N - 1))**0.5

        U_err = []
        I_err = []

        for U, I in zip(std_U, std_I):
            U_err.append(U / N**0.5)
            I_err.append(I / N**0.5)

        return U_mean, U_err, I_mean, I_err
