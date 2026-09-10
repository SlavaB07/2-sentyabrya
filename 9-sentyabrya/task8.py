class CPU:
    def __init__(self, name, fr):
        self.name = name
        self.fr = fr
class Memory:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume
class MotherBoard:
    def __init__(self, name, cpu, *mem_slots):
        self.name = name
        self.cpu = cpu
        self.total_mem_slots = 4
        self.mem_slots = list(mem_slots[:4])  # максимум 4
    def get_config(self):
        cpu_str = f"Центральный процессор: {self.cpu.name}, {self.cpu.fr}"
        mem_parts = []
        for mem in self.mem_slots:
            mem_parts.append(f"{mem.name} - {mem.volume}")
        mem_str = "Память: " + "; ".join(mem_parts)
        return [
            f"Материнская плата: {self.name}",
            cpu_str,
            f"Слотов памяти: {self.total_mem_slots}",
            mem_str]
cpu = CPU("Intel Core i7", "3.4 GHz")
mem1 = Memory("Kingston", "8 GB")
mem2 = Memory("Samsung", "8 GB")
mb = MotherBoard("ASUS ROG", cpu, mem1, mem2)
for line in mb.get_config():
    print(line)