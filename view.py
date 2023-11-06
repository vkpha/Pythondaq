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

with open('metingen_001.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U', 'I'])
    for u, i in zip(U_LED, I_LED):
        writer.writerow([u, i])
