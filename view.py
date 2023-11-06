# This is the view object. From here we can use the model class to conduct different kinds of experiments.

from diode_experiment import DiodeExperiment, list_devices
import matplotlib.pyplot as plt
import csv

# Print all the ports that are available and set the port
print(list_devices())
port = "ASRL8::INSTR"

# Call the model class
experiment = DiodeExperiment(port=port)

# Use the scan with error function to conduct an experiment N times
N = 5
U_LED, U_err, I_LED, I_err = experiment.scan_with_error(
    N=5, start=0, stop=1024)

# Plot results
plt.errorbar(U_LED, I_LED, xerr=U_err, yerr=I_err, marker='.')
plt.savefig('U_I_char.png')
plt.show()

# Export to csv file
with open('metingen_met_error.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U_mean', 'I_mean', 'U_err', 'I_err'])
    for u, i, u_err, i_err in zip(U_LED, I_LED, U_err, I_err):
        writer.writerow([u, i, u_err, i_err])
