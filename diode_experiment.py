# This is the model class. From here we communicate with the view class and controller class

from arduino_device import ArduinoVISADevice, list_devices


class DiodeExperiment:
    def __init__(self, port):
        self.device = ArduinoVISADevice(port=port)
        self.R = 220
        return

    # Itarate U0 output from start till stop value and return list of U and I over LED
    def scan(self, start, stop):
        U_LED = []
        I_LED = []

        for i in range(start, stop):
            # Communicate with controller by giving i value set get U1 and U2 channel input
            self.device.set_output_value(value=i)
            U1 = self.device.get_input_voltage(channel=1)
            U2 = self.device.get_input_voltage(channel=2)

            # Calculate I over the LED by taking voltage over the load, so I = U2 / R
            I = U2 / self.R
            # Calculate U over the LED by taking the difference of U before and after the LED
            U_l = U1 - U2

            # Add to lists
            U_LED.append(U_l)
            I_LED.append(I)

        # turn off device
        self.device.set_output_value(value=0)

        return U_LED, I_LED

    def scan_with_error(self, N, start, stop):
        U_LED_values = []
        I_LED_values = []

        # use scan function N times and calculate mean value for every U0 channel output
        U_mean = [0] * (stop - start)
        I_mean = [0] * (stop - start)
        for i in range(N):
            # conduct an experiment and get the U and I values
            U, I = self.scan(start, stop)

            # Temporarily sum up the U and I in the mean list
            for j in range(start, stop):
                U_mean[j] += U[j]
                I_mean[j] += I[j]

            # save every experiment
            U_LED_values.append(U)
            I_LED_values.append(I)
        for i in range(start, stop):
            # Divide sum list by sample size to get the mean values
            U_mean[i] /= N
            I_mean[i] /= N

        # calculate standard deviation adding the squared differences of every measurement and mean
        std_U = [0] * (stop - start)
        std_I = [0] * (stop - start)
        for i in range(N):
            for j in range(start, stop):
                std_U[j] += (U_LED_values[i][j] - U_mean[j])**2
                std_I[j] += (I_LED_values[i][j] - I_mean[j])**2
        for i in range(start, stop):
            std_U[i] = (std_U[i] / (N - 1))**0.5
            std_I[i] = (std_I[i] / (N - 1))**0.5

        # calculate error for set of N experiments by dividing standard deviation N - 1 and taking square root
        U_err = []
        I_err = []
        for U, I in zip(std_U, std_I):
            U_err.append(U / N**0.5)
            I_err.append(I / N**0.5)

        return U_mean, U_err, I_mean, I_err
