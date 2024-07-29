import psutil
import win32process
import time
import subprocess



class MonitoringSoftware():
    def __init__(self, software, timeout): #     Inicializa o objeto com o diretório, timeout e tempo de cpu inseridos pelo usuário.
        self.software = software
        #self.software_name = software_name
        self.timeout = timeout
        #self.tempo_cpu = tempo_cpu

    def abrir_programa(self):
        return subprocess.Popen([self.software])

    def get_pid_by_name(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.software:
                return proc
        return None
    
    def monitorar_cpu(self):
        
        self.abrir_programa()
        time.sleep(2)
        proc = self.get_pid_by_name() #pega o pid do processo com base o nome fornecido pelo usuário
        
        process = psutil.Process(proc.pid)

        while self.timeout >= 0:

            if not process.is_running():
                print("\n\n--------------ATENÇÃO---------------")
                print("\nPrograma encerrado antes de terminar a a medição!")
                break

            user_time = process.cpu_times().user
            system_time = process.cpu_times().system
            total_cpu_time = user_time + system_time
            print(f"Tempo de CPU (user): {user_time}")
            print(f"Tempo de CPU (system): {system_time}")

            # Aguarde 1 segundo antes de verificar novamente
            time.sleep(1)
            self.timeout -= 1

        print(f'\n\n---------------------------------------------')
        print(f"\nPrograma finalizado\n\n")
        print(f"tempo de cpu total consumido: {total_cpu_time}\n\n")


software = str(input("\n\nDigite o nome do processo: "))
timeout = int(input("Digite um tempo máximo de execução do programa (0 caso não queira tempo máximo): "))

monitoramento = MonitoringSoftware(software  + ".exe", timeout)
monitoramento.monitorar_cpu()


################################## ALGUNS DIRETÓRIOS DO MEU PC ###############################
# C:\\Windows\\System32\\notepad.exe
# C:\Program Files\CPUID\HWMonitor\HWMonitor
# C:\Users\samue\AppData\Local\Discord\app-1.0.9155\Discord