from diode_experiment import DiodeExperiment, list_devices
import matplotlib.pyplot as plt
import csv

print(list_devices())

port = "ASRL8::INSTR"
R = 220
experiment = DiodeExperiment(R=R, port=port)

U_LED, I_LED = experiment.scan(0, 1024)

plt.plot(U_LED, I_LED, '.')
plt.savefig('U_I_char.png')
plt.show()

with open('metingen_001.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['U', 'I'])
    for u, i in zip(U_LED, I_LED):
        writer.writerow([u, i])
