import pyvisa


rm = pyvisa.ResourceManager("@py")

ports = rm.list_resources()

print(ports)

device = rm.open_resource(
    "ASRL8::INSTR", read_termination="\r\n", write_termination="\n"
)

for i in range(1024):
    value = str(i)
    device.query(f"OUT:CH0 {value}")
    print(value)
