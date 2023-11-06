from diode_experiment import DiodeExperiment, list_devices
import matplotlib.pyplot as plt
import csv

print(list_devices())

port = "ASRL8::INSTR"

experiment = DiodeExperiment(port=port)

U_LED, U_err, I_LED, I_err = experiment.scan_with_error(3, 0, 1024)

plt.errorbar(U_LED, I_LED, xerr=U_err, yerr=I_err, marker='.')
plt.savefig('U_I_char.png')
plt.show()

with open('metingen_met_error.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U', 'I', 'U_err', 'I_err'])
    for u, i, u_err, i_err in zip(U_LED, I_LED, U_err, I_err):
        writer.writerow([u, i, u_err, i_err])
