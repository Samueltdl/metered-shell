import psutil
import win32process
import time
import subprocess


class MonitoringSoftware():
    def __init__(self, software, timeout): # Inicializa o objeto com o diretório, timeout e tempo de cpu inseridos pelo usuário.
        self.software = software
        self.timeout = timeout
        #self.tempo_cpu = tempo_cpu

    def abrir_programa(self): # método que abre o programa do caminho especificado
        return subprocess.Popen([self.software])

    def monitorar_cpu(self): # método que roda um loop que fica monitorando o programa
        
        proc = self.abrir_programa()

        time.sleep(2) # sleep adicionado só para dar tempo de o programa iniciar completamente (pode ser pouco tempo se o programa demora para iniciar)

        process = psutil.Process(proc.pid)

        while process.is_running():

            if self.timeout <= 0: # condição que encerra o programa automaticamente caso tenha atingido o tempo máximo
                process.terminate()

            if not process.is_running(): # vericica se o programa não foi fechado forçadamente
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


software = str(input("\n\nDigite o caminho do processo: "))
timeout = int(input("Digite um tempo máximo de execução do programa (0 caso não queira tempo máximo): "))

monitoramento = MonitoringSoftware(software, timeout)
monitoramento.monitorar_cpu()


################################## ALGUNS DIRETÓRIOS DO MEU PC ###############################
# C:\Program Files\CPUID\HWMonitor\HWMonitor
# C:\Users\samue\AppData\Local\Discord\app-1.0.9155\Discord
# C:\Program Files\Windows NT\Accessories\wordpad.exe